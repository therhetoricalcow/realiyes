import PupilFit
import PupilStream
from PyQt5 import QtWidgets
class PupilGui:
    def __init__(self):
        self.streamObject = PupilStream.PupilStream()
        self.streamObject.start()
        self.app = QtWidgets.QApplication([])
        self.widget = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout


PupilGui()


