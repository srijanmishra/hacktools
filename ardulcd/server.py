#!/bin/env python
#Evoke as: python -i <file-name>
import serial
import os, sys, time

from execproc import Monitor

def getDevice():
  paths = []
  for num in range(5):
    path = '/dev/ttyUSB%d' % num
    if os.path.exists(path):
      paths.append(path)

  arduLcd = ''
  for path in paths:
    s = serial.Serial(path, 9600)
    s.timeout = 1
    s.readall()
    s.write('~')
    payload = s.read()
    if payload == '\\':
      arduLcd = path
      s.close()
      break
    s.close()
  return arduLcd

def writenum(s, n):
  s.write(chr(n))

def cls(s):
  """
  Clears LCD
  22: curoff, noblink
  23: curoff, blink
  24: curon, noblink
  25: curon, blink
  """
  writenum(s, 24)

def backlight(s, p):
  if p:
    writenum(s, 17)
  else:
    writenum(s, 18)

def goto(s, line, column):
  if line == 0:
    s.write(128+column)
  else:
    s.write(148+column)

dev = getDevice()
if dev == "":
  sys.exit()
s = serial.Serial(dev, 9600)
print "Serial connection established with %s at 9600 baud" % dev
s.timeout = 2
s.readall()

cls(s)
cls(s)
cls(s)

def pl(st):
  st = st[:16]
  line = [' '] * 16
  for i in range(len(st)):
    line[i] = st[i]
  s.write(''.join(line))
  s.write('\r')

pl("Rohit Yadav")
pl("antrix.yaan.in")
shell = Monitor('rohit')
while True:
  mem = float(shell.run("ps aux | grep -v MEM | awk '{sum += $4} END {print sum}'"))
  cpu = float(shell.run("ps aux | grep -v CPU | awk '{sum += $3} END {print sum/8}'"))
  temp = float(shell.run("""sensors | grep 'Core.*+' | awk '{print $3}' | sed 's/+//' | sed 's/.C//' | awk '{sum+=$0} END {print sum/4}'"""))
  print mem, cpu, temp
  pl("CPU:%0.2f @ %0.1fC" % (cpu, temp))
  pl("Mem:%0.2fGB" % (mem*4/100))
  time.sleep(2)
