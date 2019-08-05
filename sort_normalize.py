# -*- coding: utf-8 -*-
import glob
import cv2
import numpy as np
import os
import sys
import txt_loader
 
dataset_path = '/home/ubuntu/dvs_dataset/road/'


START_AT_ZERO = 0

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

def main(): 
    for subdir, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith("events.txt"):
                print "##############################################"
                print "loading... ",os.path.join(subdir, file)
                events = txt_loader.event_txt_loader(os.path.join(subdir, file))
                last_ev = 0.0
                sorted_event = sorted(events, key=lambda x: x[0])
                for i in sorted_event:
                    if i[0] - last_ev < 0:
                        print "find reverse, sorting fail!"
                    if i[0] - last_ev > 0.1:
                        print "find space too large!",i[0] - last_ev,i[0]
                    last_ev = i[0]
                if START_AT_ZERO:
                    init_timestamp = sorted_event[0][0]
                else:
                    init_timestamp = 0

                with open(os.path.join(subdir, file), "w") as text_file:
                    for ev in sorted_event:
                        ev_t = ev[0] - init_timestamp
                        ev_x = ev[1]
                        ev_y = ev[2]
                        ev_p = ev[3]
                        text_file.write('%f' % (ev_t) + " " + str(ev_x) + " " + str(ev_y) + " " + str(ev_p) + "\n") 


if __name__ == "__main__":
    main()


