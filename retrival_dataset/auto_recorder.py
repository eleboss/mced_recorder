import subprocess, shlex, rospy
import time


cfg_path = "/home/eleboss/dvs_dataset/ukbench/cfg/"
counter = 0
DURATION = 2

while(1):
    start_time = time.time()
    print "record start!"
    command = "roslaunch esim_ros esim.launch config:=" + cfg_path + "ukbench" +"%05d" % counter + ".conf"
    command = shlex.split(command)
    rosbag_proc = subprocess.Popen(command)

    elapsed_time = time.time() - start_time
    while(elapsed_time < int(DURATION) + 20):
        elapsed_time = time.time() - start_time
    counter = counter + 4
    if counter == 10200:
        break

