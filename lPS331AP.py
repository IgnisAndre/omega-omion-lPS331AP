from OmegaExpansion import onionI2C
from time import sleep
'''
    Registers address map
'''
r_a_m = {
"EF_P_XL" : 0x08,
"REF_P_L" : 0x09,
"REF_P_H" : 0x0a,
"WHO_AM_I" : 0x0f,
"RES_CONF" : 0x10,
"CTRL_REG1" : 0x20,
"CTRL_REG2" : 0x21,
"CTRL_REG3" : 0x22,
"INT_CFG_REG" : 0x23,
"INT_SOURCE_REG" : 0x24,
"THS_P_LOW_RadEG" : 0x25,
"THS_P_HIGH_REG" : 0x26,
"STATUS_REG" : 0x27,
"PRESS_OUT_XL" : 0x28,
"PRESS_OUT_L" : 0x29,
"PRESS_OUT_H" : 0x2a,
"TEMP_OUT_L" : 0x2b,
"TEMP_OUT_H" : 0x2c,
"AMP_CTRL" : 0x30
}
'''
    STRING to HEX map
'''
s_t_h = { '0' : 0,  '1' : 1,  '2' : 2,  '3' : 3,
          '4' : 4,  '5' : 5,  '6' : 6,  '7' : 7,
          '8' : 8,  '9' : 9,  'a' : 10, 'b' : 11,
          'c' : 12, 'd' : 13, 'e' : 14, 'f' : 16 }

class LPS331AP(object):
              
    def __init__(self, address=0x5c, precision=True):
        self.i2c = onionI2C.OnionI2C()
        self.address = address
        self.precision = precision
        self.temperature = 0.0
        self.pressure = 0.0

        if self.__deviceAdressCheck(self.address):
            print('Device found')
            self.__power_down(self.address) #for clean start
            if self.__working_check(self.address):
                raise EnvironmentError('Chip seems to be broken')
            else:
                print('Operation test - success!')
        else:
            raise ValueError('Wrong LPS331AP address')
            
    def get_temperature(self):
        if self.precision:
            self.__set_higher_precision(self.address)
        self.__turn_on(self.address)
        self.__run_measurement(self.address)
        c = self.__check_measurement(self.address)
        while not c:
            c = self.__check_measurement(self.address)
        t = self.__read_temperature(self.address)
        self.__power_down(self.address)
        return t

    def get_pressure(self):
        if self.precision:
            self.__set_higher_precision(self.address)
        self.__turn_on(self.address)
        self.__run_measurement(self.address)
        c = self.__check_measurement(self.address)
        while not c:
            c = self.__check_measurement(self.address)
        p = self.__read_pressure(self.address)
        self.__power_down(self.address)
        return p
    
    def custom(self, mode = 'r', register = 0x00, option = 1):
        if mode == 'r':
            res = self.i2c.readBytes(self.address, register, option)
            return res
        elif mode == 'w':
            self.i2c.writeByte(self.address, register, option)
            return 0
        else:
            raise TypeError('Unknown mode')
        
    def __string_to_int(self, hex_string):
        l = len(hex_string) - 1
        res = 0
        for h in hex_string:
            res += s_t_h[h] * (16 ** l)
            l -= 1
        return res

    def __deviceAdressCheck(self, address):
        res = self.i2c.readBytes(address, r_a_m["WHO_AM_I"], 1)[0]
        if res == 0xBB:
            return True
        else:
            return False

    def __power_down(self, address):
        self.i2c.writeByte(address, r_a_m["CTRL_REG1"], 0x00)

    def __set_higher_precision(self, address):
        self.i2c.writeByte(address, r_a_m["RES_CONF"], 0x7a)

    def __turn_on(self, address):
        self.i2c.writeByte(address, r_a_m["CTRL_REG1"], 0x84)

    def __run_measurement(self, address):
        self.i2c.writeByte(address, r_a_m["CTRL_REG2"], 0x01)

    def __check_measurement(self, address):
        r = self.i2c.readBytes(0x5c, r_a_m["CTRL_REG2"], 1)[0]
        if r == 0x00:
            return True
        else:
            sleep(1)
            self.__check_measurement(address)

    def __read_temperature(self, address):
        part1 = self.i2c.readBytes(address, r_a_m["TEMP_OUT_L"], 1)[0]
        part2 = self.i2c.readBytes(address, r_a_m["TEMP_OUT_H"], 1)[0]
        hex_string = '' + hex(part2)[2:] + hex(part1)[2:]
        raw_temp = self.__string_to_int(hex_string) - 32767
        temp_DegC = 42.5 + (raw_temp / (120 * 4))
        return temp_DegC

    def __read_pressure(self, address):
        part1 = self.i2c.readBytes(address, r_a_m["PRESS_OUT_XL"], 1)[0]
        part2 = self.i2c.readBytes(address, r_a_m["PRESS_OUT_L"], 1)[0]
        part3 = self.i2c.readBytes(address, r_a_m["PRESS_OUT_H"], 1)[0]
        hex_string = '' + hex(part3)[2:] + hex(part2)[2:] + hex(part1)[2:]
        raw_press = self.__string_to_int(hex_string)
        press_mBar = raw_press/4096
        return press_mBar
    
    def __working_check(self, address):
        c1 = self.__read_pressure(address)
        c2 = self.__read_pressure(address)
        c3 = self.__read_pressure(address)
        if c1 == c2 == c3 == (0x2f8000/4096):
            return True
        else:
            return False
