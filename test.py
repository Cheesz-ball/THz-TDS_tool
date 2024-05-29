import random
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter.ttk import *
from tdstool import read_tdscsv,process_signal
import pandas as pd
import os



class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.Bg = None
        self.Sam = None
        self.tk_button_lwqjcfcu = self.__tk_button_lwqjcfcu(self)
        self.tk_input_lwrbzcgo = self.__tk_input_lwrbzcgo(self)
        self.tk_list_box_lwrc07lb = self.__tk_list_box_lwrc07lb(self)
        self.tk_input_lwrc3al1 = self.__tk_input_lwrc3al1(self)
        self.tk_button_lwrc3doc = self.__tk_button_lwrc3doc(self)
        self.tk_label_lwrc3w37 = self.__tk_label_lwrc3w37(self)
        self.tk_label_lwrc3xa5 = self.__tk_label_lwrc3xa5(self)
        self.canvas = self.__tk_canvas_lwrg4ck8(self)  # 初始化画布

    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        width = 600
        height = 500
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

    def __tk_input_lwrbzcgo(self, parent):
        ipt = Entry(parent)
        ipt.place(relx=0.2167, rely=0.0800, relwidth=0.4667, relheight=0.0600)
        return ipt

    def __tk_list_box_lwrc07lb(self, parent):
        lb = Listbox(parent)
        lb.place(relx=0.2233, rely=0.5320, relwidth=0.2500, relheight=0.2000)
        lb.bind('<<ListboxSelect>>', self.on_listbox_select)
        return lb

    def on_listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            file_name = event.widget.get(index)
            folder_path = self.tk_input_lwrbzcgo.get()
            file_path = os.path.join(folder_path, file_name)
            self.read_and_assign_sam(file_path)

    def read_and_assign_sam(self, file_path):
        self.Sam = read_tdscsv(file_path)
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
        if self.Bg is not None and self.Sam is not None:
            result = process_signal(self.Bg, self.Sam)
            self.draw_data(result)

    def draw_data(self, data):
        for widget in self.canvas.winfo_children():
            widget.destroy()  # 清空画布上的所有小部件
        fig, ax = plt.subplots()
        ax.plot(data.iloc[:, 0], data.iloc[:, 1])
        ax.set_xlabel('X-axis Label')
        ax.set_ylabel('Y-axis Label')
        ax.set_title('Processed Signal')
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

    def __tk_label_lwrc3w37(self, parent):
        label = Label(parent, text="TDS数据路径", anchor="center")
        label.place(relx=0.0083, rely=0.0800, relwidth=0.1333, relheight=0.0600)
        return label

    def __tk_label_lwrc3xa5(self, parent):
        label = Label(parent, text="背景路径", anchor="center")
        label.place(relx=0.0083, rely=0.2000, relwidth=0.1333, relheight=0.0600)
        return label

    def __tk_canvas_lwrg4ck8(self, parent):
        canvas = Canvas(parent, bg="#aaa")
        canvas.place(relx=0.4233, rely=0.4760, relwidth=0.5200, relheight=0.4120)
        return canvas

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
