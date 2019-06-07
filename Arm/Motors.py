import dynamixel_sdk as DXLSDK
from Dxl_Register import Dxl_Register as Register

class MotorBase(object):
    baud2reg = {
        9600:0,
        57600:1,
        115200:2,
        1000000:3,
        2000000:4,
        3000000:5,
        4000000:6,
        4500000:7
    }
    
    baudfromreg = {
        0:9600,
        1:57600,
        2:115200,
        3:1000000,
        4:2000000,
        5:3000000,
        6:4000000,
        7:4500000
    }
    
    port = None
    packetHandler  = None
    
     # Control table address
    #EEPROM
    ID_REG = None
    BAUDRATE = None
    MAX_POS = None
    MIN_POS = None
    
    #RAM
    TORQUE_ENABLE = None
    LED = None
    GOAL_POSITION = None
    PRESENT_LOAD = None
    PRESENT_POSITION = None
    PRESENT_TEMP = None
    
class Motor1(MotorBase):
    
    def __init__(self, ID, portHandler, reverse=False, baudrate="57600"):
        self.port              = portHandler
        self.packetHandler     = DXLSDK.PacketHandler(1.0)
        self.ID                = ID
        
        # Control table address
        #EEPROM
        self.ID_REG            = Register(self.packetHandler, 3, 1, 252)  #ID 254 is broadcast               
        self.BAUDRATE          = Register(self.packetHandler, 4, 1, 7)
        self.MAX_POS           = Register(self.packetHandler, 8, 2, 1023)
        self.MIN_POS           = Register(self.packetHandler, 6, 2, 1023)
        
        #RAM
        self.TORQUE_ENABLE     = Register(self.packetHandler, 24, 1, 1)
        self.LED               = Register(self.packetHandler, 25, 1, 1)
        self.GOAL_POSITION     = Register(self.packetHandler, 30, 2, 1023)
        self.MOVING_SPEED      = Register(self.packetHandler, 32, 2, 2047)
        self.PRESENT_LOAD      = Register(self.packetHandler, 40, 2, 1023, writeable=False)
        self.PRESENT_POSITION  = Register(self.packetHandler, 36, 2, 4095, writeable=False)
        self.PRESENT_TEMP      = Register(self.packetHandler, 43, 1, 99, writeable=False)
        
        
        if reverse is not "init":
            minPos                 = self.read(self.MIN_POS)
            maxPos                 = self.read(self.MAX_POS)
            self.minPos            = minPos if minPos is not None else 0
            self.maxPos            = maxPos if maxPos is not None else 1264095
        
        print((self.setDriveMode(Reversed=reverse)))
        
        
    def setDriveMode(self, WheelMode=False, Reversed=False):
        if WheelMode:
            self.write(self.MIN_POS, 0)
            self.write(self.MAX_POS, 0)
            
        
            
    def status(self):
        return "ID: %, reversed: %" % (self.read(self.ID), self.read(self.DRIVE_MODE)&1)
            
    def hasError(self):
        return self.read(self.ERROR) != 0
    
    def printErrors(self):
       pass
        
    def enable(self):
        return self.write(self.TORQUE_ENABLE, 1) == 1
    
    def disable(self):
        return self.write(self.TORQUE_ENABLE, 0) == 1
    
    def isenabled(self):
        return self.read(self.TORQUE_ENABLE)
    
    def write(self, register, data):
        if self.port.getBaudRate() != self.BAUDRATE:
            self.port.setBaudRate(self.BAUDRATE)
        dxl_comm_result, dxl_error = register.write(int(data), self.ID, self.port)
        return self.commResult(dxl_comm_result, dxl_error)
    
    def commResult(self, result, error):
        if result != DXLSDK.COMM_SUCCESS:
           return 0
        elif error != 0:
            return -1
        else:
            return 1
    
    def read(self, register):
        if self.port.getBaudRate() != self.BAUDRATE:
            self.port.setBaudRate(self.BAUDRATE)
        data, comm_result, error = register.read(self.ID, self.port)
        if(comm_result == DXLSDK.COMM_SUCCESS and error==0):
            return data
        else:
            return None
        
    def currentPos(self, convert2Deg=True):
        pos = self.read(self.PRESENT_POSITION)
        if pos is None:
            return -99999
        elif convert2Deg:
            return Pos2Deg(pos)
        else:
            return pos
        
    def getGoalPos(self, convert2Deg=True):
        pos = self.read(self.GOAL_POSITION)
        if pos is None:
            return -99999
        elif convert2Deg:
            return Pos2Deg(pos)
        else:
            return pos
    
    def setGoalPos(self, goal, Deg=True):
        if Deg:
            goal=Deg2Pos(goal)
        if goal <= self.maxPos and goal >= self.minPos:
            return self.write(self.GOAL_POSITION, goal)
        return -1
    
    def setPosBounds(self, minPos, maxPos, Deg=True):
        if Deg:
            minPos = Deg2Pos(minPos)
            maxPos = Deg2Pos(maxPos)
        count = 0
        if self.write(self.MIN_POS, minPos)==1:
            self.minPos = minPos
            count+=1
        if self.write(self.MAX_POS, maxPos)==1:
            self.maxPos = maxPos
            count+=1
        return count==2
    
    def reboot(self):
        dxl_comm_result, dxl_error = self.packetHandler.reboot(self.portHandler, self.ID)
        return self.commResult(dxl_comm_result, dxl_error)
        

