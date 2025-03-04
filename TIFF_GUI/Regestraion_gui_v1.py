import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import  QColor, QPalette, QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout,
                             QWidget, QMenu, QHBoxLayout, QGridLayout, QStackedLayout, QTabWidget,
                             QToolBar, QStatusBar, QCheckBox, QDialog, QMessageBox, QDialogButtonBox, 
                             QFileDialog)
from layout_colorwidget import Color
from random import choice, randint
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


from Reg_optical_flow_ilk import reg_optical_flow_ilk
from Reg_optical_flow_tvl1 import reg_optical_flow_tvl1



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration GUI")
        
        
        

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout() 
        layout3 = QVBoxLayout() 

        
        
        #### Label and plot for image 1 #####
        # text1 = QLabel("Image 1")
        # font = text1.font()
        # # font.setPointSize(15)
        # text1.setFont(font)
        # text1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        # self.setCentralWidget(text1)
        # layout2.addWidget(text1)
        
        
    
        
        ##### button for load image 1 ######
        button1 = QPushButton("Load image 1", self)
        button1.clicked.connect(lambda: self.openFileDialog(f1,0))
        layout2.addWidget(button1) 
        
        f1 = QLabel("Image not loaded")
        layout2.addWidget(f1)
        

        
        layout1.addLayout(layout2)
        

        ##### Label and plot for image 2 #####
        # text2 = QLabel("Image 2")
        # font = text2.font()
        # # font.setPointSize(15)
        # text2.setFont(font)
        # text2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        # self.setCentralWidget(text2)
        # layout3.addWidget(text2)
        
        ##### button for load image 2 ######
        button2 = QPushButton("Load image 2", self)
        button2.clicked.connect(lambda: self.openFileDialog(f2,1))
        layout3.addWidget(button2)
        
        f2 = QLabel("Image not loaded")
        layout3.addWidget(f2)

        
        
        layout1.addLayout(layout3)
        
        ##### list the file path of the two loaded images
        self.file_paths = ["", ""]

        
        
        
        button3 = QPushButton("Optical_flow_ilk", self)
        button3.clicked.connect(self.analysis_run_ilk)
        layout2.addWidget(button3)
        
        
        
        button4 = QPushButton("Optical_flow_tvl1", self)
        button4.clicked.connect(self.analysis_run_tvl1)
        layout3.addWidget(button4)
        
        
        
        ##### Plot results #####
        layout5 = QVBoxLayout() 
        
        # text3 = QLabel("Results")
        # font = text1.font()
        # # font.setPointSize(15)
        # text3.setFont(font)
        # text3.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        # self.setCentralWidget(text3)
        # layout5.addWidget(text3)
        
        layout6 = QHBoxLayout() 
        
     
        self.figure1 = plt.figure(figsize = (8,8))
        self.canvas1 = FigureCanvas(self.figure1)
        layout6.addWidget(self.canvas1)
    
        self.figure2 = plt.figure(figsize = (8,8))
        self.canvas2 = FigureCanvas(self.figure2)
        layout6.addWidget(self.canvas2)
        
        layout5.addLayout(layout6)
        
        
        layout7 = QHBoxLayout() 
        
        self.figure3 = plt.figure(figsize = (8,8))
        self.canvas3 = FigureCanvas(self.figure3)
        layout7.addWidget(self.canvas3)
        
        self.figure4 = plt.figure(figsize = (8,8))
        self.canvas4 = FigureCanvas(self.figure4)
        layout7.addWidget(self.canvas4)
        
        layout5.addLayout(layout7)
        
        
        layout8 = QHBoxLayout() 
        
        self.figure5 = plt.figure(figsize = (12,8))
        self.canvas5 = FigureCanvas(self.figure5)
        layout8.addWidget(self.canvas5)
        
        self.figure6 = plt.figure(figsize = (12,8))
        self.canvas6 = FigureCanvas(self.figure6)
        layout8.addWidget(self.canvas6)
        
        self.figure7 = plt.figure(figsize = (12,8))
        self.canvas7 = FigureCanvas(self.figure7)
        layout8.addWidget(self.canvas7)
        
        layout5.addLayout(layout8)
        
        
        
        
        layout1.addLayout(layout5)

        layout1.setContentsMargins(30,30,30,30)
        layout1.setSpacing(20)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
    
        
        
    def openFileDialog(self,f,index):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            # print("Selected File:", selected_files[0]) 
            
            figure = QPixmap(selected_files[0])
            figure_resize = figure.scaledToWidth(256)
            f.setPixmap(figure_resize)
            
            self.file_paths[index] = selected_files[0] 


        
    def analysis_run_ilk(self, check):
        seq_im, reg_im, norm, norm_flat, u1, v1, u, v, x, y = reg_optical_flow_ilk(self.file_paths)
        
        
        ax = self.figure1.add_subplot(111)
        ax.imshow(seq_im,aspect='equal')
        ax.set_title("w cross-corr.; w/o optical flow")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas1.draw()


        ax = self.figure2.add_subplot(111)
        ax.imshow(reg_im,aspect='equal')
        ax.set_title("w cross-corr.; then optical flow")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas2.draw()

        ##### Display

        ax = self.figure3.add_subplot(111)
        ax.imshow(norm)
        ax.quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
        ax.set_title("Optical flow magnitude and vector field")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas3.draw()
        
        
        
        ax = self.figure4.add_subplot(111)
        ax.imshow(reg_im, cmap='gray')
        ax.quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas4.draw()

        
        #### histograph of norm, u1, v1
        ax1 = self.figure5.add_subplot(111)
        ax1.hist(norm_flat, bins=50, edgecolor='black', alpha=0.7)
        ax1.set_title('Norm')
        ax1.set_xlabel('Pixel')
        ax1.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas5.draw()
        
        ax2 = self.figure6.add_subplot(111)
        ax2.hist(abs(u1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='orange')
        ax2.set_title('horizontal')
        ax2.set_xlabel('Pixel')
        ax2.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas6.draw()

        ax3 = self.figure7.add_subplot(111)
        ax3.hist(abs(v1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='green')
        ax3.set_title('vertical')
        ax3.set_xlabel('Pixel')
        ax3.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas7.draw()
        
        
        
    def analysis_run_tvl1(self, check):
        seq_im, reg_im, norm, norm_flat, u1, v1, u, v, x, y = reg_optical_flow_tvl1(self.file_paths)
        
        
        ax = self.figure1.add_subplot(111)
        ax.imshow(seq_im,aspect='equal')
        ax.set_title("w cross-corr.; w/o optical flow")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas1.draw()


        ax = self.figure2.add_subplot(111)
        ax.imshow(reg_im,aspect='equal')
        ax.set_title("w cross-corr.; then optical flow")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas2.draw()

        ##### Display

        ax = self.figure3.add_subplot(111)
        ax.imshow(norm)
        ax.quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
        ax.set_title("Optical flow magnitude and vector field")
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas3.draw()
        
        
        
        ax = self.figure4.add_subplot(111)
        ax.imshow(reg_im, cmap='gray')
        ax.quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
        ax.set_axis_off()
        plt.tight_layout()
        self.canvas4.draw()

        
        #### histograph of norm, u1, v1
        ax1 = self.figure5.add_subplot(111)
        ax1.hist(norm_flat, bins=50, edgecolor='black', alpha=0.7)
        ax1.set_title('Norm')
        ax1.set_xlabel('Pixel')
        ax1.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas5.draw()
        
        ax2 = self.figure6.add_subplot(111)
        ax2.hist(abs(u1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='orange')
        ax2.set_title('horizontal')
        ax2.set_xlabel('Pixel')
        ax2.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas6.draw()

        ax3 = self.figure7.add_subplot(111)
        ax3.hist(abs(v1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='green')
        ax3.set_title('vertical')
        ax3.set_xlabel('Pixel')
        ax3.set_ylabel('Frequency')
        plt.tight_layout()
        self.canvas7.draw()




        
          
            
app = QApplication(sys.argv)
w = MainWindow()
# w.resize(1440,900);
w.show()
app.exec()

