    #include <rosbag/bag.h>
    #include <rosbag/view.h>
    #include <dvs_msgs/EventArray.h>

    rosbag::Bag bag;
    bag.open("test.bag");  // BagMode is Read by default

    for(rosbag::MessageInstance const m: rosbag::View(bag))
    {
      std_msgs::Int32::ConstPtr i = m.instantiate<std_msgs::Int32>();
      if (i != NULL)
        std::cout << i->data << std::endl;
    }

    bag.close();