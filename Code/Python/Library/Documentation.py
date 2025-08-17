# These skip the intro/introduction in terminal
import os
os.environ["SKIP_INTRO"] = "1"

# This is the importer you can also import certain classes so the entire library doesn't need to load.
from Library import glib
#from Library.glib import Extras # <== This is the Extras class

# if you're just importing the entire library you can name them like this.
music = glib.Music()
extras = glib.Extras()
Math = glib.Math()

# These are the arguments you can change for the entirty of the code they can all be handled hear and can be updated as you please.
glib.update_arguments({
    'music': {
        'volume': 0.5,
    },
    'debugging': {
        'extras': True,
        'warning': False,
        'error': True
    },
    'debug': False, # I am slowly replacing this with the debugging category but its here incase I missed any
    'intro': True # Do not use this unless you really want to it does infact do nothing and is a placeholder for the library itself
})

### EXTRAS ###

extras.wait(1) # This waits a certain amount of seconds like. (it does support foats [ex. 0.4)

### MUSIC ###

music.play(r"path to mp3.mp3") # This plays a .mp3 volume is handled about in the arguments

music.removefile(b"path to file.file-extension") # This deleted a file for you, you just have to put in the path

music.download(url = 'url here', format = "mp3", out = "output folder here") # This downloads a mp3 from a website that yt_dlp supportsand puts it into the file you want (Mostly a wrapper)
music.download(url = 'url here', format = "mp4", out = "output folder here") # This downloads a mp4 from a website that yt_dlp supportsand puts it into the file you want (Mostly a wrapper)

### MATH ###

# The random function can be called in two ways and returns the number.

math_example1 = Math.random(10,20) # This one relys on the Math = glib.Math()
math_example2 = glib.Math.random(glib.Math(), 10,20)  # This does not rely on the Math = glib.Math() but relys on you importing the entire library at once.

# My special toint it handles alot for you read the about for more info on this.

math_example3 = Math.toint(v=None, returns="int", f=False)
"""
{v} is the value you wanna convert
{returns} has str and int for strings or integer returning
{f} is if you wanna floatify it (False by default)
"""