class Motor2(MotorBase):
    
    def __init__(self, ID, portHandler, reverse=False, baudrate="57600"):
        self.port              = portHandler
        self.packetHandler     = DXLSDK.PacketHandler(2.0)
        self.ID                = ID
        
        # Control table address
        #EEPROM
        self.ID_REG            = Register(self.packetHandler, 7, 1, 253)  #ID 253 is broadcast               
        self.BAUDRATE          = Register(self.packetHandler, 8, 1, 7)
        self.DRIVE_MODE         = Register(self.packetHandler, 10, 1, 256)
        self.OPERATING_MODE    = Register(self.packetHandler, 11, 1, 16)
        self.MAX_POS           = Register(self.packetHandler, 48, 4, 4095)
        self.MIN_POS           = Register(self.packetHandler, 52, 4, 4095)
        
        #RAM
        self.TORQUE_ENABLE     = Register(self.packetHandler, 64, 1, 1)
        self.LED               = Register(self.packetHandler, 65, 1, 1)
        self.ERROR             = Register(self.packetHandler, 70, 1, 255, writeable=False)
        self.GOAL_POSITION     = Register(self.packetHandler, 116, 4, 4095)
        self.PRESENT_LOAD      = Register(self.packetHandler, 126, 2, 1000, minVal=-1000, writeable=False)
        self.PRESENT_POSITION  = Register(self.packetHandler, 132, 4, 4095, writeable=False)
        self.PRESENT_TEMP      = Register(self.packetHandler, 146, 1, 256, writeable=False)
        
        
        if reverse is not "init":
            minPos                 = self.read(self.MIN_POS)
            maxPos                 = self.read(self.MAX_POS)
            self.minPos            = minPos if minPos is not None else 0
            self.maxPos            = maxPos if maxPos is not None else 4095
        
        print((self.setDriveMode(Reversed=reverse)))
        
        
    def setDriveMode(self, ProfileConfiguration=None, Reversed=None):
        if Reversed is "init":
            return "MG init"
        data = 0
        if   (ProfileConfiguration is None or Reversed is None): 
            if ((Reversed is None) and (ProfileConfiguration is None)):
                return 0b1101011
            else:
                data =self.read(self.DRIVE_MODE)
                print(("ID: %d OG: %s \t" % (self.ID, bin(data))))
                
            
        if ProfileConfiguration is "toggle":
            data = data^(1<<2)
        elif ProfileConfiguration is not None:
            data = data & ~(1<<2) | ProfileConfiguration<<2
            
        if Reversed is "toggle":
            data = data^1
        elif Reversed is not None:
            data = data & ~(1) | Reversed
        print(("sent\t%s" % bin(data)))
        return bin(data) if self.write(self.DRIVE_MODE, data)==1 else bin(255)
        
            
    def status(self):
        return "ID: %, reversed: %" % (self.read(self.ID), self.read(self.DRIVE_MODE)&1)
            
    def hasError(self):
        return self.read(self.ERROR) != 0
    
    def printErrors(self):
        errors = self.read(self.ERROR)
        if errors == 0:
            return
        print(("Error on Dynamixel ID: %d \n" % self.ID))
        if errors is None:
            print("\tUnable to Read Errors")
        if(errors == 0b00110100):
            print("\tDefault Error")
            return
        if(errors & 1) != 0:
            print("\tInput Voltage Error\n")
        if(errors>>2 & 1):
            print("\tOverHeating Error\n")
        if(errors>>3 & 1):
            print("\tMotor Encoder Error\n")
        if(errors>>4 & 1):
            print("\tElectrical Shock Error\n")
        if(errors>>5 & 1):
            print("\tOverload Error\n")
        
    def enable(self):
        return self.write(self.TORQUE_ENABLE, 1) == 1
    
    def disable(self):
        return self.write(self.TORQUE_ENABLE, 0) == 1
    
    def isenabled(self):
        return self.read(self.TORQUE_ENABLE)
    
    def write(self, register, data):
        if self.port.getBaudRate() != self.BAUDRATE:
            self.port.setBaudRate(self.BAUDRATE)
        dxl_comm_result, dxl_error = register.write(int(data), self.ID, self.port)
        return self.commResult(dxl_comm_result, dxl_error)
    
    def commResult(self, result, error):
        if result != DXLSDK.COMM_SUCCESS:
           return 0
        elif error != 0:
            return -1
        else:
            return 1
    
    def read(self, register):
        if self.port.getBaudRate() != self.BAUDRATE:
            self.port.setBaudRate(self.BAUDRATE)
        data, comm_result, error = register.read(self.ID, self.port)
        if(comm_result == DXLSDK.COMM_SUCCESS and error==0):
            return data
        else:
            return None
        
    def currentPos(self, convert2Deg=True):
        pos = self.read(self.PRESENT_POSITION)
        if pos is None:
            return -99999
        elif convert2Deg:
            return Pos2Deg(pos)
        else:
            return pos
        
    def getGoalPos(self, convert2Deg=True):
        pos = self.read(self.GOAL_POSITION)
        if pos is None:
            return -99999
        elif convert2Deg:
            return Pos2Deg(pos)
        else:
            return pos
    
    def setGoalPos(self, goal, Deg=True):
        if Deg:
            goal=Deg2Pos(goal)
        if goal <= self.maxPos and goal >= self.minPos:
            return self.write(self.GOAL_POSITION, goal)
        return -1
    
    def setPosBounds(self, minPos, maxPos, Deg=True):
        if Deg:
            minPos = Deg2Pos(minPos)
            maxPos = Deg2Pos(maxPos)
        count = 0
        if self.write(self.MIN_POS, minPos)==1:
            self.minPos = minPos
            count+=1
        if self.write(self.MAX_POS, maxPos)==1:
            self.maxPos = maxPos
            count+=1
        return count==2
    
    def reboot(self):
        dxl_comm_result, dxl_error = self.packetHandler.reboot(self.portHandler, self.ID)
        return self.commResult(dxl_comm_result, dxl_error)



