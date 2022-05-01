from shutil import move
from time import process_time_ns, time
from turtle import color, distance, right
import cv2
import numpy as np
import math
from findpose import *
from graphdb import *
from statistics import mean
import csv
from csv import writer

frame_counter = 0

def findquery():
     query = "CREATE"
     

def trackxy(filename):
     global movement, frame_counter
     tracker = cv2.TrackerKCF_create()
     #tracker = cv2.TrackerGOTURN_create()
     video = cv2.VideoCapture(filename)
     fps = video.get(cv2.CAP_PROP_FPS)
     print("fps",fps)
     ok,frame=video.read()
     bbox = cv2.selectROI(frame)
     ok = tracker.init(frame,bbox)
     home = False
     color = "none"
     tempx, tempy, homex, homey = 0,0,0,0 
     frame_number, fingers_gap, left_elbows, right_elbows  = [] , [], [], []
     while True:
          frame_counter = frame_counter + 1
          ok,frame=video.read()
          if not ok:
               break
          ok,bbox=tracker.update(frame)
          if ok and home == False:
               (x,y,w,h)=[int(v) for v in bbox]
               cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
               cropi = frame[y:y+h, x:x+w]
               #cropi = frame[y,x]
               lowcolor = (0,0,255)
               highcolor =(128,128,255)
               lowb= np.array([78,158,124])
               uppb = np.array([138,255,255])
               thresh = cv2.inRange(cropi, lowb, uppb)
               average = cv2.mean(thresh)[0]
               print("average =",average)
               if average == 0:
                    color = "green"
               else:
                    color = "red"
               #print(cropi)
               #if cropi.size > 0 :
               #     cv2.imwrite("CroppedImage.jpg", cropi)
               homex, tempx = x , x
               homey, tempy = y , y
               #print(str(x)+"home"+str(y))
               home = True
          elif ok and home == True:
               (x,y,w,h)=[int(v) for v in bbox]
               x2 = x+w
               y2 = y+h
               cv2.rectangle(frame,(x,y),(x2,y2),(0,255,0),2,1)
               gap = math.hypot(tempx-x, tempy-y)
               tempx, tempy = x, y 
               image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               image.flags.writeable = False
               if gap > 1.0:
                    try:
                         frame_number.append(frame_counter)
                         left,right = findelbow(image)
                         left_elbows.append(left)
                         right_elbows.append(right)
                         ff = findfinger(image)
                         if(ff != None):
                              fingers_gap.append(ff)
                    except:
                         pass
               
          else:
               cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
          cv2.imshow('Full analysis',frame)
          if cv2.waitKey(1) & 0XFF==27:
             break
     cv2.destroyAllWindows()
     item_distance = math.hypot(tempx-homex, tempy-homey)
     cycletime = int((frame_number[-1]-frame_number[0])/fps)
     #print(fingers_gap)
     gap_ave = round(mean(fingers_gap),2)
     #print(gap_ave)
     max_le = max(left_elbows)
     min_le = min(left_elbows)
     max_ri = max(right_elbows)
     min_ri = min(right_elbows)
     #'redcoins','w_20','a_130','xy_100_100','c_1','d_130')
     #print(color, tempx,tempy,item_distance, cycletime, max_le,min_le,max_ri,min_ri,gap_ave)
     finxy = "xy_"+str(tempx)+'_'+str(tempy)
     gap_ave = "w_"+str(gap_ave)
     min_ri = "a_"+str(min_ri)
     cycletime = "c_"+str(cycletime)
     distance ="d_"+str(item_distance)
     print(color,gap_ave,min_le,finxy,cycletime, item_distance)
     return  color,gap_ave,min_le,finxy,cycletime, item_distance
     #return  color,tempx,tempy,item_distance, cycletime, max_le,min_le,max_ri,min_ri,gap_ave

if __name__ == '__main__':
     #f = open('test', 'w')
     data = trackxy("arrange_right2_45.mp4")
     headers = ['color', 'finalx','finaly','distance_moved', 'ctime', 'max_le','min_le','max_ri','min_ri','finger_gap']# = trackxy("arrange3.mp4")
     #rows = [{'finalx' : data[0],'finaly':data[1],'distance_moved' : data[2],'fctime':data[3],'max_le' : data[4],'min_le':data[5],
     #          'max_ri' : data[6],'min_ri':data[7], 'finger_gap' : data[8]}]
     with open('robot.csv', 'a', newline='') as f_object:  
          writer_object = writer(f_object)
          writer_object.writerow(data)  
          f_object.close()
     

     


