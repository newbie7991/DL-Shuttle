import cv2
import numpy as np
import mediapipe as mp
import math
import os
import glob

videoPath = ('./Upload Video/')

class poseDetector():
    # MediaPipe Pose Function Initiator
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)
 
    # Function to recognize the person in the image
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw: 
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
 
    # Find the node of the pose landmarks and store it (h, w, c)
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    
    def findAngle(self, img, p1, p2, p3, draw=True):
 
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
 
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
  
        # Put the text of the angle of shoulder and arm
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 3, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 3, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 3, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

# --------------Clear Pose Estimation Checking--------------------#
def poseEstimationClear():
    #Remove a picture of last training
    files = glob.glob('./static/Image/Clear/*.jpg')
    for f in files:
        os.remove(f)
    files = glob.glob('./static/Image/CorrectPose/*.jpg')
    for f in files:
        os.remove(f)
    counter = 0
    rightShoulderTemp = 0
    leftShoulderTemp = 0
    correctPose = 0
    incorrectPose = 0  
    stage = None
    check = 0 
    currentframe = 0
    MaxAngleRightShoulder = 0
    MaxAngleLeftShoulder = 0
    detector = poseDetector()
    # Read the video file from the path
    for file in os.listdir(videoPath):
        if file.endswith(".mp4"):
            path=os.path.join(videoPath, file)
            cap = cv2.VideoCapture(path)
            
            # Check if video read successfully
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
            # Read until video is completed
            while (cap.isOpened()):
                # Capture frame-by-frame for processing
                ret, frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    frame = detector.findPose(frame, True)
                    lmList = detector.findPosition(frame, True)
                    if len(lmList) != 0:
                        # Angle counting
                        # Right Arm
                        angleRightArm = detector.findAngle(frame, 12, 14, 16)
                        # Left Arm
                        angleLeftArm = detector.findAngle(frame, 11, 13, 15)
                        # Right Shoulder 
                        angleRightShoulder = detector.findAngle(frame, 24, 12, 14)
                        # Left Shoulder
                        angleLeftShoulder = detector.findAngle(frame, 13, 11, 23)

                    #Clear 
                    #-------------------------------------------#    
                        # Get Incorrect Right Sholder Picture
                        if counter == rightShoulderTemp:
                            if angleRightShoulder > MaxAngleRightShoulder and angleRightShoulder < 280:
                                MaxAngleRightShoulder = angleRightShoulder                                              
                                if MaxAngleRightShoulder < 110:
                                    tempRightFrame = frame                          
                                                        
                        else:
                            if MaxAngleRightShoulder < 110 and MaxAngleRightShoulder >30:
                                print(MaxAngleRightShoulder) 
                                name = './static/Image/Clear/WrongPose' + str(currentframe) + '.jpg'
                                cv2.imwrite(name, tempRightFrame)
                                currentframe += 1
                            rightShoulderTemp += 1
                            MaxAngleRightShoulder = 0
                        # Incorrect right Shoulder End

                        #-------------------------------------------#    
                        # Get Incorrect Left Sholder Picture
                        if counter == leftShoulderTemp:
                            if angleLeftShoulder > MaxAngleLeftShoulder and angleLeftShoulder < 300:
                                MaxAngleLeftShoulder = angleLeftShoulder                                              
                                if MaxAngleLeftShoulder < 120:
                                    tempLeftFrame = frame  
                        
                                                        
                        else:
                            if MaxAngleLeftShoulder < 120 and MaxAngleLeftShoulder >30:
                                print(MaxAngleLeftShoulder) 
                                name = './static/Image/Clear/WrongPose' + str(currentframe) + '.jpg'
                                cv2.imwrite(name, tempLeftFrame)
                                currentframe += 1
                            leftShoulderTemp += 1
                            MaxAngleLeftShoulder = 0
                        # Incorrect Left Shoulder end

                    # Action Counting
                    if angleRightArm > 220 and angleRightShoulder>80:
                        stage = "down"
                        # Check Correct Posture
                        if angleRightArm > 220 and angleRightShoulder>110 and angleLeftArm>60 and angleLeftShoulder>50 and MaxAngleLeftShoulder>120:
                            check +=1

                    if angleRightArm < 180 and stage =='down' and angleRightShoulder < 30 and angleLeftShoulder<35:
                        stage="up"
                        counter +=1
                        print("Count = %s" %counter)    
                        if check != 0:
                            correctPose += 1
                            print("Correct Pose = %s" %correctPose)
                            check = check - check
                    # End of Action Counting
  
                            # ---------Store a sample Correct Poseture----------
                    if check == 0 and correctPose == 0:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectClear" + '.jpg', frame)
                    if check == 0 and correctPose == 2:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectClear1" + '.jpg', frame)
                    if check == 0 and correctPose == 1:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectClear2" + '.jpg', frame)
                    if check == 0 and correctPose == 3:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectClear3" + '.jpg', frame)
                            # --------------------------------------------------

                    # Display the resulting frame
                    cv2.imshow('Frame', frame)
                    
                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            
                # Break the loop
                else:
                    break
            
            # When everything done, release the video capture object
            cap.release()
            
            # Closes all the frames
            cv2.destroyAllWindows()
            incorrectPose = counter - correctPose
            print("Correct Pose = %s" % correctPose)
            print("Incorrect Pose = %s" % incorrectPose)
    return correctPose,incorrectPose,counter
