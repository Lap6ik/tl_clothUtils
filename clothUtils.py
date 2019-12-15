#!/usr/bin/env python
from PySide2 import QtWidgets, QtGui, QtCore
import os, sys
# import shutil
# import subprocess
import pymel.core as pm
# from importlib import reload

import clothUtilsUI as ui
reload(ui)

def doOpenUI(delete=False):
    '''
    Function used to call the instansantation of the tool avoiding 
    the duplicate of leaving extra class behind
    ''' 
    dial = None
    for qt in QtWidgets.QApplication.topLevelWidgets():
        if qt.__class__.__name__== 'ClothUtils':
            dial = qt
            print (dial)

        if not dial:
            dial = ClothUtils()
            return dial 
        else:
            dial.close()
            dial = ClothUtils()
            return dial

class ClothUtils(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ClothUtils, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        #class veriables
        self.clothTransformNodes = None
        self.colliderTransformNodes = None
        self.currentSelection = []

        self.__buildUI()

    def __buildUI(self):
        '''
        Function used to build the UI. All the signal, slot and default state are initialized here
        '''  
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # fill the buttons 
        self.__updateClothObjectsListWidget()
        self.__updateColliderObjectListWidget()

        #----------Signals-----------#
        self.ui.clothObjectsListWidget.itemClicked.connect(self._clothObjectSelect)

    def __updateClothObjectsListWidget(self):
        self.ui.clothObjectsListWidget.clear()
        self.ui.clothObjectsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        clothShapeNodes = pm.ls(exactType='nCloth')
        self.clothTransformNodes = pm.listRelatives(clothShapeNodes, parent = True ) 
        for obj in self.clothTransformNodes:
            b = obj.shortName(stripNamespace=True)
            self.ui.clothObjectsListWidget.addItem(b)

    def __updateColliderObjectListWidget(self):
        self.ui.colliderObjectListWidget.clear()
        self.ui.colliderObjectListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        colliderShapeNodes = pm.ls(exactType='nRigid')
        self.colliderTransformNodes = pm.listRelatives(colliderShapeNodes, parent = True ) 
        for obj in self.colliderTransformNodes:
            b = obj.shortName(stripNamespace=True)
            self.ui.colliderObjectListWidget.addItem(b)
    
    def _clothObjectSelect(self):
        item = self.ui.clothObjectsListWidget.currentItem()
        itemName = item.text()
        print (itemName)
        print (type(itemName))
        if self.ui.clothObjectsListWidget.isItemSelected(item):
            #if current item selected do the 
            if not self.currentSelection:
                a = pm.select(itemName, replace = True)
                self.currentSelection.append(itemName)
                print ('we are in option one')
            else:
                a = pm.select(itemName, add = True)
                self.currentSelection.append(itemName)
                print ('we are in option two')
            print ('selected objects list %s'%self.currentSelection)
        
        
        selectedNames = self.ui.clothObjectsListWidget.selectedItems()
        print ('%s\n'%selectedNames)
            
        
        # clothEnabled = pm.getAttr('%s.isDynamic'%obj)

        #attributeChange = pm.scriptJob(attributeChange = [obj+'.isDynamic', self._printN])

    
    def _printN(self):
        print('attribute changed') 

# def main():
#     '''
#     Main function for starting the application
#     '''

#     app = QtWidgets.QApplication(sys.argv)
#     widget = ClothUtils()
#     widget.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#         main()
