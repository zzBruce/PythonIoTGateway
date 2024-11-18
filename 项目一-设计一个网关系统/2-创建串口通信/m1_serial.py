# 导入库，serial库为串口通信库，time是延迟库
import serial
import time
# 打开串口，设置串口参数：端口号COM31，数据长度8比特，无校验位，停止位1比特，最长延迟1秒
myserial = serial.Serial('COM31', 9600, 8, 'N', 1, 1)
# is_open变量判断是否打开成功
if myserial.is_open:
    print(myserial.port,"打开成功")
else:
    print(myserial.port,"打开失败")
# 捕获串口通信的错误
try:
    # 通信循环
    while True:
        # 发送固定的语句
        myserial.write(b"hello serial, i am 23wlw zhangzhen!")
        # 延时5秒
        time.sleep(5)
        # 判断是否有未读数据的数量（大于0即存在未读的数据）
        if myserial.in_waiting > 0:
            # 读取发送过来的数据，保存在data中
            data = myserial.read(myserial.in_waiting)
            # 打印数据
            print('接收到的数据', data.decode('ascii'))
except KeyboardInterrupt:
    # 如果接收到键盘中断退出，即输出此句
    print('程序被中断')
finally:
    # 无论捕获结果如何，都关闭串口
    myserial.close()
    # 输出串口关闭信息
    print('串口已经关闭')