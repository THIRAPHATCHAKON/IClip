import tkinter as tk
from tkinter import ttk
import yt_dlp

def Download(ydl_opts):    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url.get()])
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        
def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"⬇️ {d['_percent_str']} - {d['_speed_str']}")
    if d['status'] == 'finished':
        print("✅ ดาวน์โหลดเสร็จ!")

def delete_text(url):
    url.delete(0, tk.END)
    
root = tk.Tk()
root.title('IClip')

window_width = 500
window_height = 500

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

try:
    photo = tk.PhotoImage(file='D:\IClip\img\C.png') #.png or .gif
    root.iconphoto(False, photo)
except tk.TclError:
    pass

url = ttk.Entry(root)
url.pack()

ydl_opts = {
    'progress_hooks': [progress_hook],
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
}

# exit button
download_button = ttk.Button(
    root,
    text='Download',
    command=lambda: (Download(ydl_opts), delete_text(url))
)

download_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)


root.mainloop()