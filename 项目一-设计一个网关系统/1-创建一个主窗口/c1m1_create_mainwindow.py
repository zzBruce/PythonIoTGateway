'''
1-创建一个主窗口
'''
# 系统库
import sys
# 导入pyqt5的主窗口和应用类
from PyQt5.QtWidgets import QMainWindow, QApplication
# 导入由qt designer设计的主窗口
from c1m1 import Ui_MainWindow
class SmartRanchSystemMainWindow(QMainWindow):
    '''
    智慧牧场系统主窗口类,继承了QMainWindow类
    '''
    def __init__(self):
        # 调用父类的初始函数
        QMainWindow.__init__(self)
        # 设计一个ui变量，用于存储qt designer设计的主窗口类
        self.ui = Ui_MainWindow()
        # 安装此窗口的所有静态UI
        self.ui.setupUi(self)

if __name__=='__main__':
    '''
    主函数，程序入口
    '''
    # 创建一个QT应用
    app = QApplication(sys.argv)
    # 实例化智慧牧场系统类
    smartRanch = SmartRanchSystemMainWindow()
    # 显示主窗口
    smartRanch.show()
    # 退出系统
    sys.exit(app.exec_())