# -*- coding: utf-8 -*-
import glob
import cv2
import numpy as np
import os
import sys
from shutil import copyfile
import shutil
 
dataset_path = './'
cfg_path = "/home/eleboss/dvs_dataset/ukbench/cfg/"
output_path = "/media/eleboss/C14D581BDA18EBFA/ret_events/"

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

    for i in range(10200):
        shutil.copy("./template.conf",cfg_path+ "ukbench" + "%05d" % i + ".conf")

    for i in range(10200):

        with open(cfg_path + "ukbench" + "%05d" % i + ".conf", 'r') as conf:
            lines = conf.readlines()

        with open(cfg_path + "ukbench" + "%05d" % i + ".conf", "w") as text_file:
            for index, line in enumerate(lines):
                text_file.write(line) 
            ztext_file.write("--path_to_output_bag=" + output_path + "ukbench" + "%05d" % i + ".bag" + "\n") 
            text_file.write("--renderer_texture=/home/eleboss/dvs_dataset/ukbench/ukbench" + "%05d" % i + ".jpg" + "\n") 

if __name__ == "__main__":
    main()


