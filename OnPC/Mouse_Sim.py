from Xlib import display

class Mouse_Sim:
    def __init__(self):
        data = display.Display().screen().root.query_pointer()._data


    def getPointer(self):
        data = display.Display().screen().root.query_pointer()._data
        return data["root_x"], data["root_y"]
    