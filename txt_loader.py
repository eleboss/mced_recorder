def event_txt_loader(file_path = '', load_number = 0):
    import numpy as np
    import os
    print("starting opening files...")
    with open(file_path, 'r') as ev_f:
        event_lines = ev_f.readlines()
    print("Opening finished...")
    print("starting appending events...")
    events = []
    for index, ev_line in enumerate(event_lines):
        ev_polarity = 0
        ev_line = ev_line.split(' ')
        ev_time = float(ev_line[0])
        ev_x = int(ev_line[1])
        ev_y = int(ev_line[2])
        if int(ev_line[3][0]) == 0:
            ev_polarity = 0
        else:
            ev_polarity = 1     
        events.append([ev_time, ev_x, ev_y, ev_polarity])
        # if index % 10000 == 0:
        #     print index
        if load_number != 0:
            if index > load_number:
                print("reached setting number")
                print("Have a good day!",np.shape(events))
                return events
    print("finished")
    # print("Have a good day!",np.shape(events))

    return events
    
