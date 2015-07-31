'''
Created on 09.07.2015

@author: jrenken
'''
from PyQt4.QtGui import QWidget, QHBoxLayout, QToolButton, QLineEdit, QIcon
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPoint
from PyQt4.Qt import pyqtSlot
from PyQt4.QtCore import Qt

class PositionDisplay(QWidget):
    '''
    classdocs
    '''

    __FORMATS = ('DD', 'DDM', 'DMDS')
    
    def __init__(self, iface, parent=None):
        '''
        Constructor
        '''
        super(PositionDisplay, self).__init__(parent)
        self.setObjectName('positionDisplay')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 3, 0)
        self.button = QToolButton(self)
        self.button.setText(self.__FORMATS[1])
        self.button.setObjectName('toolButtonFormat')
        self.button.clicked.connect(self.switchCoordinateFormat)
        self.button.setAutoRaise(True)
        layout.addWidget(self.button)
        self.label = QLineEdit('---  ---')
        self.label.setReadOnly(True)
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setStyleSheet('font-weight: bold;')
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.format = 1
        
        canvas = iface.mapCanvas()
        crsDest = QgsCoordinateReferenceSystem(4326)
        crsSrc = canvas.mapSettings().destinationCrs()
        self.xform = QgsCoordinateTransform(crsSrc, crsDest)
        canvas.xyCoordinates.connect(self.mouseMoved)
        canvas.destinationCrsChanged.connect(self.mapCrsHasChanged)
        self.canvas = canvas
        
    @pyqtSlot(name='on_toolButtonFormat_clicked')
    def switchCoordinateFormat(self):
        self.format = (self.format + 1) % 3
        self.button.setText(self.tr(self.__FORMATS[self.format]))

            
            
    
    @pyqtSlot()
    def mapCrsHasChanged(self):
        crsSrc = self.canvas.mapSettings().destinationCrs()
        self.xform.setSourceCrs(crsSrc)
    
    @pyqtSlot(QgsPoint)        
    def mouseMoved(self, point):
        pt = self.xform.transform(point)
        self.label.setText(self.posToStr(pt))
       
    def posToStr(self, pos):
        if self.format == 0:
            return '{:.6f}, {:.6f}'.format(pos.y(), pos.x())
        if self.format == 1:
            return ', '.join(pos.toDegreesMinutes(4, True, True).rsplit(',')[::-1])
        if self.format == 2:
            return ', '.join(pos.toDegreesMinutesSeconds(2, True, True).split(',')[::-1])