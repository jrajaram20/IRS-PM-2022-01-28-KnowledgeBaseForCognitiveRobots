from email import header
from urllib.robotparser import RobotFileParser
from graphdb import *
from Robotserver import *
from tp_final import *
import time
from chatbot import *
from bodypose_analyze import *
from handpose_analyze import *
from tp_final import *
import csv

class TaskRecommender:
    def __init__(self):
        print("")
    
    #def startserver(self,host,port):
    
    def createdb(self,db):
        db.clearDB()
        db.createDB()

    def analyzer(self,db, robot, msg):
        if(msg == "getredcoins"):
            color = "red"
            r_color = ""
            robot.senddata(msg)
            r_color = robot.rcvdata()
            if(r_color!= "none"):
                if(color== r_color):
                    print("----Found matching color")
                    print("----querying database for drop location and gripper position")
                    place_pos = db.queryplaceforcolor(color)
                    gap = str(80-20)
                    #print(place_pos)
                    (print("---sending data to robot"))
                    robot.senddata(place_pos+"_"+gap)
                    r_data = robot.rcvdata()
                    while r_data != "ack":
                        robot.senddata(place_pos)
                        r_data = robot.rcvdata()
                else:
                    print("unable to find matching database")
            
            else:
                print("unable to find red color items")
        elif(msg == "getblackbox"):
            color = "black"
            r_color = ""
            robot.senddata(msg)
            r_color = robot.rcvdata()
            if(r_color!= "none"):
                if(color== r_color):
                    print("----Found matching color")
                    print("----querying database for drop location and gripper position")
                    place_pos = db.queryplaceforcolor(color)
                    gap = str(80-40)
                    print(place_pos)
                    (print("---sending data to robot"))
                    robot.senddata(place_pos+"_"+gap)
                    r_data = robot.rcvdata()
                    while r_data != "ack":
                        robot.senddata(place_pos)
                        r_data = robot.rcvdata()
                else:
                    print("unable to find matching database")
            
            else:
                print("unable to find red color items")

                #robot.senddata("ack")
            #db.queryplaceforcolor(self,value)


if __name__ == "__main__":
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "admin"
    host = '192.168.1.3'
    port = 5000
    file = "coin1.mp4"
    #trackxy(file)
    print("----Starting Server")
    robot = Robot(host, port)
    print("----Connecting to neo4j")
    dbapp = Recommender(uri, user, password)
    task = TaskRecommender()
    print("----waiting for intent prediction")
    #bot_response = chat()
    bot_response = "getredcoins"
    if(bot_response == "analyze_body"): 
        hand = handpose(file)      
    elif(bot_response == "analyze_hand"):
        hand = handpose(file)
    elif(bot_response == "analyze_full"):
        headers = ['color',' finalx','finaly','distance_moved', 'ctime', 'max_le','min_le','max_ri','min_ri','finger_gap']
        with open('robot.csv', 'a', newline='') as f_object:  
          writer_object = writer(f_object)
          data = trackxy(file)
          writer_object.writerow(data)  
          f_object.close()
        #update db
    else:
        task.analyzer(dbapp, robot, bot_response)
        