# --------------------End Of Clear------------------------------#

# ------------- Smash Pose Estimation Checking------------------#
def poseEstimationSmash():
    #Remove a picture of last training
    files = glob.glob('./static/Image/Smash/*.jpg')
    for f in files:
        os.remove(f)
    files = glob.glob('./static/Image/CorrectPose/*.jpg')
    for s in files:
        os.remove(s)
    counter = 0
    x = 0
    rightShoulderTemp = 0
    leftShoulderTemp = 0
    tempRightFrame = 0
    tempLeftFrame = 0
    correctPose = 0
    incorrectPose = 0  
    stage = None
    check = 0 
    currentframe = 0


    MaxAngleRightShoulder = 0
    MaxAngleLeftShoulder = 0
    SmashSwingTemp = 0
    MaxSmashRightShoulder = 0
    MinSmashRightShoulder = 100
    tempSmashMinFrame = 0
    tempSmashMaxFrame = 0
    detector = poseDetector()
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    for file in os.listdir(videoPath):
        if file.endswith(".mp4"):
            path=os.path.join(videoPath, file)
            cap = cv2.VideoCapture(path)
            
            # Check if camera opened successfully
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
            # Read until video is completed
            while (cap.isOpened()):
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    frame = detector.findPose(frame, True)
                    lmList = detector.findPosition(frame, True)
                    if len(lmList) != 0:
                        # Angle counting
                        # Right Arm
                        angleRightArm = detector.findAngle(frame, 12, 14, 16)
                        # Left Arm
                        angleLeftArm = detector.findAngle(frame, 11, 13, 15)
                        # Right Shoulder 
                        angleRightShoulder = detector.findAngle(frame, 24, 12, 14)
                        # Left Shoulder
                        angleLeftShoulder = detector.findAngle(frame, 13, 11, 23)

                    #-------------------------------------------#    
                    # Smash
                    # Get After Swing of Smash Angle 
                    if counter == SmashSwingTemp:  
                        if angleRightShoulder < MinSmashRightShoulder and angleRightShoulder > 1:
                            MinSmashRightShoulder = angleRightShoulder
                            tempSmashMinFrame = frame
                        if angleRightShoulder > 320 and angleRightShoulder < 350:
                            x = 1
                        if angleRightShoulder > MaxSmashRightShoulder:
                            MaxSmashRightShoulder = angleRightShoulder
                            tempSmashMaxFrame = frame      
                                                       
                    else:
                        # store smash error posture angle > 350 
                        if x == 1:
                            pass
                        # store the min angle reach of when after swing angle are not in correct range
                        else:
                            if MaxSmashRightShoulder > 350:
                                print(MaxSmashRightShoulder) 
                                name = './static/Image/Smash/WrongPose' + str(currentframe) + '.jpg'
                                cv2.imwrite(name, tempSmashMaxFrame)
                                currentframe += 1
                            else:
                                print(MinSmashRightShoulder) 
                                name = './static/Image/Smash/WrongPose' + str(currentframe) + '.jpg'
                                cv2.imwrite(name, tempSmashMinFrame)
                                currentframe += 1
                        SmashSwingTemp += 1
                        x = 0
                        print(SmashSwingTemp) 
                        MinSmashRightShoulder = 100
                        MaxSmashRightShoulder = 0
                    # Incorrect Smash Swing End


                    #-------------------------------------------#    
                    # Get Incorrect Right Sholder Picture
                    if counter == rightShoulderTemp:
                        if angleRightShoulder > MaxAngleRightShoulder and angleRightShoulder < 280:
                            MaxAngleRightShoulder = angleRightShoulder                                                                           
                            if MaxAngleRightShoulder < 110:
                                tempRightFrame = frame  
                                                   
                    else:
                        if MaxAngleRightShoulder < 110 and MaxAngleRightShoulder >30:
                            print(MaxAngleRightShoulder) 
                            name = './static/Image/Smash/WrongPose' + str(currentframe) + '.jpg'
                            cv2.imwrite(name, tempRightFrame)
                            currentframe += 1
                        rightShoulderTemp += 1
                        MaxAngleRightShoulder = 0
                    # Incorrect right Shoulder End

                    #-------------------------------------------#    
                    # Get Incorrect Left Sholder Picture
                    if counter == leftShoulderTemp:
                        if angleLeftShoulder > MaxAngleLeftShoulder and angleLeftShoulder < 300:
                            MaxAngleLeftShoulder = angleLeftShoulder                                              
                            if MaxAngleLeftShoulder < 120:
                                tempLeftFrame = frame  
                    
                                                    
                    else:
                        if MaxAngleLeftShoulder < 120 and MaxAngleLeftShoulder >30:
                            print(MaxAngleLeftShoulder) 
                            name = './static/Image/Smash/WrongPose' + str(currentframe) + '.jpg'
                            cv2.imwrite(name, tempLeftFrame)
                            currentframe += 1
                        leftShoulderTemp += 1
                        MaxAngleLeftShoulder = 0
                    # Incorrect Left Shoulder end

                    #------------------------------------------------------------------------------#    
                    # Action Counting
                    if angleRightArm > 220 and angleRightShoulder>80:
                        stage = "down"
                        # Check Correct Posture
                        if angleRightArm > 220 and angleRightShoulder>110 and angleLeftArm>60 and angleLeftShoulder>50 and MaxAngleLeftShoulder>120:
                            check +=1

                        # ---------Store a sample Correct Poseture-------------
                    if check == 0 and correctPose == 2:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectSmash" + '.jpg', frame)
                    if check == 0 and correctPose == 0:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectSmash1" + '.jpg', frame)
                    if check == 0 and correctPose == 1:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectSmash2" + '.jpg', frame)
                    if check == 0 and correctPose == 3:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectSmash3" + '.jpg', frame)
                        # -----------------------------------------------------

                    if angleRightArm < 180 and angleRightArm > 120 and stage =='down' and angleRightShoulder > 20 and angleRightShoulder < 40 and angleLeftShoulder<40:
                        stage="up"
                        counter +=1
                        print("Count = %s" %counter)    
                        if check != 0:
                            correctPose += 1
                            print("Correct Pose = %s" %correctPose)
                            check = check - check
                    # End of Action Counting
                    #---------------------------------------------------------------------------------------#    
  
                    # Display the resulting frame
                    cv2.imshow('Frame', frame)
                    
                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            
                # Break the loop
                else:
                    break
            
            # When everything done, release the video capture object
            cap.release()
            
            # Closes all the frames
            cv2.destroyAllWindows()
            incorrectPose = counter - correctPose
            print("Correct Pose = %s" % correctPose)
            print("Incorrect Pose = %s" % incorrectPose)
    return correctPose,incorrectPose,counter        
