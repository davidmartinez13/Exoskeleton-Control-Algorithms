from ModbusHandler import modbusHandler
from datetime import datetime
import time #the initial conditions are defined here:
mbClient = modbusHandler(Method = "rtu", Port = "/dev/ttyUSB0", Stopbits = 1 , Bytesize = 8, Parity = 'E', Baudrate = 460800)

enable=1
rpm=10
run=1
st0p=0
angle=50
angle1=-50



def angMSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleMSB=angleArray[0]
 return angleMSB

def angLSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleLSB=angleArray[1]
 return angleLSB

def rot() :

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run

def stop() :

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = st0p, uniT = 1) #run

def down() : #this function moves the leg down
#  time.sleep(5)#the exoskeleton keeps the position for 5 sec

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle1), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle1), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
# To.test.actuator.control,while.loop.shall.b.commented & rot.used W/rpm&angl
# rot()
while(1):
 result = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
 initial= mbClient.modToFloat(result.registers[0],result.registers[1])*0.5
 TRH=initial+3
 TRH1=initial-3
 time.sleep(0.8)
 result1 = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
 actual= mbClient.modToFloat(result1.registers[0],result1.registers[1])*0.5
 print(actual)
#  time.sleep(0.1)
 if(actual<=TRH1):
      print('down')
      down()
      time.sleep(0.4)
     #  stop()
 if(actual>=TRH):
      print('up')
      rot()
      time.sleep(0.4)
     #  stop()
 if(actual<TRH and actual>TRH1):
      print('stop')
      time.sleep(0.1)
      stop()

