import yt_dlp
import ctypes
from yt_dlp.utils import DownloadError
import threading
import os
import warnings
import vlc

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["PYGAME_DETECT_AVX2"] = "1"

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore")

import pygame

# Load C++ functions
function = ctypes.CDLL("Library/functions/funcs.so") # If you use a IDE that supports relative paths, this should work otherwise please replace the full path. 

function.sleep.argtypes = [ctypes.c_double]
function.sleep.restype = None
function.delete_file.argtypes = [ctypes.c_char_p]
function.delete_file.restype = None
function.randomsong.restype = ctypes.c_char_p
function.set_intro.argtypes = [ctypes.c_bool]
function.set_intro.restype = None
function.get_intro_state.restype = ctypes.c_bool
function.to_int_converted.argtypes = [ctypes.c_char_p]
function.to_int_converted.restype = ctypes.c_double
function.defloat_int_c.argtypes = [ctypes.c_char_p]
function.defloat_int_c.restype = ctypes.c_int
function.defloat_int_double.argtypes = [ctypes.c_double]
function.defloat_int_double.restype = ctypes.c_int
function.filecount.argtypes = [ctypes.c_char_p]
function.filecount.restype = ctypes.c_int
function.contains_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
function.contains_c.restype = ctypes.c_bool
function.circlearea.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_int]
function.circlearea.restype = ctypes.c_double

debug_var = ctypes.c_bool.in_dll(function, "debug")
animate_var = ctypes.c_bool.in_dll(function, "animate")

# Default arguments
args = {
    'music': {
        'volume': 0.5,
        'pause': False,
    },
    'debugging': {
        'extras': True,
        'warning': False,
        'error': True
    },
    'debug': False,
    'intro': True
}

def update_arguments(nw_args: dict):
    for key, val in nw_args.items():
        if isinstance(val, dict) and key in args and isinstance(args[key], dict):
            args[key].update(val)
        else:
            args[key] = val

if os.environ.get("SKIP_INTRO") == "1":
    args['intro'] = False

def intro():
    if args['intro']:
        print("This is made by Ezy its just a general wrapper library. \nOther Libraries used: \n *yt_dlp, pygame, threading, ctypes, and a few others...")

class Video:
    def __init__(self):
        self.path = r"temp"
        self._player = None

    class Player:
        def __init__(self, path: str):
            self._instance = vlc.Instance()
            self._player = self._instance.media_player_new()
            self._media = self._instance.media_new(path)
            self._player.set_media(self._media)
            self._running = False
            self._paused = False
            self._volume = 50

        def play(self):
            def Video_Monitor():
                self._running = True
                self._player.play()
                Extras.wait(0.2)
                while self._running and self._player.is_playing():
                    Extras.wait(0.1)
            Extras().sthread(Video_Monitor)

        def pause(self):
            self._player.pause()

        def resume(self):
            self._player.play()

        def stop(self):
            self._running = False
            self._player.stop()

        def set_volume(self, vol: int):
            self._player.audio_set_volume(vol)

        def get_position(self):
            return self._player.get_time() / 1000

        def set_position(self, seconds: int):
            self._player.set_time(int(seconds * 1000))

    def play(self, path):
        self._player = self.Player(path)
        self._running = True
        return self._player

#class Keys:
       

class Math:
    class Numify:
        def __init__(self, value: int = 0):
            self._value = value

        def numify(self, num: int = None):
            if num is None:
                if args['debugging']['extras']:
                    print("No number specified")
                self._value = 0
            else:
                self._value = num
            return self

        def random(self, min_: int = 1, max_: int = 2):
            randomized = (self._value * Math().random(min_, max_))
            return Math.Numify(randomized)

        def clamp(self, min_: int = 1, max_: int = 2):
            clamped = Math().clamp(self._value, min_, max_)
            return Math.Numify(clamped)

        def circlearea(self, type: str, type2: str = "circle"):
            circlearea_ = Math().circlearea(self._value, type, type2)
            return Math.Numify(circlearea_)

        def __repr__(self):
            return str(self._value)

        def __int__(self):
            return int(self._value)

        def __float__(self):
            return float(self._value)

    def numify(self, num: int = None):
        return Math.Numify(num if num is not None else 0)

    def random(self, min: int = 1, max: int = 2):
        return function.mrandom(min, max)

    def circlearea(self, v: float, type: str, type2: str = "circle"):
        if not v or not type:
            if args['debugging']['extras']:
                print("No diameter or type set")
                return

        if type2 == 'sphere': va_ = 1
        if type2 == 'circle': va_ = 0

        values = {
            'diameter': function.circlearea(v, 1, va_),
            'radius': function.circlearea(v, 0, va_),
            'both': 0.0
        }
        values['both'] = f"{values['diameter']}, {values['radius']}"

        try:
            return values[type]
        except Exception as e:
            if args['debugging']['error']:
                print(f"ERROR: {e}")
            return 0.0
    
    def toint(self, v=None, returns="int", f=False):
        if not v:
            if args['debugging']['extras']:
                rint("No value entered.")
            return
        
        encoded = str(v).encode("utf-8")
        value = function.defloat_int_double(function.to_int_converted(encoded)) 

        if f:
            value = f"{value}.0"

        if returns == "str":
            return str(value)
        return value

    def clamp(self, value, min_value, max_value):
        return max(min_value, min(value, max_value))

