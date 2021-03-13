from ModbusHandler import modbusHandler
from datetime import datetime
import time
from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy

# The neural network is initialized
model = Sequential()
model.add(Dense(3, input_dim=3, activation='relu')) # input layer requires input_dim param
model.add(Dense(20, activation='relu'))
model.add(Dense(10, activation='relu'))

model.add(Dropout(.2))
model.add(Dense(3, activation='softmax'))

model.load_weights('weights2.h5')
# communication is stablished
mbClient = modbusHandler(Method = "rtu", Port = "/dev/ttyUSB0", Stopbits = 1 , Bytesize = 8, Parity = 'E', Baudrate = 460800)
gearRatio=11
enable=1
rpm=20
run=1
st0p=0
angle=20*gearRatio
angle1=-30*gearRatio
angleReturn=-120*gearRatio

def neural_Network(a,b,c):
 array1=numpy.array([[a,b,c]])
 predictions = model.predict(array1)
 # output our model's predictions.
 return predictions

def angMSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleMSB=angleArray[0]
 return angleMSB

def angLSB(a) :
 angleArray= mbClient.floatToMod(a)
 angleLSB=angleArray[1]
 return angleLSB

def up() :#this function moves the leg up
 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run

def stop() :#this function stops the leg

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = st0p, uniT = 1) #run

def down() : #this function moves the leg down

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angle1), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angle1), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run
 
def Return() :#this function moves the to origin

 mbClient.write_register(addresS = 40356, valuE = enable, uniT = 1) #enable
 mbClient.write_register(addresS = 40357, valuE =rpm, uniT = 1) #rpm
 mbClient.write_register(addresS = 40358, valuE =angMSB(angleReturn), uniT = 1)#angleMSB
 mbClient.write_register(addresS = 40359, valuE =angLSB(angleReturn), uniT = 1)#angleLSB
 mbClient.write_register(addresS = 40360, valuE = 2, uniT = 1)#mode
 mbClient.write_register(addresS = 40361, valuE = run, uniT = 1) #run

while(1):

    result = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
    deg=mbClient.modToFloat(result.registers[0],result.registers[1])
    time.sleep(1)
    result2 = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
    deg2=mbClient.modToFloat(result2.registers[0],result2.registers[1])
    teta=deg2-deg
    print(deg)

    result = mbClient.read_discrete_inputs(addresS =10001, counT = 10, uniT = 1)
    button1=result.bits[0]
    button2=result.bits[3]
    out_array=[result.bits[0],result.bits[3],teta]
    print(out_array)
    predicted=neural_Network(button1,button2,teta)
    print(predicted)
    action=numpy.argmax(predicted)
    print(action)

    if(action==0):
      print('down')
      down()
      time.sleep(2)

    if(action==1):
      print('up')
      up()
      time.sleep(2)

    if(action==2):
      print('stop')
      stop()

# code for simplified leg rises
# while(1):
#  result = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
#  initial= mbClient.modToFloat(result.registers[0],result.registers[1])*0.5
#  TRH=initial+15)
#  result1 = mbClient.read_holding_registers(addresS =40350, counT = 2, uniT = 1)
#  actual= mbClient.modToFloat(result1.registers[0],result1.registers[1])*0.5
#  print(actual)

#  if(actual>=120):
#       print('down')
#       time.sleep(5)
#       Return()
#       time.sleep(2)
#  if(actual<120):
#      if(actual>=TRH):
#       print('up')
#       up()
#       time.sleep(1)