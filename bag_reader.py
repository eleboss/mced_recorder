import subprocess, shlex, rospy, rosbag
import numpy as np

ev_width = 1280 #x
ev_height = 800 #y


filename = "luosidao"
exp_image = np.zeros((ev_height,ev_width))
bag = rosbag.Bag(filename+".bag")
for topic, msg, t in bag.read_messages(topics=['/celex/events']):
    print topic,t
    # print msg.events[0].polarity
    for i in msg.events:
        sum_image[799-i.y ,i.x] = i.ts.secs + i.ts.nsecs * 10e-6
        
# cv2.waitKey(1000)

for topic, msg, t in bag.read_messages(topics=['/cam/image_raw']):
    print topic,t
bag.close()
