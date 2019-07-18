# -*- coding: utf-8 -*-
"""
This module contains classes, functions and an example (main) for handling AER vision data.
"""
import glob
import cv2
import numpy as np
import os
import sys
# from win32api import GetSystemMetrics
import timer

# np.set_printoptions(threshold=sys.maxsize)

class_list = [
"accordion"           ,"cougar_body"      ,"gerenuk"       ,"metronome"   ,"soccer_ball"
,"airplanes"          ,"cougar_face"      ,"gramophone"    ,"minaret"     ,"stapler"
,"anchor"             ,"crab"             ,"grand_piano"   ,"Motorbikes"  ,"starfish"
,"ant"                ,"crayfish"         ,"hawksbill"     ,"nautilus"    ,"stegosaurus"
,"BACKGROUND_Google"  ,"crocodile"        ,"headphone"     ,"octopus"     ,"stop_sign"
,"barrel"             ,"crocodile_head"   ,"hedgehog"      ,"okapi"       ,"strawberry"
,"bass"               ,"cup"              ,"helicopter"    ,"pagoda"      ,"sunflower"
,"beaver"             ,"dalmatian"        ,"ibis"          ,"panda"       ,"tick"
,"binocular"          ,"dollar_bill"      ,"inline_skate"  ,"pigeon"      ,"trilobite"
,"bonsai"             ,"dolphin"          ,"joshua_tree"   ,"pizza"       ,"umbrella"
,"brain"              ,"dragonfly"        ,"kangaroo"      ,"platypus"    ,"watch"
,"brontosaurus"       ,"electric_guitar"  ,"ketch"         ,"pyramid"     ,"water_lilly"
,"buddha"             ,"elephant"         ,"lamp"          ,"revolver"    ,"wheelchair"
,"butterfly"          ,"emu"              ,"laptop"        ,"rhino"       ,"wild_cat"
,"camera"             ,"euphonium"        ,"Leopards"      ,"rooster"     ,"windsor_chair"
,"cannon"             ,"ewer"             ,"llama"         ,"saxophone"   ,"wrench"
,"car_side"           ,"Faces_easy"       ,"lobster"       ,"schooner"    ,"yin_yang"
,"ceiling_fan"        ,"ferry"            ,"lotus"         ,"scissors"
,"cellphone"          ,"flamingo"         ,"mandolin"      ,"scorpion"
,"chair"              ,"flamingo_head"    ,"mayfly"        ,"sea_horse"
,"chandelier"         ,"garfield"         ,"menorah"       ,"snoopy"]

# class_list = ["BACKGROUND_Google"]
         

def mkdir(path):
    # 引入模块
    import os
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print path+'Crate path'
        return True
    else:
        print path+'invaild path'
        return False