class MotorGroup(MotorBase):
    def __init__(self, motors, motorType):
        self.motors = list(motors)
    
    
    def setDriveMode(self, ProfileConfiguration=None, Reversed=None):
        for m in self.motors:
            m.setDriveMode(ProfileConfiguration=ProfileConfiguration, Reversed=Reversed)
        
    def hasError(self):
        return any(list([motor.hasError() for motor in self.motors]))
    
    def printErrors(self):
        for m in self.motors:
            m.printErrors()
        
    def enable(self):
        return self.write(self.TORQUE_ENABLE, 1)
    
    def disable(self):
        return self.write(self.TORQUE_ENABLE, 0)
    def isenabled(self):
        return self.read(self.TORQUE_ENABLE)
    
    def write(self, register, data):
        return list([motor.write(register, data) for motor in self.motors])
    
    def read(self, register):
        return list([motor.read(register) for motor in self.motors])
    
    def currentPos(self, convert2Deg=True):
        return list([motor.currentPos(convert2Deg=convert2Deg) for motor in self.motors])
        
    def getGoalPos(self, convert2Deg=True):
        return list([motor.getGoalPos(convert2Deg=convert2Deg) for motor in self.motors])
    
    def setGoalPos(self, goal, Deg=True):
        return list([motor.setGoalPos(goal, Deg=Deg) for motor in self.motors])
    
    def setPosBounds(self, minPos, maxPos, Deg=True):
        return list([motor.setPosBounds(minPos, maxPos, Deg=Deg) for motor in self.motors])


def Deg2Pos(deg):
    return (deg/0.088+2048)

def Pos2Deg(pos):
    return ((pos-2048)*0.088)