## SECTION 1 : PROJECT TITLE
## Cognitive robots to imitate human action using knowledge base system

<img src="Miscellaneous/clips/static/robotarm.jpg"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT


In recent years with artificial intelligence (AI), it has been shown that the usability of machines is enhanced when they become capable to process data, finding patterns, and suggesting proper actions. In this project, a model for semantic memory is used that allows machines to collect information and experiences to become more proficient with time. By analysing the image data, the processed information is stored in the knowledge graph which is then used to comprehend the work instructions expressed in natural language. This imparts industrial robots’ behaviour to execute the required tasks in a deterministic manner.
Programming these robots or replicating their tasks onto another robot requires a lot of effort. A typical robotic application requires a specialist to break down the complicated task into smaller sub-tasks and actions. The expert writes detailed instructions in the form of robot programs to make the robot accomplish the desired task. This process needs a high level of expertise and is time-consuming. With the shortages in skilled manpower and resources to train the workforce, it is important we need to capture the factory process into a knowledge base system. The future factory automation process will depend on the task-oriented knowledge graph 

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
|Jayaraman Rajaram | G****196U | Complete Project| ------- |


---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

Google Drive link : 


---

## SECTION 5 : USER GUIDE

The code can be executed from python environment. Below is the software requirement 
•	mediapipe
•	pyttsx3
•	nltk
•	speechrecognition
•	neo4j
•	opencv-python
•	tensorflow
•	pyaudio
•	python 3.8


Steps to run the system:
1)	Download the files from GitHub.
Here is the file Structure
 - main.py
 - bodypose_analyze.py
 - handpose_analyze.py
 - robotserver.py
 - tp_final.py
 - graphdb.py
 - chatbot.py
 - video.mp4
   speech
	- textpredict.py
	- train.py
	- chatbot_model.h5
	- classes.pkl
	- words.pkl
	- intents.json

2)	Install anaconda and neo4j desktop in your PC.
3)	Create a new conda environment with python 3.8
4)	Activate your conda environment and install the below packages
mediapipe
pyttsx3
nltk
speechrecognition
neo4j
opencv-python
tensorflow
pyaudio
python 3.8

5)	Make sure the neo4j database is active and running on your pc
6)	Communication to the robot is through TCP Socket, so it’s easier to implement the code for any robot. 
      
7)	Run the main.py program from your anaconda environment. Next run the robot so it will start communicating to the python program
8)	You can give voice commands to the system, 
Example : “Create new database”, “update database from video”
		“pickredcoins”, “pickblackbox”

9)	If you want to update the database from the video there will be a prompt to select the region of interest at the beginning of the video. After selecting the item hit enter key.
Data will be captured only when the selected item is moved in the video.
  

10)	Data captured will be updated to the knowledge base. For reference purpose the same data will be saved to robot.csv file.

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

- Executive Summary
- Market Research
- Business Justification
- Project Objectives 
     - System Design
     - Overview to create knowledge base from video
- System Validation
     -   Knowledge graph from experts
     -   New Knowledge graph after video analysis
- Resulting Output - Demo pictures
- Project Conclusion
- Appendix of report: Project Proposal
- Appendix of report: Mapped System Functionalities against knowledge, techniques and skills of modular courses: MR, RS, CGS
- Appendix of report: Installation and User Guide
- Appendix of report: Reflection on project journey

