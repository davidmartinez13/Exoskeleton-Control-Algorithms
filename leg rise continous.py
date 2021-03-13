from ModbusHandler import modbusHandler
from datetime import datetime
import time #the initial conditions are defined here:
mbClient = modbusHandler(Method = "rtu", Port = "/dev/ttyUSB0", Stopbits = 1 , Bytesize = 8, Parity = 'E', Baudrate = 460800)

enable=1
rpm=40
run=1
st0p=0
angle=300
angle1=-300
rpm2=10
smoothExt=20
smoothFlex=-20
# enable=1
# rpm=10
# run=1
# st0p=0
# angle=30
# angle1=-30
# rpm2=5
# smoothExt=10
# smoothFlex=-10

def angMSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleMSB=angleArray[0]
 return angleMSB

def angLSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleLSB=angleArray[1]
 return angleLSB

def extend() :

  mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
  mbClient.write_register(addresS = 40357, valuE =rpm2, uniT = 1) #rpm
  mbClient.write_register(addresS = 40358, valuE =angMSB(smoothExt), uniT = 1)#angleMSB
  mbClient.write_register(addresS = 40359, valuE =angLSB(smoothExt), uniT = 1)#angleLSB
  mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
  mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
  time.sleep(0.0001)
  stop()
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

def flex() : 
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm2, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(smoothFlex), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(smoothFlex), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
 time.sleep(0.0001)
 stop()
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle1), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle1), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
def smooth() : 
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm2, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(smoothFlex), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(smoothFlex), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run


while(1):
 
  result = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
  position= mbClient.modToFloat(result.registers[0],result.registers[1])*0.3
  result = mbClient.read_discrete_inputs(addresS =10001, counT = 10, uniT = 1)
  print (position)
  print(result.bits)
  button1=result.bits[0]
  button2=result.bits[3]

  if(position <= 280):

      if button1 ==1:
       print("extend")
       extend()
       
      if button2==1:
       print("flex")
       flex()
       
  if(position >=160):
      time.sleep(0.01)
      smooth()
 

 
