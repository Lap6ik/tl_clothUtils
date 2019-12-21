#!/usr/bin/env python
from PySide2 import QtWidgets, QtGui, QtCore
import os, sys
# import shutil
import pymel.core as pm
from maya import OpenMaya
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
        self.clothTransformNodes = []
        self.clothShapeNodes = []
        self.colliderTransformNodes = []
        self.selectedItems = []

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
        self.ui.clothObjectsListWidget.itemClicked.connect(self._itemSelect)
        self.ui.colliderObjectsListWidget.itemClicked.connect(self._itemSelect)

    def __updateClothObjectsListWidget(self):
        self.ui.clothObjectsListWidget.clear()
        self.ui.clothObjectsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        clothShapeNodes = pm.ls(exactType='nCloth')
        self.clothTransformNodes = pm.listRelatives(clothShapeNodes, parent = True ) 
        for obj in self.clothTransformNodes:
            b = obj.shortName(stripNamespace=True)
            a = pm.listRelatives(obj, children = True, shapes = True)
            c = pm.listConnections(a,source = True,type = 'mesh')
            d = c[0].shortName(stripNamespace = True)
            item = '%s --> %s'%(b,d)
            self.ui.clothObjectsListWidget.addItem(item)

    def __updateColliderObjectListWidget(self):
        self.ui.colliderObjectsListWidget.clear()
        self.ui.colliderObjectsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        colliderShapeNodes = pm.ls(exactType='nRigid')
        self.colliderTransformNodes = pm.listRelatives(colliderShapeNodes, parent = True ) 
        for obj in self.colliderTransformNodes:
            b = obj.shortName(stripNamespace = True)
            a = pm.listRelatives(obj, children = True, shapes = True)
            c = pm.listConnections(a,source = True,type = 'mesh')
            d = c[0].shortName(stripNamespace = True)
            item = '%s --> %s'%(b,d)
            self.ui.colliderObjectsListWidget.addItem(item)
    
    def _itemSelect(self):
        items = []
        for k in range(self.ui.clothObjectsListWidget.count()):
            items.append(self.ui.clothObjectsListWidget.item(k))
        for k in range(self.ui.colliderObjectsListWidget.count()):
            items.append(self.ui.colliderObjectsListWidget.item(k))
        for item in items:
            itemName = item.text()
            #print (itemName)
            if item.isSelected() and self.__splitName(itemName) in self.selectedItems: 
                pass
            elif item.isSelected() and self.__splitName(itemName) not in self.selectedItems:
                self.selectedItems.append(self.__splitName(itemName))
            elif not item.isSelected() and self.__splitName(itemName) in self.selectedItems: 
                self.selectedItems.remove(self.__splitName(itemName))
            elif not item.isSelected() and self.__splitName(itemName) not in self.selectedItems:
                pass
        pm.select(self.selectedItems, replace = True)
        print ('selected items are %s'%self.selectedItems)

    #callbacks.py

    # def addNameChangedCallback(callback, pynode = None):
    #     def omcallback(mobject, oldname, ):
    #         newname = OpenMaya.MFnDependencyNode(mobject).name()
    #         changedPynode = pm.PyNode(newname)
    #         if not isvalidnode(changedPynode):
    #             return
    #         callback(changedPynode, oldname, newname)
    #     if pynode is None:
    #         listenTo = OpenMaya.MObject()
    #     else:
    #         listenTo = pynode.__apimobject__()
    #     return OpenMaya.MNodeMessage.addNameChangedCallback(listenTo, omcallBack)
        
    # def _invalidnode(pynode)
    #     try:
    #         bool(pynode)
    #         return True
    #     except KeyError:
    #         return False
            
    # def removeNameChangeCallBack(callBackID):
    #     OpenMaya.MNodeMessage.removeCallback(callbackID)
    

    def __splitName(self, itemText):
        if (r' --> ') in str(itemText):
            objectOutputMesh = itemText.rpartition(' --> ')[2]
            return objectOutputMesh             
        
        # clothEnabled = pm.getAttr('%s.isDynamic'%obj)

        #attributeChange = pm.scriptJob(attributeChange = [obj+'.isDynamic', self._printN])

    
    def _printN(self):
        print('attribute changed') 

def main():
    '''
    Main function for starting the application
    '''

    app = QtWidgets.QApplication(sys.argv)
    widget = ClothUtils()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
