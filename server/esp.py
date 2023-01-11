from machine import UART
import utime,time


class esp:
    baudrate = 115200              # Default Baud rate of ESP8266
    uart = None

    def __init__(self):
        self.uart = UART(1, self.baudrate)
        self.uart.write('+++')
        time.sleep(1)
        if(self.uart.any()>0):
            self.uart.read()

    def sendCMD(self, cmd,ack,timeout=2000):
        lst = []
        self.uart.write(cmd+'\r\n')
        t = utime.ticks_ms()
        while (utime.ticks_ms() - t) < timeout:
            s=self.uart.read()
            if(s != None):
                s=s.decode()
                lst.append(s)
                if(s.find(ack) >= 0):
                    return True, lst
        return False, None


    def sendData(self, ID, data):
        self.sendCMD( 'AT+CIPSEND=' + str(ID) + ','+str(len(data)),'>')
        self.uart.write(data)
        foo = data=self.uart.read()
        time.sleep(1)
        self.sendCMD('AT+CIPCLOSE='+str(ID),"OK")

    def ReceiveData(self):
        data=self.uart.read()
        if(data != None):
            data=data.decode()
            if(data.find('+IPD') >= 0):
                n1=data.find('+IPD,')
                n2=data.find(',',n1+5)
                ID=int(data[n1+5:n2])
                n3=data.find(':')
                data=data[n3+1:]
                return ID,data
        return None,None

    def ReceiveHttp(self):
        data = ''
        while(self.uart.any()):
            data = data + self.uart.read().decode()
        if(data != ''):
            if(data.find('+IPD') >= 0):
                n1=data.find('+IPD,')
                n2=data.find(',',n1+5)
                ID=int(data[n1+5:n2])
                n3=data.find(':')
                data=data[n3+1:]
                return ID,data
        return None,None

    def initWifi(self, ssid, pwd):
        self.sendCMD("AT","OK")
        self.sendCMD("AT+CWMODE_CUR=1","OK")
        self.sendCMD("AT+CWJAP=\""+ssid+"\",\""+pwd+"\"","OK",20000)
        self.sendCMD("AT+CIPMUX=1","OK")

    def initServer(self, Port):
        self.sendCMD("AT+CIPSERVER=1,"+Port,"OK")
        success, data = self.sendCMD("AT+CIFSR","OK")
        if(success == None):
            return None
        return self.parseServerIp(data)

    def parseServerIp(self, lst):
        res = str(lst)[1:-1]
        x = res.split(",")
        x = x[1].replace('"',"")
        x = x.split("+")
        ip = x[0][:-4]
        return ip
