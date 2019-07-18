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

dataset_path = '/home/eleboss/dvs_dataset/mced/'

entries = os.listdir('/home/eleboss/dvs_dataset/mced/')
for files in entries:
    if files.endswith(".bag"):
        file_name = os.path.splitext(files)[0]
        bag = rosbag.Bag(dataset_path+files)
        mkdir(dataset_path + file_name)
        mkdir(dataset_path + file_name + "/image")
        # transfer rosbag to txt
        with open(dataset_path + file_name + "/" + "events" + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/celex/events']):
                print topic,t
                # print msg.events[0].polarity
                
                for i in msg.events:
                    ev_x = i.x
                    ev_y = i.y
                    ev_p = int(i.polarity == 'True')
                    ev_t = i.ts.secs + i.ts.nsecs * 1e-9    
                    text_file.write('%f' % (ev_t) + " " + str(ev_x) + " " + str(ev_y) + " " + str(ev_p) + "\n") 

        
        for topic, msg, t in bag.read_messages(topics=['/cam/image_raw']):
            print topic,t
            img_time = msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9     
            cv_image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
            cv2.imwrite(dataset_path + file_name + "/image/" + str(img_time) + ".png", cv_image)
        bag.close()
