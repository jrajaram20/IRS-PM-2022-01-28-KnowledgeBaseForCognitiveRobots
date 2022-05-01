from email import header
from urllib.robotparser import RobotFileParser
from graphdb import *
from socket_server import *
from tp_final import *
import time
from chatbot import *
from bodypose_analyze import *
from handpose_analyze import *
import csv
import pyttsx3

engine = pyttsx3.init() 

class TaskRecommender:
    def __init__(self):
        print("")
    
    #def startserver(self,host,port):
    
    def createdb(self,db):
        db.clearDB()
        db.createDB()

    def analyzer(self,db, robot, msg):
        if(msg == "pickredcoins"):
            color = "red"
            r_color = ""
            engine.say("sending message to robot")
            engine.runAndWait()
            robot.senddata(msg)
            r_color = robot.rcvdata()
            if(r_color!= "none"):
                if(color== r_color):
                    engine.say("item identified")
                    engine.runAndWait()
                    print("----Found matching color")
                    print("----Getting recommendation from database for drop location and gripper position")
                    engine.say("Getting recommendation from database for drop location and gripper position")
                    engine.runAndWait()
                    place_pos = db.queryplaceforcolor(color)
                    gripperwidth = db.querygripperwidth(color) # 
                    #print(place_pos)
                    engine.say("Drop location is "+place_pos)
                    engine.runAndWait()
                    engine.say("Gripper width "+gripperwidth)
                    engine.runAndWait()
                    (print("---sending data to robot"))
                    robot.senddata(place_pos+"_"+gripperwidth)
                    r_data = robot.rcvdata()
                    while r_data != "ack":
                        robot.senddata(place_pos)
                        r_data = robot.rcvdata()
                else:
                    engine.say("data unavailable in database")
                    engine.runAndWait()
                    print("unable to find matching database")
            
            else:
                engine.say("unable to find redcoins")
                engine.runAndWait()
                print("unable to find red color items")
        elif(msg == "pickblackbox"):
            color = "black"
            r_color = ""
            engine.say("sending message to robot")
            engine.runAndWait()
            robot.senddata(msg)
            r_color = robot.rcvdata()
            if(r_color!= "none"):
                if(color== r_color):
                    engine.say("item identified")
                    engine.runAndWait()
                    print("----Found matching color")
                    print("----querying database for drop location and gripper position")
                    engine.say("Querying database for drop location and gripper position")
                    engine.runAndWait()
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
                    engine.say("data unavailable in database")
                    engine.runAndWait()
                    print("unable to find matching database")
            
            else:
                engine.say("unable to find black box")
                engine.runAndWait()
                print("unable to find black color items")

                #robot.senddata("ack")
            #db.queryplaceforcolor(self,value)


if __name__ == "__main__":

    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "admin"
    host = '192.168.1.3' 
    port = 5000
    file = "video.mp4"

    #trackxy(file)
    print("----Starting system")
    engine.say("starting the system")
    engine.runAndWait()
    engine.say("connecting to client")
    engine.runAndWait()
    robot = robot(host, port)
    engine.say("connecting to database")
    engine.runAndWait()
    dbapp = Recommender(uri, user, password)
    task = TaskRecommender()
    while True:
        engine.say("waiting for voice command")
        engine.runAndWait()
        print("----waiting for voice command")
        bot_response = chat()
        #bot_response = "getredcoins"
        if(bot_response == "analyze_body"): 
            engine.say("will do body pose analysis")
            engine.runAndWait()
            hand = bodypose(file)      
        elif(bot_response == "analyze_hand"):
            engine.say("will do hand pose analysis")
            engine.runAndWait()
            hand = handpose(file)
        elif(bot_response == "analyze_all"):
            engine.say("will do full video analysis")
            engine.runAndWait()
            headers = ['color',' finalx','finaly','distance_moved', 'ctime', 'max_le','min_le','max_ri','min_ri','finger_gap']
            with open('robot.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                engine.say("Please select the item from the video shown")
                engine.runAndWait()
                data = trackxy(file)
                writer_object.writerow(data)  
                f_object.close()
                engine.say("updating database now")
                engine.runAndWait()
                app.update('redcoins','w_20','a_130','xy_100_100','c_1','d_130')
                dbapp.update('redcoins','finger')
        elif(bot_response == "pickredcoins"):
            engine.say("will pickup red coins")
            engine.runAndWait()
            task.analyzer(dbapp, robot, bot_response)
        elif(bot_response == "pickblackbox"):
            engine.say("will pickup blackbox")
            engine.runAndWait()
            task.analyzer(dbapp, robot, bot_response)
        elif(bot_response == "goodbye"):
            engine.say("goodbye")
            engine.runAndWait()
            print("Stopping the system")
            break
        else:
            engine.say(bot_response)
            engine.runAndWait()