class Events(object):
    """
    Temporal Difference events.
    data: a NumPy Record Array with the following named fields
        x: pixel x coordinate, unsigned 16bit int
        y: pixel y coordinate, unsigned 16bit int
        p: polarity value, boolean. False=off, True=on
        ts: timestamp in microseconds, unsigned 64bit int
    width: The width of the frame. Default = 304.
    height: The height of the frame. Default = 240.
    """
    def __init__(self, num_events, width=304, height=240):
        """num_spikes: number of events this instance will initially contain"""
        self.data = np.rec.array(None, dtype=[('x', np.uint16), ('y', np.uint16), ('p', np.bool_), ('ts', np.uint64)], shape=(num_events))
        self.width = width
        self.height = height



    def show_td(self, wait_delay=100, saver = 0, prefix = "", select_imgNo = 0):
        """Displays the TD events (change detection ATIS or DVS events)
        waitDelay: milliseconds
        """
        frame_length = 24e3
        t_max = self.data.ts[-1]
        frame_start = self.data[0].ts
        frame_end = self.data[0].ts + frame_length
        td_img = np.ones((self.height, self.width), dtype=np.uint8)
        frame_counter = 0
        while frame_start < t_max:
            frame_data = self.data[(self.data.ts >= frame_start) & (self.data.ts < frame_end)]
            
            if frame_data.size > 0:
                td_img.fill(128)

                #with timer.Timer() as em_playback_timer:
                for datum in np.nditer(frame_data):
                    td_img[datum['y'].item(0), datum['x'].item(0)] = datum['p'].item(0)
                #print 'prepare td frame by iterating events took %s seconds'
                #%em_playback_timer.secs
                td_img = np.piecewise(td_img, [td_img == 0, td_img == 1, td_img == 128], [0, 255, 128])
                if saver: 
                    if frame_counter == select_imgNo:
                        s_frame_counter = "%04d" % frame_counter
                        # cv2.imwrite(prefix + "img"+str(frame_counter)+".png", td_img)
                        cv2.imwrite(prefix + ".png", td_img)
                else:
                    cv2.imshow('img', td_img)
                    cv2.waitKey(wait_delay)
                frame_counter = frame_counter + 1


            frame_start = frame_end + 1
            frame_end = frame_end + frame_length + 1

        cv2.destroyAllWindows()
        return

    def time_surface(self, wait_delay=100, saver = 0, prefix = "", process_number = 10000, method = "sort"):
        """Displays time surface
        waitDelay: milliseconds
        """
        frame_length = 24e3
        t_max = self.data.ts[-1]
        frame_start = self.data[0].ts
        frame_end = self.data[0].ts + frame_length
        td_img = np.ones((self.height, self.width), dtype=np.uint8)
        frame_counter = 0
        print "Frame start",np.shape(self.data)
        time_sur = np.zeros((self.height, self.width))
        exp_sur = np.zeros((self.height, self.width))

        if np.shape(self.data)[0] < process_number:
            process_number = np.shape(self.data)[0]-1
        for i in range(process_number+1):
            time_sur[self.data[i].y, self.data[i].x] = self.data[i].ts

        if method == "exp":
        # construct error map
            exp_sur =  (self.data[process_number].ts * np.ones((self.height, self.width)) - time_sur) /10000.0
            exp_sur = np.exp(-exp_sur)
            cv2.imwrite(prefix + ".png", exp_sur*256)

        if method == "sort":
            same_window_thresh = 5 #for jitter latency suppression
            new_sea = time_sur
            new_sea = np.reshape(new_sea,(self.height * self.width))
            weight_sea = np.zeros((self.height * self.width))
            sort_list = np.argsort(new_sea)
            rank = 1
            last_sea_time = 0
            for sor in range(np.shape(sort_list)[0]):
                #use the thresh to filter the data
                if abs(new_sea[sort_list[sor]] - last_sea_time) < same_window_thresh:
                    new_sea[sort_list[sor]] = last_sea_time
                    weight_sea[sort_list[sor]] = rank
                else:
                    rank = rank + 1
                    weight_sea[sort_list[sor]] = rank
                    last_sea_time = new_sea[sort_list[sor]]
            weight_sea = np.reshape(weight_sea, (self.height , self.width)) / rank
            cv2.imwrite(prefix + ".png", weight_sea*256)
            # print weight_sea

        return

    def sort_order(self):
        """Generate data sorted by ascending ts
        Does not modify instance data
        Will look through the struct events, and sort all events by the field 'ts'.
        In other words, it will ensure events_out.ts is monotonically increasing,
        which is useful when combining events from multiple recordings.
        """
        #chose mergesort because it is a stable sort, at the expense of more
        #memory usage
        events_out = np.sort(self.data, order='ts', kind='mergesort')
        return events_out

    def save_as_txt(self,file_name):
        with open(file_name, "w") as text_file:
            events_out = np.sort(self.data, order='ts', kind='mergesort')
            for datum in np.nditer(events_out):
                ev_t = float(datum['ts'].item(0)/1e6)
                ev_x = int(datum['x'].item(0))
                ev_y = int(datum['y'].item(0))
                ev_p = int(datum['p'].item(0))
                text_file.write('%f' % (ev_t) + " " + str(ev_x) + " " + str(ev_y) + " " + str(ev_p) + "\n") 
        return


def read_dataset(filename):
    """Reads in the TD events contained in the N-MNIST/N-CALTECH101 dataset file specified by 'filename'"""
    f = open(filename, 'rb')
    raw_data = np.fromfile(f, dtype=np.uint8)
    f.close()
    raw_data = np.uint32(raw_data)

    all_y = raw_data[1::5]
    all_x = raw_data[0::5]
    all_p = (raw_data[2::5] & 128) >> 7 #bit 7
    all_ts = ((raw_data[2::5] & 127) << 16) | (raw_data[3::5] << 8) | (raw_data[4::5])

    #Process time stamp overflow events
    time_increment = 2 ** 13
    overflow_indices = np.where(all_y == 240)[0]
    for overflow_index in overflow_indices:
        all_ts[overflow_index:] += time_increment

    #Everything else is a proper td spike
    td_indices = np.where(all_y != 240)[0]

    td = Events(td_indices.size, 34, 34)
    td.data.x = all_x[td_indices]
    td.width = td.data.x.max() + 1
    td.data.y = all_y[td_indices]
    td.height = td.data.y.max() + 1
    td.data.ts = all_ts[td_indices]
    td.data.p = all_p[td_indices]
    return td


def file_counter(path):
    # return sum([len(x) for _, _, x in os.walk(os.path.dirname("./test/"))])
    return sum([len(x) for _, _, x in os.walk(os.path.dirname(path))])

def main():
    """Example usage of eventvision"""

    #read in some data
    n_caltech_path = "./N-Caltech101/"
    # save_path = "./DVS-Caltech101_denoise/"
    save_path = "./N-Caltech101_txt/"
    mkdir(save_path)
    file_name = "image_"
    for class_name in class_list:
        mkdir(save_path + class_name)
        for j in range(file_counter(n_caltech_path + class_name+"/")):
            file_name = "image_"+ ("%04d" %(j+1))
            td = read_dataset(n_caltech_path + class_name + "/" + file_name+".bin")
            td.save_as_txt(save_path+class_name+"/"+file_name+".txt")

            print np.shape(td.sort_order().ts)
            print class_name,file_name

    
    # with open("Output.txt", "w") as text_file:
    #     text_file.write("123\n123")

if __name__ == "__main__":
    main()

print 'Event-based vision module imported'
