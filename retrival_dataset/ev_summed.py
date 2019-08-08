# -*- coding: utf-8 -*-
import glob
import cv2
import numpy as np
import os
import sys
import txt_loader
 
dataset_path = '/media/eleboss/C14D581BDA18EBFA/ret_events/'


START_AT_ZERO = 0

event_height = 480
event_width = 640
compressed_time = 0.01

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

    for subdir, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith("events.txt"):
                image_array = np.zeros((event_height,event_width))
                file_name = os.path.splitext(subdir)[0][-12:]
                print file_name
                mkdir(dataset_path + file_name + "/dvs")
                print "##############################################"
                print "loading... ",os.path.join(subdir, file)
                events = txt_loader.event_txt_loader(os.path.join(subdir, file))
                first_ev_time = events[0][0]
                counter = 0

                for ev in events:
                    ev_t = ev[0]
                    ev_x = ev[1]
                    ev_y = ev[2]
                    ev_p = ev[3]
                    image_array[ev_y,ev_x] = ev_t*255
                    update_ev_frame_time = ev_t
                    if update_ev_frame_time - first_ev_time > compressed_time:
                        cv2.imwrite(dataset_path + file_name + "/dvs/"+ "%04d" % counter +".png", image_array)
                        first_ev_time = ev_t
                        image_array = np.zeros((event_height,event_width))
                        counter = counter + 1
                    
                    


if __name__ == "__main__":
    main()


