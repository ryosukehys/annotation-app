import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
import random
import os
import glob
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self, main, classes):
        self.main = main
        self.meshcode = "00000000"
        # self.day = "20220123"
        self.classes = classes
        self.int_column_counts = 3
        self.int_picture_size = 300
        self.Bus_type = "Bus_B"
        self.which_going = "toWakkanai"
        self.image_dir = f"{self.Bus_type}_{self.which_going}/"
        self.keyboard_str = "12345678"
        self.line_num = 1
        self.day_list = []
        self.mesh_list = []
        self.pictures = []
        self.img_list = []
        self.init_window()

    def init_window(self):
        # ウィンドウのサイズ指定
        self.main.geometry("1100x600")
        # メインフレーム
        # input_frame
        self.input_frame = tk.Frame(self.main, width=1100, height=100, bg="black")
        self.input_frame.pack()
        # output_frame
        self.output_frame = tk.Frame(self.main, width=1100, height=400, bg="yellow")
        self.output_frame.pack()
        # 画像表示用のcanvasを作成
        self.scroll_canvas = tk.Canvas(
            self.output_frame, width=1050, height=500, bg="white"
        )
        self.scroll_canvas.grid(column=0, row=0, columnspan=7)
        self.bar = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL)
        self.bar.grid(column=7, row=0, sticky="ns")
        self.bar.config(command=self.scroll_canvas.yview)
        self.scroll_canvas.config(yscrollcommand=self.bar.set)
        # scroll_canvasの表示範囲
        self.scroll_canvas.config(scrollregion=(0, 0, 1100, 1200))
        # 実行ボタンの生成
        self.run_button = tk.Button(
            self.input_frame, text="表示", command=self.click_button
        )
        self.run_button.grid(column=2, row=0, padx=5)
        # クラスの番号を振るボタンを作成
        self.class_buttun = []
        for i, c in enumerate(self.classes):
            key = self.keyboard_str[i]
            print(i)
            self.class_buttun.append(
                tk.Button(
                    self.output_frame,
                    text=f"{c} ({key})",
                    command=lambda kyo=i: self.write_csv(kyo),
                )
            )
            self.class_buttun[i].grid(row=1, column=i, padx=5, pady=10, sticky="nsew")

    def click_button(self):
        self.pictures = self.file_exits()
        self.i = 0
        while self.pictures is False and self.i < 100:
            self.pictures = self.file_exits()
            self.i += 1
        if self.pictures is False:
            print("対象ディレクトリ、画像が存在しません")
            return 0
        # print(self.pictures, self.i)
        self.show_pictures()

    # 画像を表示
    def show_pictures(self):
        self.scroll_canvas.delete("all")

        for index, file_name in enumerate(self.pictures):
            # print(self.pictures)
            img = self.arrange_image(file_name)
            img = ImageTk.PhotoImage(image=img)
            row_no = int(index / self.int_column_counts)
            column_no = int(index % self.int_column_counts)
            self.scroll_canvas.create_image(
                column_no * self.int_picture_size,
                row_no * self.int_picture_size,
                anchor="nw",
                image=img,
            )
            # 画像を配置
            self.img_list.append(img)

    def arrange_image(self, file_name):
        img = Image.open(file_name)
        img_width, img_height = img.size
        reducation_size = img_width if img_width >= img_height else img_height
        return img.resize(
            (
                int(img_width * (self.int_picture_size / reducation_size)),
                int(img_height * (self.int_picture_size / reducation_size)),
            )
        )

    def return_daylist(self):
        def weekly_list(day_list):  # [[一週間ごとのリスト], [--],,,]を作る
            all = []
            day = 1
            weekly = []
            for i in day_list:
                if day % 7 == 0 and day > 0:
                    weekly.append(i)
                    all.append(weekly)
                    weekly = []
                else:
                    weekly.append(i)
                day += 1
            return all

        date_index = list(pd.date_range(start="2021-12-01", end="2022-02-28", freq="D"))
        self.day_list = [i.strftime("%Y%m%d") for i in date_index]
        weeklist = weekly_list(self.day_list)
        return weeklist

    # 関数
    def write_csv(self, kyosaku):
        df = pd.read_csv("annotation.csv")
        df_2 = pd.Series(
            [self.day_list[0], self.line_num, kyosaku, self.meshcode],
            index=["day", "linenum", "kyosaku", "meshcode"],
        )
        save_csv = pd.concat([df, pd.DataFrame(df_2).T])
        save_csv.to_csv("annotation.csv", index=False)
        print(self.meshcode, self.day_list[0], kyosaku)
        self.click_button()

    def return_mesh_day(
        self,
    ):
        df = pd.read_csv("meshcode.csv")
        self.mesh_list = list(df["meshcode"])
        self.day_list = self.return_daylist()
        return random.choice(self.mesh_list), random.choice(self.day_list)

    def file_exits(self):
        self.meshcode, self.day_list = self.return_mesh_day()
        flag = False
        jpg_file_list_all = []
        for day in self.day_list:
            dir = f"{self.image_dir}/{self.meshcode}/{day}"
            if os.path.isdir(dir):
                flag = True
                jpg_file_list = glob.glob(f"{dir}/*.jpg")
                jpg_file_list_all.extend(jpg_file_list)
        if flag is False:
            # print(dir, self.meshcode, self.day_list)
            return flag
        if flag is True:
            # print(self.meshcode, self.day_list[0], flag)
            return jpg_file_list_all


classes = ["level1", "level2", "level3"]
main = tk.Tk()
MainWindow(main, classes)
main.mainloop()
