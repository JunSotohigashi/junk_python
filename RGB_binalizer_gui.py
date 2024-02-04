import cv2
from matplotlib import pyplot as plt
import tkinter.filedialog


class Histgram:
    def __init__(self, ax, ch: str, img):
        self.threshold = 127
        self.ax: plt.Axes = ax

        self._hist_raw = cv2.calcHist(
            [img], [["b", "g", "r"].index(ch)], None, [256], [0, 256])
        self._hist_max = max(self._hist_raw)

        self.ax.plot(self._hist_raw, color=ch)
        self.ax.set_xlim([0, 255])
        self.ax.set_ylim(bottom=0)
        self.ax.set_xticks([0, 64, 128, 192, 255])
        self._vline = self.ax.axvline(self.threshold)

    def setThreshold(self, threshold):
        self.threshold = int(threshold)
        self._vline.set_xdata([self.threshold])
        plt.draw()


class HistEventHandler:
    def __init__(self, histgrams: list[Histgram]):
        self._picked = None
        self._histgrams = histgrams

    def on_press(self, event):
        if event.inaxes is None:
            return
        for histgram in self._histgrams:
            if event.inaxes is histgram.ax:
                self._picked = event.inaxes
                break

    def on_release(self, event):
        if event.inaxes is None:
            return
        self._picked = None

    def on_motion(self, event):
        if self._picked is not None and event.inaxes is self._picked:
            for histgram in self._histgrams:
                if event.inaxes is histgram.ax:
                    histgram.setThreshold(int(event.xdata))
                    break


def main():
    # 画像ファイルを開く
    img_path = tkinter.filedialog.askopenfilename(
        filetypes=[("画像ファイル", "*.jpg;*.png")])
    if img_path is None:
        return
    img = cv2.imread(img_path)

    # RGBヒストグラムの表示
    fig_hist = plt.figure()
    histgram = [Histgram(fig_hist.add_subplot(3, 1, i+1), ch, img)
                for i, ch in enumerate(["r", "g", "b"])]

    # ヒストグラムのクリックイベント取得
    handler = HistEventHandler(histgram)
    fig_hist.canvas.mpl_connect("button_press_event", handler.on_press)
    fig_hist.canvas.mpl_connect("button_release_event", handler.on_release)
    fig_hist.canvas.mpl_connect("motion_notify_event", handler.on_motion)

    fig_img = plt.figure()
    ax_img_raw = fig_img.add_subplot(3, 3, 1)
    ax_img_raw.imshow(img)

    img_b, img_g, img_r = cv2.split(img)
    ax_img_r = fig_img.add_subplot(3, 3, 4)
    ax_img_g = fig_img.add_subplot(3, 3, 5)
    ax_img_b = fig_img.add_subplot(3, 3, 6)
    ax_img_r.imshow(img_g, cmap = "gray")
    ax_img_g.imshow(img_b, cmap = "gray")
    ax_img_b.imshow(img_r, cmap = "gray")
    ax_img_r_bin = fig_img.add_subplot(3, 3, 7)
    ax_img_g_bin = fig_img.add_subplot(3, 3, 8)
    ax_img_b_bin = fig_img.add_subplot(3, 3, 9)
    _, img_r_bin = cv2.threshold(img_r, histgram[0].threshold, 255, cv2.THRESH_BINARY)
    _, img_g_bin = cv2.threshold(img_g, histgram[1].threshold, 255, cv2.THRESH_BINARY)
    _, img_b_bin = cv2.threshold(img_b, histgram[2].threshold, 255, cv2.THRESH_BINARY)
    ax_img_r_bin.imshow(img_r_bin, cmap = "gray")
    ax_img_g_bin.imshow(img_g_bin, cmap = "gray")
    ax_img_b_bin.imshow(img_b_bin, cmap = "gray")

    plt.show()


if __name__ == "__main__":
    main()
