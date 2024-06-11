from PyQt5 import QtCore, QtGui, QtWidgets
try:
    import mainWindow
except:
    from src import mainWindow
try:
    import minefield
except:
    from src import minefield

MODE_ITENS = {
    "digger_mode_1" : ":/itens/assets/digger_mode_1.png",
    "digger_mode_2" : ":/itens/assets/digger_mode_2.png",
    "digger_mode_3" : ":/itens/assets/digger_mode_3.png",
    "flag_mode_2" : ":/itens/assets/flag_mode_2.png",
    "flag_mode_1" : ":/itens/assets/flag_mode_1.png",
    "flag_mode_3" : ":/itens/assets/flag_mode_3.png",
}

MODE_GROUND = {        
    "leaf_field" : ":/modes/assets/leaf_field.png",
    "leaf_flagged": ":/modes/assets/leaf_fieldFlagged.png",
    "ground_mode_1": ":/modes/assets/ground_mode_1.png",
    "ground_mode_2": ":/modes/assets/ground_mode_2.png",
    "ground_mode_3": ":/modes/assets/ground_mode_3.png",

}

class eventFilterClass(QtCore.QObject):
    def __init__(self, window:mainWindow.Ui_MainWindow=None, parentGame=None):
        super(eventFilterClass, self).__init__()
        self.icon_selected:QtWidgets.QLabel = None
        self.digger_img_default:str  = MODE_ITENS["digger_mode_1"]
        self.flag_img_default:str = MODE_ITENS["flag_mode_1"]
        self.window = window
        self.parentGame = parentGame
        self.first_click = True

    def eventFilter(self,obj:QtWidgets.QLabel,event):
        if event.type() == QtCore.QEvent.Enter and obj.objectName() == 'flag_label':
            img = MODE_ITENS["flag_mode_2"]
            obj.setPixmap(QtGui.QPixmap(img))
            return True

        elif event.type() == QtCore.QEvent.Leave and obj.objectName() == 'flag_label':
            #img = MODE_ITENS["flag_mode_1"]
            img = self.flag_img_default
            obj.setPixmap(QtGui.QPixmap(img))
            return True
        
        elif event.type() == QtCore.QEvent.Enter and obj.objectName() == 'digger_label':
            img = MODE_ITENS["digger_mode_2"]
            obj.setPixmap(QtGui.QPixmap(img))
            return True

        elif event.type() == QtCore.QEvent.Leave and obj.objectName() == 'digger_label':
            #img = MODE_ITENS["digger_mode_1"]
            img = self.digger_img_default
            obj.setPixmap(QtGui.QPixmap(img))
            return True
        
        elif event.type() == QtCore.QEvent.MouseButtonPress and obj.objectName() == 'digger_label':
            img = MODE_ITENS["digger_mode_3"]
            if self.icon_selected is None:
                self.icon_selected = obj
                self.digger_img_default = MODE_ITENS["digger_mode_3"]
                obj.setPixmap(QtGui.QPixmap(img))
                return True
            elif self.icon_selected != obj:
                self.icon_selected.setPixmap(QtGui.QPixmap(MODE_ITENS["flag_mode_1"]))
                obj.setPixmap(QtGui.QPixmap(MODE_ITENS["digger_mode_3"]))
                self.digger_img_default = MODE_ITENS["digger_mode_3"]
                self.flag_img_default = MODE_ITENS["flag_mode_1"]
                self.icon_selected = obj
                return True     
            else:
                return True
        
        elif event.type() == QtCore.QEvent.MouseButtonPress and obj.objectName() == 'flag_label':
            img = MODE_ITENS["flag_mode_3"]
            if self.icon_selected is None:
                self.icon_selected = obj
                self.flag_img_default = MODE_ITENS["flag_mode_3"]
                obj.setPixmap(QtGui.QPixmap(img))
                
                return True
            elif self.icon_selected != obj:
                self.icon_selected.setPixmap(QtGui.QPixmap(MODE_ITENS["digger_mode_1"]))
                obj.setPixmap(QtGui.QPixmap(MODE_ITENS["flag_mode_3"]))
                self.flag_img_default = MODE_ITENS["flag_mode_3"]
                self.digger_img_default = MODE_ITENS["digger_mode_1"]
                self.icon_selected = obj    
                return True    
            else:
                return True
        
        return False
    
    def set_first_click(self,condition: bool):
        self.first_click = False
        

    def get_first_click(self):
        return self.first_click
    
    def recalcule_the_first_bomb(self,x,y):
        self.parentGame.redefine_one_bomb(x,y)
    pass

