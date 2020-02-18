import os
import sys
import time
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog


class SWFOPEN(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #设置窗口大小
        self.resize(800, 120)
        #调用自定义方法使窗口显示在屏幕中央
        self.center()

        #设置标签
        self.title = QtWidgets.QLabel(self)
        #设置标签大小
        self.title.resize(100, 35)
        #设置标签位置
        self.title.move(20, 20)
        #标签信息
        self.title.setText('文件路径：')
        #标签字体信息
        self.title.setFont(QtGui.QFont("Arial", 13, QtGui.QFont.Black))

        #设置选择文件路径的按钮
        self.myButton = QtWidgets.QPushButton(self)
        #按钮id
        self.myButton.setObjectName("myButton")
        #按钮中的信息
        self.myButton.setText("选择文件")
        #按钮位置
        self.myButton.move(670, 20)
        #按钮大小
        self.myButton.resize(100, 35)
        #点击按钮后调用方法打开文件选择框
        self.myButton.clicked.connect(self.msg)

        #设置文本框用来显示选择的文件路径
        self.path = QtWidgets.QLineEdit(self)
        self.path.move(140, 20)
        self.path.resize(500, 35)
        self.path.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Courier))

        #打开文件按钮
        self.myopenButton = QtWidgets.QPushButton(self)
        self.myopenButton.setObjectName("myopenButton")
        self.myopenButton.setText("打开文件")
        self.myopenButton.move(330, 70)
        self.myopenButton.resize(100, 35)
        #点击后调用自定义函数打开文件
        self.myopenButton.clicked.connect(self.openfile)

        #设置对话框左上角的图像
        self.setWindowTitle('swf_open')
        self.setWindowIcon(QIcon('shilaimu.png'))

        self.show()

    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def msg(self):
        #获取文件路径，文件类型
        self.fileName, self.filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:", "All Files (*)")
        #print(self.fileName, self.filetype)
        #将文件路径显示到文本框中
        self.path.setText(self.fileName)

    def openfile(self):
        #获取文本框中信息
        str = self.path.text()
        #如果为空则无操作
        if str == "":
            return
        else:
            self.url = str
            #更新html文件的信息，如果返回False则说明文件格式不对
            if self.update(1) is False:
                QMessageBox.information(self, "提示", "文件格式错误，请重新选择文件", QMessageBox.Yes)
            else:
                #调用自定义函数用浏览器打开swf文件
                self.openurl()

    def update(self, flag):
        data = ""
        filepath = self.url
        with open('flash.html','r+') as f:
            fp = f.readlines()
            for line in fp:
                #更新有embed元素的这一行信息
                if line.find('embed') == 1:
                    #flag为1则更新为选中的文件，flag为0则更新为空字符串
                    if flag == 1:
                        #文件根目录，文件名
                        filepwd, filename  = os.path.split(filepath)
                        #如果文件后缀为swf则更新，否则返回False
                        if os.path.splitext(filename)[1] == '.swf':
                            data += '<embed src='+'"' + filepath + '"' + ' width="100%" height="100%"></embed>' + '\n'
                        else:
                            return False
                    elif flag == 0:
                        data += '<embed src='+'""' + ' width="100%" height="100%"></embed>' + '\n'
                #每一行数据都存入data
                else:
                    data += line
            #print(data)
        with open('flash.html', 'w+') as f:
            #将数据覆盖写入文件
            f.writelines(data)

    def openurl(self):
        #用默认浏览器打开html文件
        webbrowser.open('flash.html', new=0, autoraise=True)
        #休眠三秒后将文件初始化
        time.sleep(3)
        self.update(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SWFOPEN()
    sys.exit(app.exec_())