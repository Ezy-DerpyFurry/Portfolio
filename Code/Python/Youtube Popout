### Just a quick note this was partly made by Chat-GPT as I am also still learning python libraries.

import tkinter as tk
from tkinter import ttk
import vlc
import yt_dlp

def get_stream_url(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict['url']

def play_video():
    video_url = entry.get()
    stream_url = get_stream_url(video_url)
    player.set_mrl(stream_url)
    player.play()

root = tk.Tk()
root.title("Youtube Popout")
root.geometry("800x600")
root.attributes('-topmost', True)

entry = ttk.Entry(root, width=80)
entry.pack(pady=10)
entry.insert(0, "Youtube link here.")

btn = ttk.Button(root, text="Play", command=play_video)
btn.pack()

instance = vlc.Instance()
player = instance.media_player_new()

video_frame = tk.Frame(root)
video_frame.pack(fill="both", expand=True)
player.set_xwindow(video_frame.winfo_id())

root.mainloop()
