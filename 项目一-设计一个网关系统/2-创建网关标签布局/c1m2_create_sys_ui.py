'''
1-创建一个主窗口
'''
# 系统库
import sys
# 导入pyqt5的主窗口和应用类
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QTreeWidget, QTreeWidgetItem,
                             QWidget, QVBoxLayout,
                             QLabel, QHBoxLayout)
# 导入由qt designer设计的主窗口
from c1m2_ import Ui_MainWindow
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
        # 设置UI函数
        self.initUI()

    def initUI(self):
        # 创建左侧菜单（QTreeWidget）
        self.menu_tree = QTreeWidget()
        # 隐藏表头
        self.menu_tree.setHeaderHidden(True)
        # 设置左侧菜单的宽度
        self.menu_tree.setFixedWidth(200)

        # 添加顶层菜单项
        rootMainPage = QTreeWidgetItem(self.menu_tree, ['主页'])
        rootConnector = QTreeWidgetItem(self.menu_tree, ['连接器'])
        rootSetting = QTreeWidgetItem(self.menu_tree, ['配置'])
        rootMonitor = QTreeWidgetItem(self.menu_tree, ['数据监控'])

        # 为菜单1添加子菜单项
        childNodeAddConnector = QTreeWidgetItem(rootSetting, ['添加连接器'])
        childNodeConnectServer = QTreeWidgetItem(rootSetting, ['设置服务器接入'])


        # 展开所有菜单项
        self.menu_tree.expandAll()

        # 连接菜单项选中信号到槽函数
        self.menu_tree.itemClicked.connect(self.on_menu_item_clicked)

        # 创建右侧内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # 初始页面内容（可以是一个占位符或默认内容）
        self.current_content = QLabel('请选择左侧菜单项')
        self.content_layout.addWidget(self.current_content)

        # 创建主布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.menu_tree)
        main_layout.addWidget(self.content_widget)

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_menu_item_clicked(self, item, column):
        # 根据选中的菜单项更新右侧内容
        text = item.text(0)  # 获取选中项的文本
        self.update_content(text)

    def update_content(self, menu_text):
        # 这里可以根据 menu_text 的值来动态更新内容
        # 例如，可以根据不同的菜单项显示不同的 QLabel、QTextEdit、QWidget 等
        if menu_text == '子菜单1-1':
            self.current_content.setText('这是子菜单1-1的内容')
        elif menu_text == '子菜单1-2':
            self.current_content.setText('这是子菜单1-2的内容')
        elif menu_text == '子菜单2-1':
            self.current_content.setText('这是子菜单2-1的内容')
        elif menu_text == '子菜单2-2':
            self.current_content.setText('这是子菜单2-2的内容')
        else:  # 如果是顶层菜单项，可以选择显示一个默认内容或子菜单列表
            self.current_content.setText(f'这是{menu_text}的顶层菜单，请选择子菜单')

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