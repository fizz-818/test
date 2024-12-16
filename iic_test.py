import machine
import time

# I2C初始化
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))  # 根据实际硬件连接引脚修改这里的引脚编号
# 例如这里假设I2C使用的是0号I2C总线，SCL引脚连接到开发板的引脚5，SDA引脚连接到引脚4

# AHT20传感器地址，不同传感器地址不同，AHT20默认地址通常是0x38
AHT20_ADDR = 0x38  

# 初始化AHT20传感器的一些命令和参数
CMD_INITIALIZE = bytearray([0xBE, 0x08, 0x00])
CMD_TRIGGER_MEASUREMENT = bytearray([0xAC, 0x33, 0x00])

# 向传感器发送命令的函数
def write_command(command):
    i2c.writeto(AHT20_ADDR, command)

# 从传感器读取数据的函数
def read_data(num_bytes):
    return i2c.readfrom(AHT20_ADDR, num_bytes)

# 初始化AHT20传感器
def init_aht20():
    write_command(CMD_INITIALIZE)
    time.sleep(0.2)  # 等待传感器初始化完成，具体等待时间参考传感器手册

# 触发测量并获取温湿度数据
def get_temperature_and_humidity():
    write_command(CMD_TRIGGER_MEASUREMENT)
    time.sleep(0.08)  # 等待测量完成，不同传感器等待时间不同

    data = read_data(6)
    humidity = (data[1] << 12 | data[2] << 4 | data[3] >> 4) / 1048576.0 * 100
    temperature = ((data[3] & 0x0F) << 16 | data[4] << 8 | data[5]) / 1048576.0 * 200 - 50
    return temperature, humidity

# 主程序入口
if __name__ == "__main__":
    init_aht20()
    while True:
        temperature, humidity = get_temperature_and_humidity()
        print("温度: {:.2f}°C".format(temperature))
        print("湿度: {:.2f}%".format(humidity))
        time.sleep(2)  # 每隔2秒获取一次数据，可根据需求调整间隔时间
