import numpy as np
import pandas as pd

def read_tdscsv(csv_file_path):
    # 打开CSV文件并读取所有行
    with open(csv_file_path, 'r') as file:
        lines = file.readlines()

    # 初始化一个空列表来存储数据
    data = []

    # 标志来表示是否已经到达"Result Data"部分
    found_result_data = False

    # 遍历文件的每一行
    for line in lines:
        # 如果找到"Result Data"部分，则设置标志
        if "++++++ Result Data ++++++" in line:
            found_result_data = True
            continue  # 继续下一行

        # 如果已经找到"Result Data"部分，开始提取数据
        if found_result_data and line.strip():  # 忽略空行
            # 将每行拆分成字段，逗号分隔
            fields = line.strip().split(',')
            # 提取Index、XAxis、Result，并将它们作为元组加入到data列表中
            data.append((fields[0], fields[1], fields[2]))

    # 创建DataFrame
    df = pd.DataFrame(data, columns=['Index', 'Time', 'Value'])
    df.drop(index=0, inplace=True)
    df.drop(columns='Index', inplace=True)
    return df.apply(pd.to_numeric, errors='coerce')




def process_signal(BG, Sam, dt=0.002, add0=0, addwin=1, t11=0, t12=100, t21=0, t22=100, f_min=0.6, f_max=1.6):
    import numpy as np
    import pandas as pd
    
    # 初始化变量（示例数据）
    refE = BG.iloc[:, 1]
    samE = Sam.iloc[:, 1]
    refE_max_index = refE.idxmax()
    samE_max_index = samE.idxmax()
    BG_value = BG.iloc[refE_max_index, 0]
    Sam_value = Sam.iloc[samE_max_index, 0]
    Delay = BG_value - Sam_value

    # 计算点数和频率分辨率
    point = len(BG) + add0
    df = 1 / (dt * point)
    f = np.arange(0, point) * df

    # 时间数组和相位
    time = np.arange(0, point) * dt
    phase0 = 2 * np.pi * f * Delay

    # 窗函数
    y1 = np.ones(len(refE))
    y2 = np.ones(len(samE))
    
    if addwin == 1:
        # 对于y1的汉宁窗
        for j in range(len(refE)):
            t = time[j]
            if t11 <= t <= t12:
                # 应用汉宁窗函数
                y1[j] *= 0.5 * (1 - np.cos(2 * np.pi * (t - t11) / (t12 - t11)))
            else:
                y1[j] = 0  # 在窗外的点可以设置为0或其他衰减函数

        # 对于y2的汉宁窗
        for j in range(len(samE)):
            t = time[j]
            if t21 <= t <= t22:
                # 应用汉宁窗函数
                y2[j] *= 0.5 * (1 - np.cos(2 * np.pi * (t - t21) / (t22 - t21)))
            else:
                y2[j] = 0  # 在窗外的点可以设置为0或其他衰减函数

    # 信号处理
    Eref = np.concatenate((refE * y1, np.zeros(add0)))  # 参考信号应用窗函数并进行零填充
    Esam = np.concatenate((samE * y2, np.zeros(add0)))  # 样本信号应用窗函数并进行零填充

    # 确保补零后的数组长度一致
    Eref = np.concatenate((refE * y1, np.zeros(point - len(refE * y1))))
    Esam = np.concatenate((samE * y2, np.zeros(point - len(samE * y2))))

    Eref1 = np.fft.fft(Eref)
    Esam1 = np.fft.fft(Esam)
    Pref = np.abs(Eref1)
    Psam = np.abs(Esam1)
    FFTt = Esam1 / Eref1
    T = np.abs(FFTt)**2
    TdB = 20 * np.log10(T)
    n = 0
    phase = -np.unwrap(np.angle(FFTt)) + n * np.pi
    gro = np.diff(phase) / np.diff(f)

    # 设置想要获取的频率范围
    index_min = np.argmax(f >= f_min)  # 找到最小频率的索引
    index_max = np.argmax(f > f_max)   # 找到最大频率的索引

    # 获取传输数据的最大值
    max_T = np.max(T[index_min:index_max])
    # 如果最大值大于1，则将所有点向下平移
    if max_T > 1:
        shift = max_T - 1
        T_shifted = T[index_min:index_max] - shift
    else:
        T_shifted = T[index_min:index_max]

    # 创建并返回 DataFrame
    result_df = pd.DataFrame({
        'Frequency (THz)': f[index_min:index_max],
        'Transmission (unitless)': T_shifted
    })
    
    return result_df
