'''
1-创建一个主窗口
'''
# 系统库
import sys
# 导入pyqt5的主窗口和应用类
from PyQt5.QtWidgets import QMainWindow, QApplication
# 导入由qt designer设计的主窗口
from c1m2 import Ui_MainWindow
# 导入串口通信类
import m1_serial.tools.list_ports
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
        # 设置类的成员变量
        self.init_values()
        # 设置类的控件
        self.init_widget()

    def init_values(self):
        # 串口是否打开的flag
        self.pushButton_serial_flag = False
        # 用于保存串口的类
        self.myserial : serial.Serial

    def init_widget(self):
        '''
        初始化，设置控件的方法
        :return:
        '''
        # 初始化串口号列表
        ports = serial.tools.list_ports.comports()
        self.ui.combobox_serialport.clear()
        for port in ports:
            self.ui.combobox_serialport.addItem(f"{port.device}")
        # 初始化波特率列表
        baudRateItem = [300,1200,2400,4800,9600,19200,38400,57600,115200]
        for item in baudRateItem:
            self.ui.combobox_baudrate.addItem(f"{item}")
        # 打开串口按钮的初始化
        self.ui.pushButton_serial.clicked.connect(self.pushButton_serial_clicked_callback)

    def pushButton_serial_clicked_callback(self):
        if self.pushButton_serial_flag:
            self.pushButton_serial_flag = False
            self.ui.pushButton_serial.setText("打开串口")
            self.myserial.close()
            if not self.myserial.is_open:
                self.ui.textBrowser_log.append("串口"+self.ui.combobox_serialport.currentText()+"已经关闭")
                self.ui.combobox_serialport.setEnabled(True)
                self.ui.combobox_baudrate.setEnabled(True)
                print("串口成功关闭")
        else:
            self.myserial = serial.Serial(self.ui.combobox_serialport.currentText(), int(self.ui.combobox_baudrate.currentText()))
            # self.myserial = serial.Serial("COM31", int(self.ui.combobox_baudrate.currentText(), 5))
            if self.myserial.is_open:
                print("串口成功打开")
                self.ui.textBrowser_log.append("串口"+self.ui.combobox_serialport.currentText()+"成功打开")
                self.ui.combobox_serialport.setDisabled(True)
                self.ui.combobox_baudrate.setDisabled(True)
                self.pushButton_serial_flag = True
                self.ui.pushButton_serial.setText('关闭串口')
            else:
                self.ui.textBrowser_log.append("串口"+self.ui.combobox_serialport.currentText()+"打开失败")
                print("串口打开失败")


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