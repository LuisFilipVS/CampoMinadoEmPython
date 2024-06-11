from PyQt5.QtWidgets import  *
from PyQt5 import  QtGui, QtCore
from PyQt5.QtCore import  *
import random



try:
    from mineSlots import mineSlots
except:
    from src.mineSlots import mineSlots
try:
    from widgets import modes_assets_rc
except:
    from src.widgets import modes_assets_rc
try:
    from mainWindow import Ui_MainWindow
except:
    from src.mainWindow import Ui_MainWindow
try:
    import eventFilterClass
except:
    from src import eventFilterClass


MODE_ITENS = {
    "digger_mode_1" : ":/itens/assets/digger_mode_1.png",
    "digger_mode_2" : ":/itens/assets/digger_mode_2.png",
    "flag_mode_2" : ":/itens/assets/flag_mode_2.png",
    "flag_mode_1" : ":/itens/assets/flag_mode_1.png"
}

MODE_GROUND = {        
    "leaf_field" : ":/modes/assets/leaf_field.png",
    "leaf_flagged": ":/modes/assets/leaf_fieldFlagged.png",
    "ground_mode_1": ":/modes/assets/ground_mode_1.png",
    "ground_mode_2": ":/modes/assets/ground_mode_2.png",
    "ground_mode_3": ":/modes/assets/ground_mode_3.png",
    "bomb": ":/modes/assets/bomb.png",
    "number_1": ":/modes/assets/ground_number_1.png",
    "number_2": ":/modes/assets/ground_number_2.png",
    "number_3": ":/modes/assets/ground_number_3.png",
    "number_4": ":/modes/assets/ground_number_4.png",
    "number_5": ":/modes/assets/ground_number_5.png",
    "number_6": ":/modes/assets/ground_number_6.png",
    "number_7": ":/modes/assets/ground_number_7.png",
    "number_8": ":/modes/assets/ground_number_8.png"

}