# -----------------Smash Checking End------------------------------#

# Serve Pose Estimation checking
def poseEstimationServe():
    #Remove a picture of last training
    files = glob.glob('./static/Image/Serve/*.jpg')
    for f in files:
        os.remove(f)
    files = glob.glob('./static/Image/CorrectPose/*.jpg')
    for f in files:
        os.remove(f)
    counter = 0
    correctPose = 0
    incorrectPose = 0  
    stage = None
    check = 0 
    currentframe = 0   
    detector = poseDetector()
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    for file in os.listdir(videoPath):
        if file.endswith(".mp4"):
            path=os.path.join(videoPath, file)
            cap = cv2.VideoCapture(path)
            
            # Check if camera opened successfully
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
            # Read until video is completed
            while (cap.isOpened()):
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    frame = detector.findPose(frame, True)
                    lmList = detector.findPosition(frame, True)
                    if len(lmList) != 0:
                        # Angle counting
                        # Right Arm
                        angleRightArm = detector.findAngle(frame, 12, 14, 16)
                        # Left Arm
                        angleLeftArm = detector.findAngle(frame, 11, 13, 15)
                        # Right Shoulder 
                        angleRightShoulder = detector.findAngle(frame, 24, 12, 14)
                        # Left Shoulder
                        angleLeftShoulder = detector.findAngle(frame, 13, 11, 23)


                    # Serve 
                    # -------------------Action Counting--------------------------------
                    if angleRightArm > 120 and angleRightArm < 180 and angleRightShoulder> 35 and angleRightShoulder < 90 and angleLeftShoulder < 60 :
                        stage = "down"
                        # Check Correct Posture
                        if angleRightArm > 150 and angleRightArm < 170 and angleRightShoulder> 35 and angleRightShoulder < 60 and angleLeftShoulder < 40 :
                            check +=1
                        elif angleRightArm > 170 and angleRightArm < 180 and angleRightShoulder> 85 and angleRightShoulder < 90 and angleLeftShoulder < 40 :
                            name = './static/Image/Serve/WrongPose' + str(currentframe) + '.jpg'
                            cv2.imwrite(name, frame)
                            currentframe += 1
                    elif angleRightArm > 120 and angleRightArm < 180 and angleRightShoulder> 35 and angleRightShoulder < 90 and angleLeftShoulder > 340 :
                        stage = "down"
                        # Check Correct Posture
                        if angleRightArm > 150 and angleRightArm < 170 and angleRightShoulder> 35 and angleRightShoulder < 60 and angleLeftShoulder > 340 :
                            check +=1
                        elif angleRightArm > 170 and angleRightArm < 180 and angleRightShoulder> 85 and angleRightShoulder < 90 and angleLeftShoulder > 340 :
                            name = './static/Image/Serve/WrongPose' + str(currentframe) + '.jpg'
                            cv2.imwrite(name, frame)
                            currentframe += 1

                            # ---------Store a sample Correct Poseture----------
                    if check == 0 and correctPose == 2:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectServe" + '.jpg', frame)
                    if check == 0 and correctPose == 0:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectServe1" + '.jpg', frame)
                    if check == 0 and correctPose == 1:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectServe2" + '.jpg', frame)
                    if check == 0 and correctPose == 3:
                        cv2.imwrite("./static/Image/CorrectPose/CorrectServe3" + '.jpg', frame)
                            # --------------------------------------------------

                    if angleRightArm < 180 and stage =='down' and angleRightShoulder < 20 and angleLeftShoulder<35:
                        stage="up"
                        counter +=1
                        print("Count = %s" %counter)    
                        if check != 0:
                            correctPose += 1
                            print("Correct Pose = %s" %correctPose)
                            check = check - check
                    # ---------------End of Action Counting----------------------
                    
                    # Display the resulting frame
                    cv2.imshow('Frame', frame)
                    
                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
            
                # Break the loop
                else:
                    break
            
            # When everything done, release the video capture object
            cap.release()
            
            # Closes all the frames
            cv2.destroyAllWindows()
            incorrectPose = counter - correctPose
            print("Correct Pose = %s" % correctPose)
            print("Incorrect Pose = %s" % incorrectPose)
    return correctPose,incorrectPose,counter        
# -----------------End of Serve Checking----------------------------#