#!/bin/env python
#Evoke as: python -i <file-name>
import serial
import os, sys, time

import pyaudio
from scipy import fft
from numpy import short, fromstring
import math

from execproc import Monitor

s = serial.Serial()

stream = None
samples = 8
s_rate = 11000
def getFFT():
  global stream
  if stream is None:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=s_rate, input=True)

  audiodata = fromstring(stream.read(samples), dtype=short)
  #absdata = abs(audiodata) #Using amplitudes not freqs
  #avgAmp = [0] * 16
  #for i in range(16):
  #  extract = absdata[samples/16*i:samples/16*(i+1)]
  #  avgAmp[i] = 1.0 * sum(extract) / len(extract)
  #maxA = max(avgAmp)
  #normAmp = map(lambda x: int(math.ceil(x * 7.0 / maxA)), avgAmp)
  #return normAmp
  normalized_data = audiodata / 32768.0
  fft_data = fft(normalized_data)
  fft_max  = max(abs(fft_data))
  norm_fft = map(lambda x: int(math.ceil(x)), abs(fft_data) * 7 / fft_max)
  return norm_fft

def getDevice():
  global s
  paths = []
  for num in range(5):
    path = '/dev/ttyUSB%d' % num
    if os.path.exists(path):
      paths.append(path)

  arduLcd = ''
  for path in paths:
    s = serial.Serial(path, 9600)
    s.timeout = 4
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
  s.write(chr(n%256))

def customChars():
  global s
  for i in range(248, 256):
    writenum(s, i)
    p = 248 + 8 - i
    for c in range(p-1):
      writenum(s, 0)
    for c in range(8-p+1):
        writenum(s, 31)

def cls():
  """
  Clears LCD
  22: curoff, noblink
  23: curoff, blink
  24: curon, noblink
  25: curon, blink
  """
  global s
  writenum(s, 24)

def backlight(p):
  global s
  if p:
    writenum(s, 17)
  else:
    writenum(s, 18)

def goto(line, column):
  global s
  if line == 0:
    s.write(chr(128+column))
  else:
    s.write(chr(148+column))

def pl(st):
  global s
  st = st[:16]
  line = [' '] * 16
  for i in range(len(st)):
    line[i] = st[i]
  s.write(''.join(line))
  s.write('\r')

def repl():
  global s
  shell = Monitor('rohit')
  cls()
  while True:
    cpu, mem = map(float, shell.run("ps axo pcpu,pmem | awk '{sum += $0; pmem += $2} END {print sum/8, pmem}'").split(' '))
    if cpu > 100.0: cpu = 100 # Happens on Intel multicores
    temp = float(shell.run("""sensors | grep 'Core.*+' | awk '{print $3}' | sed 's/+//' | sed 's/.C//' | awk '{sum+=$0} END {print sum/4}'"""))
    goto(0,0)
    pl("%0.1f%% %0.1fG %0.1fC" % (cpu, mem*3.9/100,temp))
    sound_data = getFFT()
    goto(1,0)
    current_time = time.strftime("%H:%M:%S")
    for ch in current_time:
      s.write(ch)
    goto(1,8)
    for i in range(samples):
      writenum(s, sound_data[i])
    time.sleep(0.2)

dev = getDevice()
if dev == "":
  sys.exit()
s = serial.Serial(dev, 9600)
s.timeout = 1
s.readall()

customChars()
cls()
repl()

