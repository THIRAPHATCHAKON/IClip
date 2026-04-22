import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import yt_dlp
import threading

FFMPEG_PATH = r"FFMPEG_PATH"

class Download_Clip:
    @staticmethod
    def download_mp4(url):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'ffmpeg_location': FFMPEG_PATH,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("ดาวน์โหลด MP4 สำเร็จ!")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")

    @staticmethod
    def download_mp3(url):
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'ffmpeg_location': FFMPEG_PATH,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("ดาวน์โหลด MP3 สำเร็จ!")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")


class ConverterFrame(ttk.Frame):
    def __init__(self, container, unit_from, converter):
        super().__init__(container)

        self.unit_from = unit_from
        self.converter = converter

        # field options
        options = {'padx': 5, 'pady': 0}

        # temperature entry
        self.url = tk.StringVar()
        self.url_entry = ttk.Entry(self, textvariable=self.url)
        self.url_entry.grid(column=1, row=0, sticky='w', **options)
        self.url_entry.focus()

        # button
        self.convert_button = ttk.Button(self, text='Convert')
        self.convert_button.grid(column=2, row=0, sticky='w', **options)
        self.convert_button.configure(command=self.convert)

        self.result_label = ttk.Label(self)
        self.result_label.grid(row=1, columnspan=3, padx=5)
        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def convert(self, event=None):
        """  Handle button click event
        """
        try:
            input_value = self.url.get()
            result = self.converter(input_value)
            self.result_label.config(text=result)
        except ValueError as error:
            showerror(title='Error', message=error)

    def reset(self): 
        self.url_entry.delete(0, "end")
        self.result_label.text = ''


class ControlFrame(ttk.LabelFrame):
    def __init__(self, container):

        super().__init__(container)
        self['text'] = 'Options'

        # radio buttons
        self.selected_value = tk.IntVar()

        ttk.Radiobutton(
            self,
            text='MP3',
            value=0,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0, row=0, padx=5, pady=5)

        ttk.Radiobutton(
            self,
            text='MP4',
            value=1,
            variable=self.selected_value,
            command=self.change_frame).grid(column=1, row=0, padx=5, pady=5)

        self.grid(column=0, row=1, padx=5, pady=5, sticky='ew')

        # initialize frames
        self.frames = {}
        self.frames[0] = ConverterFrame(
            container,
            'MP3',
            Download_Clip.download_mp3)
        self.frames[1] = ConverterFrame(
            container,
            'MP4',
            Download_Clip.download_mp4)

        self.change_frame()

    def change_frame(self):
        frame = self.frames[self.selected_value.get()]
        frame.reset()
        frame.tkraise()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

    
        self.title('IClip')
        self.geometry('300x120')
        self.resizable(False, False)
        try:
            photo = tk.PhotoImage(file='D:\IClip\img\C.png') #.png or .gif
            self.iconphoto(False, photo)
        except tk.TclError:
            pass


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
