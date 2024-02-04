import cv2
from matplotlib import pyplot as plt
import tkinter as tk
import tkinter.filedialog


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("二値化プログラム")

        self.frame_file = tk.Frame(self.master)
        self.label_src_img = tk.Label(self.frame_file)
        self.button_open = tk.Button(self.frame_file, text="Open...", command=self.open_file)
        self.label_src_img.pack()
        self.button_open.pack()
        self.frame_file.pack()

        self.frame_slider = tk.Frame(self.master)
        self.thresh_r = tk.IntVar(value=127)
        self.thresh_g = tk.IntVar(value=127)
        self.thresh_b = tk.IntVar(value=127)
        self.label_bin_r = tk.Label(self.frame_slider, text="Red")
        self.label_bin_g = tk.Label(self.frame_slider, text="Greed")
        self.label_bin_b = tk.Label(self.frame_slider, text="Blue")
        self.scale_bin_r = tk.Scale(self.frame_slider, variable=self.thresh_r,
                               orient=tk.HORIZONTAL, from_=0, to=255, length=300, width=20)
        self.scale_bin_g = tk.Scale(self.frame_slider, variable=self.thresh_g,
                               orient=tk.HORIZONTAL, from_=0, to=255, length=300, width=20)
        self.scale_bin_b = tk.Scale(self.frame_slider, variable=self.thresh_b,
                               orient=tk.HORIZONTAL, from_=0, to=255, length=300, width=20)
        self.label_bin_r.pack()
        self.scale_bin_r.pack()
        self.label_bin_g.pack()
        self.scale_bin_g.pack()
        self.label_bin_b.pack()
        self.scale_bin_b.pack()
        self.frame_slider.pack()

    def open_file(self):
        path = tkinter.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg;*.png")])
        if path is None:
            return
        self.label_src_img["text"] = path
        self.img = cv2.imread(path)





if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
