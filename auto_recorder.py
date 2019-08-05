import subprocess, shlex, rospy
import time

# recording duration in second
DURATION = "10" 
DURATION = raw_input("Tell me the duration(s):")
# recording name of file
file_name = raw_input("File name:")

dataset_path = "/home/ubuntu/dvs_dataset/road/"
# recording topic 1
topic_1 = "/cam/image_raw"
# recording topic 2
topic_2 = "/celex/events"

topic_3 = "/infrared/image_raw"

# topic_4 = "/celex/image_raw"
topic_4 = ""
counter = 0
while(1):
    start_time = time.time()
    print "record start!"
    command = "rosbag record -O " + dataset_path + file_name+ "_"+ str(counter) + " " "--duration=" + DURATION + " " + topic_1 + " " + topic_2 + " " + topic_3 + " " + topic_4
    command = shlex.split(command)
    rosbag_proc = subprocess.Popen(command)

    elapsed_time = time.time() - start_time
    while(elapsed_time < int(DURATION) + 3):
        elapsed_time = time.time() - start_time
    counter = counter + 1