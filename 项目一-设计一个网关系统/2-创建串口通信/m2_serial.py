# 导入库，struct库是用于结构体的类，serial库为串口通信库，time是延迟库
import struct
import serial
import time
# 进行CRC校验的类
class CRC16Checker():
    def __init__(self):
        # crc16 modbus的多项式
        self.CRC16_MODBUS = 0xA001
    def crc16(self, data:bytes, polynomial) -> int:
        """
        计算给定字节数据的CRC16 校验码。
        :param data: 要计算CRC的字节数据
        :param polynomial: 多项式
        :return: CRC16校验码（整数形式）
        """
        # 初始化CRC寄存器为0xFFFF
        crc = 0xFFFF
        # 遍历所有数据（以字节为单位）
        for byte in data:
            # 将当前字节与CRC寄存器异或
            crc ^= byte
            # 对当前字节的每一位进行循环处理
            for i in range(8):
                # 如果CRC的最低位为1
                if crc & 0x0001:
                    # 右移一位并与生成多项式异或
                    crc = (crc >> 1)^polynomial
                else:
                    # 否则只右移一位
                    crc >>=1
        return crc

# 用于保存命令请求的类
class SlaveNode():
    def __init__(self, sensorType):
        '''
        初始化函数，设置从节点的关键参数
        '''
        # 从节点地址
        self.slave_address = 0
        # 功能码
        self.function_code = 0
        # 起始地址
        self.start_address = 0
        # 寄存器数量
        self.quantity = 0
        # 响应读取的数据长度
        self.byte_count = 0
        '''
        设置传感器类型：
        1：温湿度传感器
        '''
        self.sensorType = sensorType
    def settingREQ(self,
                   slave_address,
                   function_code,
                   start_address,
                   quantity,
                   byte_count
                   ):
        '''
        用于设置从节点的请求命令关键数据
        :param slave_address: 从设备地址
        :param function_code: 功能码
        :param start_address: 寄存器起始地址
        :param quantity: 寄存器读取数量
        :param byte_count: 响应指令的数据长度
        '''
        self.slave_address = slave_address
        self.function_code = function_code
        self.start_address = start_address
        self.quantity = quantity
        self.byte_count = byte_count


if __name__=='__main__':
    # 用于保存所有要读取传感器的字典
    sensors = []
    # 创建一个温湿度从节点
    temphumi = SlaveNode(1)
    # 设置从节点的请求数据：地址01，功能码03，起始地址0000，寄存器个数0001，响应的数据长度0004
    temphumi.settingREQ(0x01,0x03, 0x0000, 0x0002, 0x0004)
    # 添加到传感器字典中
    sensors.append(temphumi)
    # 实例化CRC算法类
    crc = CRC16Checker()
    # 创建串口通信与温湿度传感器采集温湿度传感器
    myserial = serial.Serial('COM31', 9600, 8, 'N', 1, 1)
    # 判断是否打开串口成功
    if myserial.is_open:
        print(myserial.port,"打开成功")
    else:
        print(myserial.port,"打开失败")
        # 失败即退出程序
        exit()
    # 捕获串口通信的错误
    try:
        # 通信循环
        while True:
            # 变量要采集的所有传感器
            for sensor in sensors:
                # 结构图打包为modbus协议request_frame[从设备地址][功能码][起始地址][寄存器个数]
                request_frame = struct.pack('>BBHH',
                                            sensor.slave_address,
                                            sensor.function_code,
                                            sensor.start_address,
                                            sensor.quantity)
                # 计算出CRC校验码
                crc_value = crc.crc16(request_frame, crc.CRC16_MODBUS)
                # 在数据后面添加校验码[从设备地址][功能码][起始地址][寄存器个数][校验码]
                request_frame += struct.pack('<H',
                                             crc_value)
                print("发送了请求", request_frame.hex())
                # 发送modbus请求request_frame
                myserial.write(request_frame)
                # 判断是否有未读数据的数量（大于0即存在未读的数据）
                if myserial.in_waiting > 0:
                    # 读取发送过来的命令响应
                    response = myserial.read(myserial.in_waiting)
                    # 读取命令响应中的数据
                    data = response[:-2]
                    # CRC算法计算校验码
                    crc_value = crc.crc16(data, crc.CRC16_MODBUS)
                    # 从命令响应中提取的校验码
                    crc_value_check = struct.unpack('<H', response[-2:])[0]
                    # 命令响应计算出的校验码与命令响应提取的校验码比较
                    if crc_value_check == crc_value:
                        # 如果一样，表示数据传输成功
                        print('接收到的数据', response.hex())
                        print('响应从机地址', response[0], ',功能码', response[1])
                        # 判断当前传感器类型
                        if sensor.sensorType == 1:
                            # 读取湿度，响应命令的4-5字节
                            humidity = struct.unpack('>H', response[3:5])[0]
                            # 读取湿度，响应命令的6-7字节
                            temperature = struct.unpack('>H', response[5:7])[0]
                            # 实际值为读取值除以10
                            print("温度", temperature/10, '湿度', humidity /10)
                    else:
                        # 如果不一样，传输失败
                        print('校验错误', response.hex())
                # 延时5秒
                time.sleep(5)
    except KeyboardInterrupt:
        # 如果接收到键盘中断退出，即输出此句
        print('程序被中断')
    finally:
        # 无论捕获结果如何，都关闭串口
        myserial.close()
        # 输出串口关闭信息
        print('串口已经关闭')