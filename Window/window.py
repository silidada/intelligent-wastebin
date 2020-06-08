#!/usr/bin/env python
# @Project -> File  :intelligent-wastebin -> window
# @Date     : 2020/5/22 18:01
# @Author   : ChenHaHa
# @Email:   :silidada@163.com

import tkinter as tk
from PIL import Image, ImageTk


class Window:
    def __init__(self, pie_path):
        """
        :param pie_path: a dict, such as {'last_week': './pie.png', ...}
        """
        self.root = tk.Tk()
        self.root.title("垃圾分布统计")
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 1000
        height = 600
        size = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)
        self.button_num = 0
        self.frame_num = 0
        self.empty_label_num = 0
        self.image_label_num = 0
        self.pie_path = pie_path
        self.pie_label = None
        self.pie_size = (500, 600)

    def built_bottom(self, frame, size, position, text, function, bd=1):
        h = size[0]
        w = size[1]
        row = position[0]
        column = position[1]
        button = tk.Button(frame, text=text, height=h, width=w, command=function, bd=bd)
        button.grid(row=row, column=column)

        self.button_num += 1

        return button

    def built_frame(self, frame, position, grid=True):
        frame = tk.Frame(frame)
        row = position[0]
        column = position[1]
        if grid:
            frame.grid(row=row, column=column)

        self.frame_num += 1

        return frame

    def built_empty_label(self, frame, position, size):
        h = size[0]
        w = size[1]
        label = tk.Label(frame, height=h, width=w)
        row = position[0]
        column = position[1]
        label.grid(row=row, column=column)
        self.empty_label_num += 1

        return label

    def built_image_label(self, frame, photo_path, position, size):
        global photo
        h = size[0]
        w = size[1]
        try:
            photo = Image.open(fp=photo_path)
            photo = photo.resize(size=(w, h))
            photo = ImageTk.PhotoImage(photo)
            label = tk.Label(frame, compound='center', image=photo, height=h, width=w)
        except Exception as e:
            label = tk.Label(frame, text='还木有统计数据哦', height=h//15, width=w//15)

        row = position[0]
        column = position[1]
        label.grid(row=row, column=column)

        self.image_label_num += 1

        return label

    def button_choose(self, choose):
        self.init_face.destroy()
        self.built_second_face(choose)
        self.second_face.grid(row=0, column=0)

    def empty_function(self):
        pass

    def built_second_face(self, choose):
        # 上方frame
        frm4 = self.built_frame(position=(0, 0), frame=self.second_face)
        # 下方frame
        frm5 = self.built_frame(position=(1, 0), frame=self.second_face)

        # 左侧button
        button4 = self.built_bottom(frame=frm4, size=(1, 7), position=(0, 0),
                                    text='最近一周', function=lambda: self.change_pie(1), bd=0)
        # 中间button
        button5 = self.built_bottom(frame=frm4, size=(1, 7), position=(0, 1),
                                    text='最近一月', function=lambda: self.change_pie(2), bd=0)
        # 右侧button
        button6 = self.built_bottom(frame=frm4, size=(1, 7), position=(0, 2),
                                    text='最近一年', function=lambda: self.change_pie(3), bd=0)

        # 图片和右侧的空位
        empty_label = self.built_empty_label(frame=frm5, position=(1, 0), size=(1, 28))

        # 按钮和图片之间的空位
        empty_label1 = self.built_empty_label(frame=frm5, position=(0, 0), size=(2, 1))

        if choose == 1:
            self.pie_label = self.built_image_label(frame=frm5, photo_path=self.pie_path['last_week'],
                                                    position=(1, 1), size=self.pie_size)
        elif choose == 2:
            self.pie_label = self.built_image_label(frame=frm5, photo_path=self.pie_path['last_month'],
                                                    position=(1, 1), size=self.pie_size)
        elif choose == 3:
            self.pie_label = self.built_image_label(frame=frm5, photo_path=self.pie_path['last_year'],
                                                    position=(1, 1), size=self.pie_size)

    def change_pie(self, choose):
        global photo1
        if choose == 1:
            photo1 = Image.open(fp=self.pie_path['last_week'])
        elif choose == 2:
            photo1 = Image.open(fp=self.pie_path['last_month'])
        elif choose == 3:
            photo1 = Image.open(fp=self.pie_path['last_year'])
        h = self.pie_size[0]
        w = self.pie_size[1]
        photo1 = photo1.resize(size=(w, h))
        photo1 = ImageTk.PhotoImage(photo1)
        self.pie_label.configure(image=photo1)
        self.pie_label.update()

    def __call__(self, *args, **kwargs):
        # 开始界面
        self.init_face = self.built_frame(frame=self.root, position=(0, 0))
        # 最上方的frame
        self.frm1 = self.built_frame(position=(0, 0), frame=self.init_face)
        # 中间的frame
        self.frm2 = self.built_frame(position=(1, 0), frame=self.init_face)
        # 最下方的frame
        self.frm3 = self.built_frame(position=(2, 0), frame=self.init_face)
        # 左侧按钮
        self.button1 = self.built_bottom(frame=self.frm3, size=(2, 15), position=(0, 1),
                                         text='最近一周', function=lambda: self.button_choose(1))
        # 中间按钮
        self.button2 = self.built_bottom(frame=self.frm3, size=(2, 15), position=(0, 3),
                                         text='最近一个月', function=lambda: self.button_choose(2))
        # 右侧按钮
        self.button3 = self.built_bottom(frame=self.frm3, size=(2, 15), position=(0, 5),
                                         text='最近一年', function=lambda: self.button_choose(3))
        # 图片
        self.image_label = self.built_image_label(frame=self.frm1, photo_path=r'C:\Users\HaHa Chen\Downloads\1.gif',
                                                  position=(1, 1), size=(150, 300))
        # 最上方的孔label, 让图片离顶部远一点
        self.empty_label1 = self.built_empty_label(frame=self.frm1, position=(0, 0), size=(5, 42))
        # 图片和按钮之间的label, 让图片和按钮隔开
        self.empty_label2 = self.built_empty_label(frame=self.frm2, position=(0, 0), size=(6, 2))
        # 最左侧按钮左边的label, 让按钮里左边远一点
        self.empty_label3 = self.built_empty_label(frame=self.frm3, position=(0, 0), size=(1, 37))
        # 左侧按钮和中间按钮之间的label
        self.empty_label4 = self.built_empty_label(frame=self.frm3, position=(0, 2), size=(1, 8))
        # 中间和右侧按钮之间的label
        self.empty_label5 = self.built_empty_label(frame=self.frm3, position=(0, 4), size=(1, 8))
        # 右侧按钮右侧的label
        # self.empty_label6 = self.built_empty_label(frame=self.frm3, position=(0, 6), size=(1, 5))

        # 次页面
        self.second_face = self.built_frame(frame=self.root, position=(0, 0), grid=False)


if __name__ == "__main__":
    w = Window(pie_path={'last_week': r'D:\File\pycharm2019\rubbish-recognization\lalala.png',
                         'last_month': r'D:\download\0.png',
                         'last_year': r'ajfafl'})
    w()
    w.root.mainloop()
