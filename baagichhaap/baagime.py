#!/usr/bin/env python
# baagichhaap: Takes your decent photo and makes it Baagi!
# dependency: opencv
# author: bhaisahab

import sys, os
from opencv.cv import *
from opencv.highgui import *

def detectObjects(imagePath, debug=False):
  image = cvLoadImage(imagePath)
  if debug:
    import cv
    oimage = cv.LoadImage(imagePath, cv.CV_LOAD_IMAGE_COLOR)

  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)

  cascade = cvLoadHaarClassifierCascade(
    'haarcascade_frontalface_default.xml',
    cvSize(1,1))
  faces = cvHaarDetectObjects(image, cascade, storage, 1.1, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))

  moochstr = ""
  if not faces:
    return

  for f in faces:
    if debug: cv.Rectangle(oimage, (f.x, f.y), (f.x+f.width, f.y+f.height), cv.CV_RGB(255,0,0))
    img = cvGetSubRect(image, f)
    cascade = cvLoadHaarClassifierCascade('haarcascade_mcs_mouth.xml', cvSize(1,1))
    mouths = cvHaarDetectObjects(img, cascade, storage, 1.1, 3, 0, cvSize(30,30))
    cascade = cvLoadHaarClassifierCascade('haarcascade_mcs_nose.xml', cvSize(1,1))
    noses = cvHaarDetectObjects(img, cascade, storage, 1.1, 3, 0, cvSize(20,15))

    if mouths[0] != None and noses[0] != None:
      nose = noses[0]
      mouth = mouths[0]

      for n in noses:
        if debug: cv.Rectangle(oimage, (f.x+n.x, f.y+n.y), (f.x+n.x+n.width, f.y+n.y+n.height), cv.CV_RGB(0,0,255))
        if n.y+n.height >= nose.y+nose.height:
          nose = n

      for m in mouths:
        if debug: cv.Rectangle(oimage, (f.x+m.x, f.y+m.y), (f.x+m.x+m.width, f.y+m.y+m.height), cv.CV_RGB(0,255,0))
        if m.y > nose.y:
          mouth = m
          break

      if mouth.y < nose.y:
        mouth = nose
        mouth.y += nose.height/2

      moochw, moochh = f.width, 400*f.width/1600
      moochx, moochy = f.x + (mouth.x + mouth.width/2 + nose.x + nose.width/2)/2 - moochw/2, f.y + (nose.y + nose.height + mouth.y + mouth.height/3)/2 - moochh/2
      moochstr += """ -draw 'image SrcOver %d,%d %d,%d mooch.png'""" % (moochx, moochy, moochw, moochh)

  if moochstr == "": return
  os.system("convert %s '%s' '%s'" % (moochstr, imagePath, imagePath))

  if debug:
    windown = "baagichaap"
    cv.NamedWindow(windown, 1)
    cv.ShowImage(windown, oimage);
    cv.WaitKey(0);

def main():
  detectObjects(sys.argv[1], len(sys.argv) > 2)

if __name__ == "__main__":
  main()
