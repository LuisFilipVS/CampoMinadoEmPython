from PyQt5.QtWidgets import  *
from PyQt5 import  QtGui
from PyQt5.QtCore import  *
import random

try:
    import eventFilterClass
    import eventFilterClass_ground
except:
    from src import eventFilterClass
    from src import eventFilterClass_ground

try:
    from widgets import number_widget
except:
    from src.widgets import number_widget

MODE_GROUND = {        
    "leaf_field" : ":/modes/assets/leaf_field.png",
    "leaf_flagged": ":/modes/assets/leaf_fieldFlagged.png",
    "ground_mode_1": ":/modes/assets/ground_mode_1.png",
    "ground_mode_2": ":/modes/assets/ground_mode_2.png",
    "ground_mode_3": ":/modes/assets/ground_mode_3.png",
    "number_1": ":/modes/assets/ground_number_1.png",
    "number_2": ":/modes/assets/ground_number_2.png",
    "number_3": ":/modes/assets/ground_number_3.png",
    "number_4": ":/modes/assets/ground_number_4.png",
    "number_5": ":/modes/assets/ground_number_5.png",
    "number_6": ":/modes/assets/ground_number_6.png",
    "number_7": ":/modes/assets/ground_number_7.png",
    "number_8": ":/modes/assets/ground_number_8.png"
}

class mineSlots():
    def __init__(self, xCoord, yCoord, parentE=None) -> None:
        self.neighbor: list[mineSlots] = []  
        self.isABomb = False
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.uiWidget = None
        self.widget = None
        
        #ui.flag_label.installEventFilter(e)
        
        try: 
            self.widget = QWidget()
            self.uiWidget = number_widget.Ui_Form()
            self.uiWidget.setupUi(self.widget)

            self.uiWidget.number_label.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

            self.parentE = parentE
            self.e = eventFilterClass_ground.eventFilterClass_ground(self.uiWidget,self.parentE,self)
            
            self.uiWidget.number_label.installEventFilter(self.e)

        except Exception as e:
            print(e)


    def set_modeSlot(self, mode):    
        pass

    def add_neighbor(self, neihgbor):
        self.neighbor.append(neihgbor)
        pass

    def set_isABomb(self,condition):
        self.isABomb = condition
        
    def get_isABomb(self):
        return self.isABomb
    
    def verify_neighbor_bomb(self):
        count_bombs = 0
        for i in self.neighbor:
            if i.get_isABomb() == True:
                count_bombs += 1
        #print(f"({self.xCoord}{self.yCoord}) tem {count_bombs} na vizinhança")
        
        if count_bombs == 0:
            randInt = random.randint(1,100)
            if randInt >= 90:
                img = MODE_GROUND["ground_mode_3"]
                self.uiWidget.number_label.setPixmap(QtGui.QPixmap(img))
            elif randInt >= 50:
                img = MODE_GROUND["ground_mode_2"]
                self.uiWidget.number_label.setPixmap(QtGui.QPixmap(img))
            else:
                img = MODE_GROUND["ground_mode_1"]
                self.uiWidget.number_label.setPixmap(QtGui.QPixmap(img))
            self.uiWidget.was_visited = True
            self.uiWidget.was_Clicked = True
            self.uiWidget.number_label.setCursor(QtGui.QCursor(Qt.ArrowCursor))

            for i in self.neighbor:
                if not i.uiWidget.was_visited:
                    i.verify_neighbor_bomb()
        else:
            #print(f"Slot ({self.xCoord}{self.yCoord}) tem {count_bombs} bombas na vizinhança")
            asset = "number_"+ str(count_bombs) 
            img = MODE_GROUND[asset]
            self.uiWidget.number_label.setCursor(QtGui.QCursor(Qt.ArrowCursor))
            self.uiWidget.number_label.setPixmap(QtGui.QPixmap(img))
            self.uiWidget.was_Clicked = True
            self.uiWidget.was_visited = True