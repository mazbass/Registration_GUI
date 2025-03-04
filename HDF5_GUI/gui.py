import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QColor, QPalette, QIcon, QKeySequence, QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout,
                             QWidget, QMenu, QHBoxLayout, QGridLayout, QStackedLayout, QTabWidget,
                             QToolBar, QStatusBar, QCheckBox, QDialog, QMessageBox, QDialogButtonBox)
from layout_colorwidget import Color
from random import choice, randint




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration GUI")

        layout1 = QHBoxLayout() # horizontal axis
        layout2 = QVBoxLayout() # the first row
        layout3 = QVBoxLayout() # the second row
        layout4 = QVBoxLayout() # the third row

        ###### the first row #######
        ###### two figures for compare #######


        text1 = QLabel("Figure 1")
        font = text1.font()
        font.setPointSize(15)
        text1.setFont(font)
        text1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(text1)
        layout2.addWidget(text1)

        f1 = QLabel()
        figure1 = QPixmap('Uncoated_Sample5_Frame1.tif')
        figure1_resize = figure1.scaledToWidth(512)
        f1.setPixmap(figure1_resize)
        layout2.addWidget(f1)
        
        
        text2 = QLabel("Figure 2")
        font = text2.font()
        font.setPointSize(15)
        text2.setFont(font)
        text2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(text2)
        layout2.addWidget(text2)
        
        f2 = QLabel()
        figure2 = QPixmap('Uncoated_Sample5_Frame300.tif')
        figure2_resize = figure2.scaledToWidth(512)
        f2.setPixmap(figure2_resize)
        layout2.addWidget(f2)


        layout1.addLayout(layout2)
        
        
        
        ###### the second row #######
        ###### the processed figure #######
        
        
        text3 = QLabel("Processed figure")
        font = text3.font()
        font.setPointSize(15)
        text3.setFont(font)
        text3.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(text3)
        layout3.addWidget(text3)
        
        
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
    

        f3 = QLabel()
        figure3 = QPixmap('Uncoated_Sample5_Frame1.tif')
        figure3_resize = figure3.scaledToWidth(768)
        f3.setPixmap(figure3_resize)
        tabs.addTab(f3,"Method 1")
        
        
        f4 = QLabel()
        figure4 = QPixmap('Uncoated_Sample5_Frame300.tif')
        figure4_resize = figure4.scaledToWidth(768)
        f4.setPixmap(figure4_resize)
        tabs.addTab(f4,"Method 2")

        layout3.addWidget(tabs)
        
        
        layout1.addLayout(layout3)
        # self.stacklayout.addWidget(Color("red"))
        



        
        
        ###### the third row #######
        ###### show the difference #######
        
        
        f1 = QLabel()
        figure1 = QPixmap('Uncoated_Sample5_Frame1.tif')
        figure1_resize = figure1.scaledToWidth(512)
        f1.setPixmap(figure1_resize)
        layout4.addWidget(f1)


        layout1.addLayout(layout4)
        layout1.setContentsMargins(30,30,30,30)
        layout1.setSpacing(20)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
    def activate_tab_1(self):
        self.layout3.setCurrentIndex(0)
        
    def activate_tab_2(self):
        self.layout3.setCurrentIndex(1)
        
            
            
app = QApplication(sys.argv)
w = MainWindow()
# w.resize(1440,900);
w.show()
app.exec()