class MineField(QMainWindow):
    def __init__(self, field:int, bombs:int, window_frame:Ui_MainWindow=None, MainWindow=None):
        super(MineField, self).__init__()
        self.fieldSize = field
        self.bombs = bombs
        self.window_frame = window_frame
        self.fieldGame: list[list[mineSlots]] = []
        self.e = None
        self.MainWindow = MainWindow


        #Layout of GameSpace
        self.game_frame = self.window_frame.game_frame
        self.vertical_layout = QVBoxLayout(self.game_frame)
        self.vertical_layout.setContentsMargins(0,0,0,0)
        self.vertical_layout.setSpacing(0)

        self.window_frame.options_frame.setVisible(False)
        self.window_frame.InfoGame_label.setVisible(False)
        self.window_frame.label.setVisible(False)
        #self.gameController()

        #Configure the actions for click Buttons
        self.window_frame.initConf_pushButton.clicked.connect(self.show_options)
        self.window_frame.initGame_pushButton.clicked.connect(self.gameController)
        self.window_frame.exit_pushButton.clicked.connect(self.exitTheGame)
        pass
    
    #Caso o user faça o primeiro clique em slot que seja uma bomba, a bomba deve ser realocada
    def redefine_one_bomb(self, x, y):
            while True:
                new_x = random.randint(0,self.fieldSize-1)
                new_y = random.randint(0,self.fieldSize-1)
                self.fieldGame[x][y].set_isABomb(False)

                if (not(x == new_x and y == new_y)):
                    if (self.fieldGame[new_x][new_y].get_isABomb() == False):
                        self.fieldGame[new_x][new_y].set_isABomb(True)
                        break
            self.show_terminalBombs()
            
        
    def define_the_eventClicks(self):
        self.e = eventFilterClass.eventFilterClass(self.window_frame, self)
        self.window_frame.flag_label.installEventFilter(self.e)
        self.window_frame.digger_label.installEventFilter(self.e)
        
        pass

    def show_options(self):
        self.window_frame.options_frame.setVisible(True)
        self.window_frame.fieldConf_lineEdit.setReadOnly(False)
        self.window_frame.fieldConf_lineEdit.setText("")
        self.window_frame.bombsConf_lineEdit.setReadOnly(False)
        self.window_frame.bombsConf_lineEdit.setText("")
        self.window_frame.initGame_pushButton.setVisible(True)
        self.window_frame.label.setText("")
        pass

    def clearTheFieldGame(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearTheFieldGame(item.layout())

        self.fieldGame.clear()

        pass

    def gameController(self):
        self.clearTheFieldGame(self.vertical_layout)
        self.window_frame.InfoGame_label.setVisible(False)

        #Verify if exists data in lineEdit
        wrongData = False
        if self.window_frame.fieldConf_lineEdit.text() != '':
            newField = int(self.window_frame.fieldConf_lineEdit.text())
            if newField > 5 and newField < 15:
                self.fieldSize = newField
            else:
                wrongData = True
        if self.window_frame.bombsConf_lineEdit.text() != '':
            newBombs = int((self.window_frame.bombsConf_lineEdit.text()))
            if newBombs > 0 and newBombs < self.fieldSize ** 2:
                self.bombs = newBombs
            else:
                wrongData = True
        
        if wrongData:
            self.window_frame.label.setVisible(True)
            self.window_frame.label.setText("Erro ao adicionar algum dado.\n\nCampo definido com\nbase nos dados corretos!")
            self.window_frame.label.setStyleSheet("#label{color:#fff}")

        #hide and block config itens
        self.window_frame.fieldConf_lineEdit.setReadOnly(True)
        self.window_frame.fieldConf_lineEdit.setText(str(self.fieldSize))
        self.window_frame.bombsConf_lineEdit.setReadOnly(True)
        self.window_frame.bombsConf_lineEdit.setText(str(self.bombs))
        self.window_frame.initGame_pushButton.setVisible(False)
        
        #Init the game
        self.define_the_eventClicks()
        self.createField()
        self.setNeighbor()
        self.define_the_bombs()
        self.renderFields()
        self.recalculeBombsSelected()
        #self.show_bombs()
        pass

    def exitTheGame(self):
        self.MainWindow.close()

    def countBombsSelected(self):
        bombasSelecionadas = 0
        for i in range(0, self.fieldSize):
            for k in range(0, self.fieldSize):
                if self.fieldGame[i][k].uiWidget.was_ClickedAsFlag:
                    bombasSelecionadas += 1
        return bombasSelecionadas

    def recalculeBombsSelected(self):
        bombasSelecionadas  = self.countBombsSelected()
        self.window_frame.CountBomb_label.setText(str(self.bombs -  bombasSelecionadas))
        pass
    
    #verify if there no click leafs fields
    def verifyGameStatus(self) -> bool:
        status = False
        x = 0
        for i in range(0, self.fieldSize):
            for k in range(0, self.fieldSize):
                if not (self.fieldGame[i][k].get_isABomb()) and not (self.fieldGame[i][k].uiWidget.was_visited):
                    status = True
                    x += 1        
        print(f"Restam {x} espaços")
        if not status:
            self.finishTheGame(True)
        return status


    #Finish the round
    def finishTheGame(self, status):
        if status:
            print("Parabens, você VENCEU o jogo! Aproveite e jogue mais uma!!")
            self.window_frame.InfoGame_label.setVisible(True)
            self.window_frame.InfoGame_label.setText("VOCÊ\nGANHOU!!")
            self.window_frame.InfoGame_label.setStyleSheet("#InfoGame_label{color:green}")
        else:
            print("Você PERDEU o jogo! Aproveite e jogue mais uma!!")
            self.show_bombs()
            for i in range(0, self.fieldSize):
                for k in range(0, self.fieldSize):
                    self.fieldGame[i][k].e.active = False

            self.window_frame.InfoGame_label.setVisible(True)
            self.window_frame.InfoGame_label.setText("VOCÊ\nPERDEU:(")
            self.window_frame.InfoGame_label.setStyleSheet("#InfoGame_label{color:red}")

        self.show_options()
        
    def define_the_bombs(self):
        for i in range(0,self.bombs):
            while True:
                x = random.randint(0,self.fieldSize-1)
                y = random.randint(0,self.fieldSize-1)
                if (self.fieldGame[x][y].get_isABomb() == False):
                    self.fieldGame[x][y].set_isABomb(True)
                    self.fieldGame[x][y].uiWidget.isABomb = True

                    break
        #self.show_terminalBombs()

    def show_terminalBombs(self):
        for i in range(0, self.fieldSize):
            for k in range(0, self.fieldSize):
                if self.fieldGame[i][k].get_isABomb() == True:
                    print(f"[{i}][{k}]")
        
    def alter_mode_icon(self, widget:QLabel, mode:str) -> None:
        try:
            widget.setPixmap(QtGui.Qpixmap(MODE_ITENS[mode]))
        except Exception as e:
            print(f"Erro ao alterar a imagem do widget: {e}")
            

    def renderFields(self):
        
        h_slot = int(self.game_frame.size().height()/self.fieldSize)
        w_slot = int(self.game_frame.size().height()/self.fieldSize)
        
        '''
        self.vertical_layout = QVBoxLayout(self.game_frame)
        self.vertical_layout.setContentsMargins(0,0,0,0)
        self.vertical_layout.setSpacing(0)
        '''

        for k in range(0,self.fieldSize):
            line_frame = QFrame(self.game_frame)
            horizontal_layout = QHBoxLayout(line_frame)
            horizontal_layout.setContentsMargins(0,0,0,0)
            horizontal_layout.setSpacing(0)
            for i in range(0,self.fieldSize):
                slot:QWidget = self.fieldGame[k][i].widget
                slot.size().setHeight(h_slot)
                slot.size().setWidth(w_slot)
                slot.setMinimumSize(40,h_slot)
                horizontal_layout.addWidget(slot)
            self.vertical_layout.addWidget(line_frame)

        spacer = QSpacerItem(20,10000,QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacer)
        
    def createField(self):    
        for i in range(0,self.fieldSize):
            line = []
            for k in range(0,self.fieldSize):
                line.append(mineSlots(i,k,self.e))
            self.fieldGame.append(line)

    def show_bombs(self):
        for i in range(0,self.fieldSize):
            for k in range(0, self.fieldSize):
                if self.fieldGame[i][k].get_isABomb():
                    self.fieldGame[i][k].uiWidget.number_label.setPixmap(QtGui.QPixmap(MODE_GROUND["bomb"]))
                    self.fieldGame[i][k].uiWidget.number_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    
    def setNeighbor(self):
        for i in range(0,self.fieldSize):
            for k in range(0, self.fieldSize):
                if(i == 0 and k == 0): #Linha 0 e coluna 0 - 3 Vizinhos
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k+1])
                if(i == 0 and k>0 and k < self.fieldSize-1): #Linha 0, e coluna > 0 e < size-1 (5 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k+1])
                if(i == 0 and k==self.fieldSize-1): #Linha 0, e Coluna Size-1 (3 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k-1])
                
                if((i>0 and i<self.fieldSize-1) and k==0): #Linha>0 e Linha<Size-1; Coluna 0 (5 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                if((i>0 and i<self.fieldSize-1) and (k>0 and k<self.fieldSize-1)): #Linha>0 e Linha<Size-1; Coluna > 0 e < Size-1 (8 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                if((i>0 and i<self.fieldSize-1) and k==self.fieldSize-1): #Linha>0 e Linha<Size-1; Coluna Size-1 (5 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i+1][k-1])

                if(i == self.fieldSize-1 and k == 0): #Linha Size-1 e coluna 0 - 3 Vizinhos
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                if(i == self.fieldSize-1 and k>0 and k < self.fieldSize-1): #Linha Size-1, e coluna > 0 e < size-1 (5 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k+1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k+1])
                if(i == self.fieldSize-1 and k==self.fieldSize-1): #Linha Size-1, e Coluna Size-1 (3 Vizinhos)
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i][k-1])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k])
                    self.fieldGame[i][k].add_neighbor(self.fieldGame[i-1][k-1])
                        
        pass

if __name__ == "__main__":
    '''fieldGame = MineField(4,6)
    fieldGame.createField()
    fieldGame.setNeighbor()
    z = 0
    for i in fieldGame.fieldGame[3][3].neighbor:
        print(f"x{i.xCoord},y{i.yCoord}")
        ''for k in i:
            print(f"x{k.xCoord},y{k.yCoord}")
            z += 1
        ''
        z += 1
    print(z)
    '''
    import sys
    import minefield,mainWindow

    app = QApplication(sys.argv)
    
    MainWindow = QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    
    #Config the action by use mouse
    ui.flag_label.installEventFilter(MainWindow)
    game = minefield.MineField(8,6,ui)
    

    MainWindow.show()
    

 
    sys.exit(app.exec_())


    pass