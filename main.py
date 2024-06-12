import random
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter.ttk import *
from tdstool import read_tdscsv, process_signal
import pandas as pd
import os


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.Bg = None
        self.Sam = []
        self.data_list = []
        self.all_data_list = []
        self.tk_button_lwqjcfcu = self.__tk_button_lwqjcfcu(self)
        self.tk_input_lwrbzcgo = self.__tk_input_lwrbzcgo(self)
        self.tk_list_box_lwrc07lb = self.__tk_list_box_lwrc07lb(self)
        self.tk_input_lwrc3al1 = self.__tk_input_lwrc3al1(self)
        self.tk_button_lwrc3doc = self.__tk_button_lwrc3doc(self)
        self.tk_label_lwrc3w37 = self.__tk_label_lwrc3w37(self)
        self.tk_label_lwrc3xa5 = self.__tk_label_lwrc3xa5(self)
        self.canvas = self.__tk_canvas_lwrg4ck8(self)  # 初始化画布
        self.save_button = self.__tk_button_save_data(self)  # 添加保存按钮
        self.merge_button = self.__tk_button_merge_data(self)  # 添加合并按钮
        self.save_all_button = self.__tk_button_save_all_data(self)  # 添加保存所有(合并)按钮

        # 添加参数输入框
        self.param_entries = self.__create_param_entries(self)

    def __win(self):
        self.title("TDS-Tool")
        # 设置窗口大小、居中
        width = 700
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_button_lwqjcfcu(self, parent):
        btn = Button(parent, text="打开数据文件夹", takefocus=False, command=lambda: self.check_and_select_folder(self.tk_input_lwrbzcgo))
        btn.place(relx=0.7500, rely=0.0800, relwidth=0.1667, relheight=0.0600)
        return btn

    def check_and_select_folder(self, entry_to_update):
        folder_path = entry_to_update.get()
        if not folder_path or not os.path.isdir(folder_path):
            folder_path = filedialog.askdirectory()
            if folder_path:
                entry_to_update.delete(0, 'end')  # 清空输入框
                entry_to_update.insert(0, folder_path)  # 插入新路径
                self.update_listbox_with_csv_files(folder_path)
        else:
            messagebox.showinfo("info", f"路径打开成功：\n{folder_path}")
            self.update_listbox_with_csv_files(folder_path)

    def update_listbox_with_csv_files(self, folder_path):
        self.tk_list_box_lwrc07lb.delete(0, END)  # 清空列表框
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in csv_files:
            self.tk_list_box_lwrc07lb.insert(END, file)
        self.Sam = [read_tdscsv(os.path.join(folder_path, file)) for file in csv_files]
        self.all_data_list = [self.process_signal_with_params(self.Bg, sam) for sam in self.Sam]  # 处理所有数据
        self.process_and_draw()

    def __tk_input_lwrbzcgo(self, parent):
        ipt = Entry(parent)
        ipt.place(relx=0.2261, rely=0.0900, relwidth=0.4870, relheight=0.0600)
        return ipt

    def __tk_list_box_lwrc07lb(self, parent):
        lb = Listbox(parent, selectmode=MULTIPLE)
        lb.place(relx=0.0348, rely=0.3200, relwidth=0.2609, relheight=0.5700)
        lb.bind('<<ListboxSelect>>', self.on_listbox_select)
        return lb

    def on_listbox_select(self, event):
        selected_files = [event.widget.get(i) for i in event.widget.curselection()]
        folder_path = self.tk_input_lwrbzcgo.get()
        self.Sam = [read_tdscsv(os.path.join(folder_path, file)) for file in selected_files]
        self.process_and_draw()

    def __tk_input_lwrc3al1(self, parent):
        ipt = Entry(parent)
        ipt.place(relx=0.2167, rely=0.2000, relwidth=0.4667, relheight=0.0600)
        return ipt

    def __tk_button_lwrc3doc(self, parent):
        btn = Button(parent, text="打开背景", takefocus=False, command=lambda: self.check_and_select_file(self.tk_input_lwrc3al1))
        btn.place(relx=0.7500, rely=0.2000, relwidth=0.1667, relheight=0.0600)
        return btn

    def check_and_select_file(self, entry_to_update):
        file_path = entry_to_update.get()
        if not file_path or not (os.path.isfile(file_path) and file_path.endswith('.csv')):
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                entry_to_update.delete(0, 'end')  # 清空输入框
                entry_to_update.insert(0, file_path)  # 插入新路径
                self.Bg = read_tdscsv(file_path)
                self.process_and_draw()
        else:
            messagebox.showinfo("info", f"文件打开成功：\n{file_path}")

    def process_and_draw(self):
        if self.Bg is not None and self.Sam:
            self.data_list = [self.process_signal_with_params(self.Bg, sam) for sam in self.Sam]
            self.draw_data(self.data_list)

    def process_signal_with_params(self, Bg, Sam):
        params = {key: float(entry.get()) for key, entry in self.param_entries.items()}
        # Ensure the appropriate parameters are integers
        for int_param in ['add0', 'addwin', 't11', 't12', 't21', 't22']:
            params[int_param] = int(params[int_param])
        return process_signal(Bg, Sam, **params)

    def draw_data(self, data_list):
        for widget in self.canvas.winfo_children():
            widget.destroy()  # 清空画布上的所有小部件
        fig, ax = plt.subplots(figsize=(8, 6))  # 设置图表的比例为3:4
        for data in data_list:
            ax.plot(data.iloc[:, 0], data.iloc[:, 1])
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Transmission')
        fig.tight_layout()  # 调整图表布局以适应画布
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        plt.close(fig)  # 关闭当前图形窗口

    def __tk_label_lwrc3w37(self, parent):
        label = Label(parent, text="TDS数据路径", anchor="center")
        label.place(relx=0.0348, rely=0.0900, relwidth=0.1391, relheight=0.0600)
        return label

    def __tk_label_lwrc3xa5(self, parent):
        label = Label(parent, text="背景路径", anchor="center")
        label.place(relx=0.0348, rely=0.2000, relwidth=0.1391, relheight=0.0600)
        return label

    def __tk_canvas_lwrg4ck8(self, parent):
        canvas = Canvas(parent, bg="#aaa")
        canvas.place(relx=0.2571, rely=0.3200, relwidth=0.5429, relheight=0.5700)
        return canvas

    def __tk_button_save_data(self, parent):
        btn = Button(parent, text="保存选中(单独)", takefocus=False, command=self.save_data)
        btn.place(relx=0.3548, rely=0.9100, relwidth=0.2348, relheight=0.0600)      
        return btn

    def __tk_button_merge_data(self, parent):
        btn = Button(parent, text="保存选中(合并)", takefocus=False, command=self.merge_data)
        btn.place(relx=0.0661, rely=0.9180, relwidth=0.2017, relheight=0.0600)
        return btn

    def __tk_button_save_all_data(self, parent):
        btn = Button(parent, text="保存所有(合并)", takefocus=False, command=self.save_all_data)
        btn.place(relx=0.6000, rely=0.9100, relwidth=0.2348, relheight=0.0600)
        return btn

    def save_data(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for i, data in enumerate(self.data_list):
                file_path = os.path.join(folder_path, f'processed_data_{i+1}.csv')
                data.to_csv(file_path, index=False)
            messagebox.showinfo("info", f"数据已成功保存到：\n{folder_path}")

    def merge_data(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            combined_data = pd.DataFrame()

            for i, data in enumerate(self.data_list):
                if combined_data.empty:
                    combined_data['Time'] = data.iloc[:, 0]  # 假设第一列为时间列或共同X轴
                combined_data[f'Data_{i+1}'] = data.iloc[:, 1]  # 其余列依次添加

            file_path = os.path.join(folder_path, 'combined_processed_data.csv')
            combined_data.to_csv(file_path, index=False)
            messagebox.showinfo("info", f"数据已成功保存到：\n{file_path}")

    def save_all_data(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            combined_data = pd.DataFrame()

            for i, data in enumerate(self.all_data_list):
                if combined_data.empty:
                    combined_data['Time'] = data.iloc[:, 0]  # 假设第一列为时间列或共同X轴
                combined_data[f'Data_{i+1}'] = data.iloc[:, 1]  # 其余列依次添加

            file_path = os.path.join(folder_path, 'combined_all_processed_data.csv')
            combined_data.to_csv(file_path, index=False)
            messagebox.showinfo("info", f"所有数据已成功保存到：\n{file_path}")

    def __create_param_entries(self, parent):
        params = {
            "dt": 0.002, "add0": 0, "addwin": 1,
            "t11": 0, "t12": 100, "t21": 0, "t22": 100,
            "f_min": 0.6, "f_max": 1.6
        }
        entries = {}
        for idx, (param, default) in enumerate(params.items()):
            label = Label(parent, text=f"{param}:")
            label.place(relx=0.8143, rely=0.3200 + idx * 0.0500, relwidth=0.0714, relheight=0.0600)
            entry = Entry(parent)
            entry.insert(0, str(default))
            entry.place(relx=0.9000, rely=0.3200 + idx * 0.0500, relwidth=0.0714, relheight=0.0600)
            entries[param] = entry
        return entries


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
