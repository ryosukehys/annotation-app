import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
import random
import os
import glob
from PIL import Image, ImageTk

meshcode = "90000000"
day = "20230000"
linenum = "0"
kyosaku = "0"
day_list = []

INT_PICTURE_SIZE = 300
INT_COLUMN_COUNTS = 3
CLASS = ["level1", "level2", "level3"]
keyboard_str = "123456789"


###関数(主要でない)###
def return_daylist():
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
    day_list = [i.strftime("%Y%m%d") for i in date_index]
    weeklist = weekly_list(day_list)
    return weeklist


###関数###
def write_csv(meshcode, day, linenum, kyosaku):
    df = pd.read_csv("annotation.csv")
    df_2 = pd.Series(
        [day, linenum, kyosaku, meshcode],
        index=["day", "linenum", "kyosaku", "meshcode"],
    )
    save_csv = pd.concat([df, pd.DataFrame(df_2).T])
    save_csv.to_csv("annotation.csv", index=False)
    print(meshcode, day, kyosaku)
    click_button()


def return_mesh_day():
    df = pd.read_csv("meshcode.csv")
    mesh_list = list(df["meshcode"])
    day_list = return_daylist()
    return random.choice(mesh_list), random.choice(day_list)


def file_exits():
    global meshcode
    global day_list
    meshcode, day_list = return_mesh_day()
    flag = False
    jpg_file_list_all = []
    for day in day_list:
        dir_path = f"Bus_B_toWakkanai/{meshcode}/{day}/"
        if os.path.isdir(dir_path):
            flag = True
            jpg_file_list = glob.glob(f"{dir_path}/*jpg")
            jpg_file_list_all.extend(jpg_file_list)
    if flag is False:
        return flag
    if flag is True:
        print(meshcode, day_list[0])
        return jpg_file_list_all


# 取得した画像を表示
def show_pictures(canvas, picture_path):
    canvas.delete("all")
    label_index = tk.Label(canvas, textvariable=f"{meshcode}, {day_list[0]}", width=10)
    label_index.grid(column=4, row=1, padx=5)

    for index, file_name in enumerate(picture_path):
        img = arrange_image(file_name)
        img = ImageTk.PhotoImage(image=img)
        row_no = int(index / INT_COLUMN_COUNTS)
        column_no = int(index % INT_COLUMN_COUNTS)
        canvas.create_image(
            column_no * INT_PICTURE_SIZE,
            row_no * INT_PICTURE_SIZE,
            anchor="nw",
            image=img,
        )
        # 画像を配置
        img_list.append(img)


# 指定のサイズにファイルを成形
def arrange_image(file_name):
    img = Image.open(file_name)
    img_width, img_height = img.size
    reducation_size = img_width if img_width >= img_height else img_height
    return img.resize(
        (
            int(img_width * (INT_PICTURE_SIZE / reducation_size)),
            int(img_height * (INT_PICTURE_SIZE / reducation_size)),
        )
    )


# 画像を表示
def show_pictures(canvas, picture_path):
    canvas.delete("all")

    for index, file_name in enumerate(picture_path):
        img = arrange_image(file_name)
        img = ImageTk.PhotoImage(image=img)
        row_no = int(index / INT_COLUMN_COUNTS)
        column_no = int(index % INT_COLUMN_COUNTS)
        canvas.create_image(
            column_no * INT_PICTURE_SIZE,
            row_no * INT_PICTURE_SIZE,
            anchor="nw",
            image=img,
        )
        # 画像を配置
        img_list.append(img)


# ガベコレに消されないようにイメージリストに画像を入れておく用のリスト
img_list = []


def click_button():
    pictures = file_exits()
    i = 0
    while pictures is False and i < 100:
        pictures = file_exits()
        i += 1
    if pictures is False:
        print("対象ディレクトリ、画像が存在しません")
        return 0
    show_pictures(scroll_canvas, pictures)


img_list = []

# メインウィンドウの作成
window = tk.Tk()
# メインウィンドウのサイズ指定
window.geometry("1100x600")

# メインフレーム
# input_frame
input_frame = tk.Frame(window, width=1100, height=100, bg="black")
input_frame.pack()

# output_frame
output_frame = tk.Frame(window, width=1100, height=400, bg="yellow")
output_frame.pack()


# 画像表示用のcanvasを作成
scroll_canvas = tk.Canvas(output_frame, width=1050, height=500, bg="white")
scroll_canvas.grid(column=0, row=0, columnspan=7)
bar = tk.Scrollbar(output_frame, orient=tk.VERTICAL)
bar.grid(column=7, row=0, sticky="ns")
bar.config(command=scroll_canvas.yview)
scroll_canvas.config(yscrollcommand=bar.set)
# scroll_canvasの表示範囲
scroll_canvas.config(scrollregion=(0, 0, 1100, 1200))

run_button = tk.Button(input_frame, text="表示", command=click_button)

run_button.grid(column=2, row=0, padx=5)

class_buttun = []
for i, c in enumerate(CLASS):
    key = keyboard_str[i]
    print(i)
    class_buttun.append(
        tk.Button(
            output_frame,
            text=f"{c} ({key})",
            command=lambda kyo=i: write_csv(meshcode, day_list[0], linenum, kyo),
        )
    )
    class_buttun[i].grid(row=1, column=i, padx=5, pady=10, sticky="nsew")

# run_button = tk.Button(
#     root, text="Run", command=lambda: write_csv(meshcode, day, linenum, kyosaku)
# )
# run_button.place(x=160, y=40)


# ウィンドウの状態を維持
window.mainloop()
