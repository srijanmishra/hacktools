#!/bin/env python
#Evoke as: python -i <file-name>
import serial
import os, sys, time

import gtop

import pyaudio
from scipy import fft
from numpy import short, fromstring
import math

from execproc import Monitor

s = serial.Serial()

stream = None
samples = 4
s_rate = 11000
def getFFT():
  global stream
  if stream is None:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=s_rate, input=True)

  audiodata = fromstring(stream.read(samples*16), dtype=short)
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
  writenum(s, 22)

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
  line = [' '] * len(st)
  for i in range(len(st)):
    line[i] = st[i]
  s.write(''.join(line))

def repl():
  global s
  shell = Monitor('rohit')
  cls()
  curEpocs1 = time.time()
  curEpocs2 = time.time()
  lastBytes = 0
  while True:
    cpu, mem = map(float, shell.run("ps axo pcpu,pmem | awk '{sum += $0; pmem += $2} END {print sum/8, pmem}'").split(' '))
    #cpu = 0
    #for core in gtop.cpu().cpus:
    #  cpu += 100.0 * (core.user+core.sys) / core.total
    #print cpu
    #cpu /= 8
    if cpu > 100.0: cpu = 100 # Happens on Intel multicores
    mem = 1.0 * gtop.mem().user / gtop.mem().total * (gtop.mem().total/1024.0/1024.0/1024.0)#3.98
    temp = float(shell.run("""sensors | grep 'Core.*+' | awk '{print $3}' | sed 's/+//' | sed 's/.C//' | awk '{sum+=$0} END {print sum/4}'"""))
    netload = gtop.netload('eth0')
    curEpocs2 = time.time()
    net = (netload.bytes_total - lastBytes) / (curEpocs2 - curEpocs1) / 1024 #kbps
    lastBytes = netload.bytes_total
    curEpocs1 = curEpocs2
    if net > 999:
      net /= 1024
      netstr = "%.1fM" % net
    else:
      netstr = "%.1fK" % net

    goto(0,0)
    pl("%.1f " % cpu)
    goto(0, 5)
    pl("%0.1fG" % mem)
    goto(0,10)
    pl(netstr.zfill(6))
    goto(1,0)
    pl(time.strftime("%H%M:%S"))
    goto(1,11)
    pl("%0.1fC" % temp)
    goto(1,7)
    sound_data = getFFT()
    for i in range(samples):
      writenum(s, sound_data[i])
    time.sleep(0.4)

dev = getDevice()
if dev == "":
  sys.exit()
s = serial.Serial(dev, 9600)
s.timeout = 1
s.readall()

customChars()
cls()
repl()

