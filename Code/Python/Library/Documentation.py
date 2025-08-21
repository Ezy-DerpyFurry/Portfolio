# These skip the intro/introduction in terminal
import os
os.environ["SKIP_INTRO"] = "1"

# This is the importer you can also import certain classes so the entire library doesn't need to load.
from Library import glib
#from Library.glib import Extras # <== This is the Extras class

# If you're just importing the entire library you can name them like this.
music = glib.Music()
extras = glib.Extras()
Math = glib.Math()
file = glib.File()
video = glib.Video()

# If you just wanna use a single function as a base function you can do
wait = extras.wait 
# Then you can do
wait(2) # instead of extras.wait(2)

# These are the arguments you can change for the entirty of the code they can all be handled hear and can be updated as you please.
glib.update_arguments({
    'music': {
        'volume': 0.5,
        'pause': False, # Seems dumb but incase you wanna pause by default.
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

extras.wait(1) # This waits a certain amount of seconds like. (it does support foats [ex. 0.4])

extras.keep_alive(True) # Will keep your code alive even if it all ends it will just keep it running
extras.keep_alive(False) # Disables the keep alive

print(extras.contains("abc123", "c12")) # Sees if a string contains another string (value), the first argument is the string, the 2nd argument is the value you want to find

# My thread wrapper (this is a bigger one)

def monitor(str, str2):
    extras.print(str)
    wait(2)
    extras.print(str2)
    extras.wait(5)
    print(str)
    extras.wait(2)

extras.sthread(monitor, "Hi", "test", a=True) 
# The first argument is the function you're targeting, the next arguments will all be arguments you put into the function.
# You have to do a=True for the daemon toggle, True means it will stop the function when your code stops, False will mean it will keep your code going till it stops.

### MUSIC ###

# Suports multiple music players

player1 = music.play(r"path to mp3.mp3") # This intializes a .mp3 player, default volume in the arguments
player1 = music.play(r"path to mp3.mp3").play() # This plays it when initalized (just starts playing)

player1.play() # This actually plays the player
player1.pause() # Pauses player
player1.unpause() # Unpauses player
player1.toggle() # Toggles pause and unpause player
player1.stop() # Deletes/Breaks the player
player1.set_volume(0.2) # This sets the volume of it 

glib.update_arguments({'music': {'volume': 1},}) # Another way to set sound aswell

music.download(url = 'url here', format = "mp3", out = "output path here") # This downloads a mp3 from a website that yt_dlp supports and puts it into the file you want (Mostly a wrapper)
music.download(url = 'url here', format = "mp4", out = "output path here") # This downloads a mp4 from a website that yt_dlp supports and puts it into the file you want (Mostly a wrapper)

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

### FILE ###

file.removefile(b"path to file.file-extension") # This deleted a file for you, you just have to put in the path

print(file.filecount("folder path here")) # This returns how many FILES are in a folder so it will not include folders inside another folder.

### VIDEO ###

player1 = video.play(r"path to mp4") # Creates a player in the value player1

player1.pause() # Pauses the player
player1.resume() # Unpauses the player
player1.play() # Plays the player
player1.set_volume(50) # Sets volume 1-100
player1.stop() # Destroys/stops the player
timestamp = player1.get_position() # Gets the timestamp
player1.set_position(120) # Sets a new timestamp in seconds (can start video at the end)




