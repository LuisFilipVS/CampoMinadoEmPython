from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from widgets import number_widget
    import eventFilterClass, mineSlots
except:
    from src.widgets import number_widget
    from src import eventFilterClass, mineSlots


MODE_GROUND = {        
    "leaf_field" : ":/modes/assets/leaf_field.png",
    "leaf_flagged": ":/modes/assets/leaf_fieldFlagged.png",
    "ground_mode_1": ":/modes/assets/ground_mode_1.png",
    "ground_mode_2": ":/modes/assets/ground_mode_2.png",
    "ground_mode_3": ":/modes/assets/ground_mode_3.png",

}

class eventFilterClass_ground(QtCore.QObject):
    def __init__(self, widget:number_widget.Ui_Form=None, eventFilterParent:eventFilterClass.eventFilterClass=None, slot_Field=None):
        super(eventFilterClass_ground, self).__init__()
        self.widget = widget
        self.eventFilterParent = eventFilterParent
        self.slot_Field = slot_Field
        self.active = True

    def eventFilter(self,obj:QtWidgets.QLabel,event):
        if self.active:
            if self.eventFilterParent.icon_selected is None or self.widget.was_Clicked or (self.eventFilterParent.icon_selected.objectName() == 'flag_label' and not(self.eventFilterParent.parentGame.bombs - self.eventFilterParent.parentGame.countBombsSelected()) > 0):
                return False
            elif event.type() == QtCore.QEvent.MouseButtonPress and self.eventFilterParent is not None and self.eventFilterParent.icon_selected.objectName() == 'digger_label' and self.eventFilterParent.first_click and self.widget.isABomb:
                self.eventFilterParent.first_click = False
                self.recalcule_the_first_bomb()
                return True
    
            else:
                if event.type() == QtCore.QEvent.MouseButtonPress and self.eventFilterParent is not None and self.eventFilterParent.icon_selected.objectName() == 'digger_label':
                    self.eventFilterParent.first_click = False
                    if self.widget.isABomb:
                        self.eventFilterParent.parentGame.finishTheGame(False)
                        return True
                    elif not self.widget.was_Clicked:  
                        #print("Já fui clickado!")
                        #print(self.eventFilterParent.icon_selected.objectName())
                        self.call_neighbor()
                    else:
                        return False
                    self.widget.number_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                    self.widget.was_Clicked = True
                    self.widget.was_visited = True
                    self.eventFilterParent.parentGame.verifyGameStatus()
                        
                    return True
                elif event.type() == QtCore.QEvent.MouseButtonPress and self.eventFilterParent is not None and self.eventFilterParent.icon_selected.objectName() == 'flag_label' and not (self.widget.was_ClickedAsFlag):
                    self.eventFilterParent.first_click = False
                    if not (self.widget.was_Clicked) and (self.eventFilterParent.parentGame.bombs - self.eventFilterParent.parentGame.countBombsSelected()) > 0:
                        self.widget.was_ClickedAsFlag = True
                        self.eventFilterParent.parentGame.recalculeBombsSelected()
                        img = MODE_GROUND["leaf_flagged"]
                        obj.setPixmap(QtGui.QPixmap(img))
                        return True
                elif event.type() == QtCore.QEvent.MouseButtonPress and self.eventFilterParent is not None and self.eventFilterParent.icon_selected.objectName() == 'flag_label' and (self.widget.was_ClickedAsFlag):
                    self.eventFilterParent.first_click = False
                    if not (self.widget.was_Clicked) and (self.widget.was_ClickedAsFlag):
                        self.widget.was_ClickedAsFlag = False
                        self.eventFilterParent.parentGame.recalculeBombsSelected()
                        img = MODE_GROUND["leaf_field"]
                        obj.setPixmap(QtGui.QPixmap(img))
                        return True
                    else:
                        return False
                else:   
                    return False
        else: 
            return False
    def call_neighbor(self):
        self.slot_Field.verify_neighbor_bomb()
        pass
    
    def recalcule_the_first_bomb(self):
        self.eventFilterParent.recalcule_the_first_bomb(self.slot_Field.xCoord, self.slot_Field.yCoord)
        self.call_neighbor()
        pass