class Extras:
    def __init__(self):
        self._keep_alive = False

    def sthread(self, func=None, *f_args, a=False, **kwargs):
        if not func:
            if args['debug']:
                print("Warning: No function mentioned")
            return
        threading.Thread(target=func, args=f_args, kwargs=kwargs, daemon=a).start()
    
    def keep_alive(self, on: bool = True):
        if on:
            self._keep_alive = True
        else:
            self._keep_alive = False

        def keep_alive_monitor():
            while self._keep_alive:
                if args['debug']:
                    print("Keeping alive...")
                self.wait()
        
        self.sthread(keep_alive_monitor, a=False)

    def wait(self, time: float = 1.0):
        function.sleep(time)

    def contains(self, string: str = None, value: str = None):
        return function.contains_c(string.encode('utf-8'), value.encode('utf-8'))

class File:
    def removefile(self, path: str = None):
        if not path:
            if args['debugging']['extras']:
                print("Warning: No path set please set a path.")
            return
        function.delete_file(path)

    def filecount(self, path: str = None):
        if not path:
            if args['debugging']['extras']:
                parint("Warning: No path set please set a path")
            return
        return function.filecount(path.encode('utf-8'))


class Music:
    def __init__(self):
        self.path = r"temp"
        pygame.mixer.init()

    class LogControl:
        def debug(self, msg):
            if args['debug'] or args['debugging']['extras']:
                print(msg)

        def warning(self, msg):
            if args['debugging']['warning']:
                print(msg)

        def error(self, msg):
            if args['debugging']['error']:   
                print(f"AN ERROR HAS OCCURED: {msg}")

    ### PLAYER ###

    class Player:
        def __init__(self, path=None):
            if not path and args['debugging']['extras']: 
                print("No path set")
                return
            self._paused = args['music']['pause']
            self._volume = args['music']['volume']
            self._path = path
            self._running = False

            self._channel = None
            self._sound = pygame.mixer.Sound(path)
        

        def play(self, loops=0):
            self._channel = self._sound.play(loops=loops)
            self._channel.set_volume(self._volume)
            self._running = True

            Extras().sthread(self.music_monitor, a=False)  
            return self

        def music_monitor(self):
            while self._running:
                if self._paused:
                    self._channel.pause()
                else:
                    self._channel.unpause()

                if not self._channel.get_busy() and not self._paused:
                    if args['debug']:
                        print(f"Song Done: {self._path}")
                    self._running = False
                    break
                
                Extras.wait(1)  

        # Player Commands

        def pause(self):
            self._paused = True

        def unpause(self):
            self._paused = False
        
        def toggle(self):
            self._paused = not self._paused

        def stop(self):
            self._running = False
            if self._channel:
                self._channel.stop()

        def set_volume(self, vol: float):
            self._volume = max(0.0, min(vol, 1.0))
            if self._channel:
                self._channel.set_volume(self._volume)

    def play(self, path: str):
        return self.Player(path)

    ### R_song

    def randomsong(self):
        return function.randomsong().decode("utf-8")


    ### Downloading

    def download(self, url: str = None, format: str = "mp4", out: str = None):
        if not url:
            print("No url set please set a url.")
            return

        if out is None:
            out = self.path

        def downloadinganim(action=True):
            if action:
                animate_var.value = True
                Extras().sthread(function.downloadanim)
            else:
                animate_var.value = False

        # Downloading formats

        if format == "mp3":
            ydl_opts = {
                'logger': self.LogControl(),
                'cookiesfrombrowser': ('chrome',),
                'format': 'bestaudio/best',
                'outtmpl': out + '/%(title)s.%(ext)s',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ]
            }
        elif format == "mp4":
            ydl_opts = {
                'logger': self.LogControl(),
                'outtmpl': out + '/%(title)s.%(ext)s',
            }
        else:
            print("Unsupported format")
            return

        def download_monitor():
            try:
                Extras().sthread(downloadinganim)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    Extras().sthread(downloadinganim, False)
            except DownloadError as e:
                print(f"Error downloading video: {e}")
            except Exception as e:
                print(f"An error has occurred: {e}")
        Extras().sthread(download_monitor, a=False)

# Starting Lines vv

intro()

### Testing Code Direction ###

"""print(function.defloat_int_c("16.0".encode("utf-8")))  # 16
print(function.defloat_int_c("123.45".encode("utf-8")))  # 123

print(function.defloat_int_double(14.2))  # 14
print(function.defloat_int_double(99.99))  # 99
"""
