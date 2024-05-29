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
    df = pd.DataFrame(data, columns=['Index', 'Frequency', 'Value'])
    df.drop(index=0, inplace=True)
    df.drop(columns='Index', inplace=True)
    return df