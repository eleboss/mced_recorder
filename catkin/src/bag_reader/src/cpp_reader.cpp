
#include <rosbag/bag.h>
#include <rosbag/view.h>
#include <dvs_msgs/EventArray.h>
#include <sensor_msgs/Image.h>

using namespace std;


int main(int argc, char **argv)
{
    rosbag::Bag bag;
    bag.open("test.bag");  // BagMode is Read by default
    cout<<"open"<<endl;
    for(rosbag::MessageInstance const m: rosbag::View(bag))
    {
      // cout<<"hellp"<<endl;
          // cout<<m.getTopic()<<endl;
        // dvs_msgs::EventArray::ConstPtr i = m.instantiate<dvs_msgs::EventArray>();
        // if (i != NULL)
        // std::cout << i << std::endl;
    }
    cout<<"over"<<endl;
    bag.close();







    // rosbag::Bag bag;
    // bag.open("test.bag", rosbag::bagmode::Read);

    // std::vector<std::string> topics;
    // topics.push_back(std::string("/cam/image_raw"));
    // topics.push_back(std::string("/celex/events"));


    // rosbag::View view(bag, rosbag::TopicQuery(topics));

    // for(rosbag::MessageInstance const m: view){
    // // foreach(rosbag::MessageInstance const m, view)
    // // {
    //     // std_msgs::String::ConstPtr s = m.instantiate<std_msgs::String>();
    //     cout<<m.getTopic()<<endl;
    //     // sensor_msgs::Image::ConstPtr image = m.instantiate<sensor_msgs::Image>();
    //     // dvs_msgs::EventArray::ConstPtr j = m.instantiate<dvs_msgs::EventArray>();
    //     // cout<<j<<endl;
    //     // if (s != NULL)
    //     //     ASSERT_EQ(s->data, std::string("foo"));


    //     // if (i != NULL)
    //     //     ASSERT_EQ(i->data, 42);
    // }

    // bag.close();







    return 0;
}