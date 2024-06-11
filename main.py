from src import minefield,mainWindow,eventFilterClass
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    game = minefield.MineField(10,15,ui,MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
