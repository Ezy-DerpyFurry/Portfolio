import terminalui
import threading

options = {
    "Button 1": "  This is an example hover for button 1",
    "Button 2": "  This is an example hover for button 2",
    "Button 3": "  This is an example hover for button 3"
}
buttons = {
    "Button A": "  This is an example hover for button A",
    "Button B": "  This is an example hover for button B",
    "Button C": "  This is an example hover for button C"
}
print(terminalui.createButtons(buttons, "These are buttons"))
print(terminalui.createSelector(options, "This is a selector", " >> "))
print(terminalui.createSlider(0, 20, "This is the slider"))

terminalui.startInput()

try: 
    while True:
        keyAscii = terminalui.getKey(True)
        if keyAscii is not None:
            if keyAscii == 113 or keyAscii == 'q':
                terminalui.stopInput()
                break
            print(f"Key pressed: {keyAscii}")
except:
    terminalui.stopInput()
