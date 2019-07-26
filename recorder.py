import subprocess, shlex, rospy


# recording duration in second
DURATION = "10" 
DURATION = raw_input("Tell me the duration(s):")
# recording name of file
file_name = "apple"
# recording topic 1
topic_1 = "/cam/image_raw"
# recording topic 2
topic_2 = "/celex/events"

topic_3 = "/infrared/image_raw"

topic_4 = "/celex/image_raw"

while(1):

    file_name = raw_input("File name:")
    print "record start!"
    command = "rosbag record -O " + file_name + " " "--duration=" + DURATION + " " + topic_1 + " " + topic_2 + " " + topic_3 + " " + topic_4
    command = shlex.split(command)
    rosbag_proc = subprocess.Popen(command)
