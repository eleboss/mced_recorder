import subprocess, shlex, rospy, rosbag
import numpy as np
import os


ev_width = 1280 #x
ev_height = 800 #y

entries = os.listdir('./')
for files in entries:
    if files.endswith(".bag"):
        file_name = os.path.splitext(files)[0]
        bag = rosbag.Bag(files)
        with open(file_name + ".txt", "w") as text_file:
            for topic, msg, t in bag.read_messages(topics=['/celex/events']):
                print topic,t
                # print msg.events[0].polarity
                
                for i in msg.events:
                    ev_x = i.x
                    ev_y = i.y
                    ev_p = int(i.polarity == 'True')
                    ev_t = i.ts.secs + i.ts.nsecs * 1e-6    
                    text_file.write('%f' % (ev_t) + " " + str(ev_x) + " " + str(ev_y) + " " + str(ev_p) + "\n") 

        for topic, msg, t in bag.read_messages(topics=['/cam/image_raw']):
            print topic,t
        bag.close()
