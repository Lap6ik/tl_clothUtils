#!/usr/bin/env python
from PySide2 import QtWidgets, QtGui, QtCore
import os, sys
#import shutil
#import subprocess
import pymel.core as pm

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
        self.clothShapeNodes = None
        self.clothTransformNodes = None
        

        self.__buildUI()

    def __buildUI(self):
        '''
        Function used to build the UI. All the signal, slot and default state are initialized here
        '''  
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        #fill the buttons 
        self.__updateNodeLists()

        self._updateClothObjComboBox() 
        self.ui.clothObjComboBox.currentIndexChanged.connect(self._updateDisableClothObjectCheckBox)

        #self.ui.clothObjComboBox.currentIndexChanged(self._updateClothObjComboBox)


        
        # -------Signals-------------#   

    def __updateNodeLists(self):
        self.clothShapeNodes = pm.ls(exactType='nCloth')
        self.clothTransformNodes = pm.listRelatives(self.clothShapeNodes, parent = True)
        #self._updateDisableClothObjectCheckBox()

    def _updateClothObjComboBox(self):
        self.__updateNodeLists()
        for obj in self.clothTransformNodes:
            b = obj.shortName(stripNamespace=True)
            self.ui.clothObjComboBox.addItem(b)
        self.ui.clothObjComboBox.clearEditText() 

    def _updateDisableClothObjectCheckBox(self):
        clothName = str(self.ui.clothObjComboBox.currentText())
        for obj in self.clothTransformNodes:
            b = obj.shortName(stripNamespace=True)
            if b==clothName:
                pm.select(obj)
                break

        #clothEnabled = pm.getAttr('%s.isDynamic'%obj)

        attributeChange = pm.scriptJob(attributeChange = [obj+'.isDynamic', self._printN])
        print (attributeChange)
    
    def _printN(self):
        print('attribute changed')
  
        # if clothEnabled == 1 and self.ui.disableClothObjectCheckBox.isChecked():
        #     pass
        # elif clothEnabled ==1 and not self.ui.disableClothObjectCheckBox.isChecked():
        #     self.ui.disableClothObjectCheckBox.setChecked(True)
        # else:
        #     self.ui.disableClothObjectCheckBox.setChecked(False)

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
