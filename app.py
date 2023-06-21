import tkinter as tk
import pandas as pd

meshcode = "90000000"
day = "20230000"
linenum = "0"
kyosaku = "0"


###関数###
def write_csv(meshcode, day, linenum, kyosaku):
    df = pd.read_csv("annotation.csv")
    df_2 = pd.Series(
        [day, linenum, kyosaku, meshcode],
        index=["day", "linenum", "kyosaku", "meshcode"],
    )
    save_csv = pd.concat([df, pd.DataFrame(df_2).T])
    save_csv.to_csv("annotation.csv", index=False)


# ウィンドウの作成
root = tk.Tk()
# ウィンドウのサイズ指定
root.geometry("350x100")

run_button = tk.Button(
    root, text="Run", command=lambda: write_csv(meshcode, day, linenum, kyosaku)
)
run_button.place(x=160, y=40)


# ウィンドウの状態を維持
root.mainloop()
