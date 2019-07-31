import subprocess, shlex, rospy, rosbag
import numpy as np
import os
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def mkdir(path):
    import os
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print path+'Crate path'
        return True
    else:
        print path+'invaild path'
        return False

ev_width = 1280 #x
ev_height = 800 #y

dataset_path = './'

entries = os.listdir(dataset_path)
for files in entries:
    if files.endswith(".bag"):
        file_name = os.path.splitext(files)[0]
        bag = rosbag.Bag(dataset_path+files)
        mkdir(dataset_path + file_name)
        # transfer rosbag to txt
        with open(dataset_path + file_name + "/" + "events" + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/celex/events']):
                print topic,t.secs,".",t.nsecs
                # print msg.events[0].polarity
                for i in msg.events:
                    ev_x = i.x
                    ev_y = i.y
                    ev_p = int(i.polarity)
                    ev_t = float(str(i.ts.secs)[-5:]+ '.' + str(i.ts.nsecs)) 
                    text_file.write('%f' % (ev_t) + " " + str(ev_x) + " " + str(ev_y) + " " + str(ev_p) + "\n") 

        # process images
        mkdir(dataset_path + file_name + "/rgb")
        frame_counter = 0
        with open(dataset_path + file_name + "/" + "rgb_time" + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/cam/image_raw']):
                print topic,t   
                
                cv_image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
                cv2.imwrite(dataset_path + file_name + "/rgb/" + "%09d" % frame_counter + ".png", cv_image)

                img_time = float(str(msg.header.stamp.secs)[-5:]+ '.' + str(msg.header.stamp.nsecs)) 
                text_file.write("%09d" % frame_counter + " " + str(img_time) + "\n")
                frame_counter = frame_counter + 1 

        mkdir(dataset_path + file_name + "/infrared")
        frame_counter = 0
        with open(dataset_path + file_name + "/" + "infrared_time" + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/infrared/image_raw']):
                print topic,t   
                
                cv_image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
                cv2.imwrite(dataset_path + file_name + "/infrared/" + "%09d" % frame_counter + ".png", cv_image)

                img_time = float(str(msg.header.stamp.secs)[-5:]+ '.' + str(msg.header.stamp.nsecs)) 
                text_file.write("%09d" % frame_counter + " " + str(img_time) + "\n")
                frame_counter = frame_counter + 1 

        mkdir(dataset_path + file_name + "/ev_frame")
        frame_counter = 0
        with open(dataset_path + file_name + "/" + "ev_frame_time" + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/celex/image_raw']):
                print topic,t   
                
                cv_image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
                cv2.imwrite(dataset_path + file_name + "/ev_frame/" + "%09d" % frame_counter + ".png", cv_image)

                img_time = float(str(msg.header.stamp.secs)[-5:]+ '.' + str(msg.header.stamp.nsecs)) 
                text_file.write("%09d" % frame_counter + " " + str(img_time) + "\n")
                frame_counter = frame_counter + 1 
        

        bag.close()
