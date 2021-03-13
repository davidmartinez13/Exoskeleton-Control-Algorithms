from ModbusHandler import modbusHandler
from datetime import datetime
import time #the initial conditions are defined here:
mbClient = modbusHandler(Method = "rtu", Port = "/dev/ttyUSB0", Stopbits = 1 , Bytesize = 8, Parity = 'E', Baudrate = 460800)
gearRatio=11
enable=1
run=1
st0p=0
angle=8*gearRatio
angle1=-8*gearRatio
rpm=10
rpm2=2
smoothExt=10
smoothFlex=-10

def angMSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleMSB=angleArray[0]
 return angleMSB

def angLSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleLSB=angleArray[1]
 return angleLSB
def stop() :

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = st0p, uniT = 1) #run 
def stand() :

  mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
  mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
  mbClient.write_register(addresS = 40358, valuE =angMSB(90*10), uniT = 1)#angleMSB
  mbClient.write_register(addresS = 40359, valuE =angLSB(90*10), uniT = 1)#angleLSB
  mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
  mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run

def walk() :
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
 time.sleep(1)
 stop()
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

def plusreturn() : 
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm2, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
def minusreturn() : 
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm2, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(smoothFlex), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(smoothFlex), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run 

stand()
time.sleep(5)
while(1):
 
  result = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
  position= mbClient.modToFloat(result.registers[0],result.registers[1])*0.15
  result = mbClient.read_discrete_inputs(addresS =10001, counT = 10, uniT = 1)
  print (position)
  print(result.bits)
  button1=result.bits[0]

  if(position < 110 and position > 90):

    if button1 ==1:
       print("walk")
       walk()
       time.sleep(2)

  if(position >= 110):
      print("out of range")
      time.sleep(0.01)
      minusreturn()

  if(position<= 90):
      print("out of range")
      time.sleep(0.01)
      plusreturn()
