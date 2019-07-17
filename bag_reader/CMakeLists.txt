cmake_minimum_required (VERSION 2.6)
project (reader)


find_package(rosbag REQUIRED)
set(SOURCES cpp_reader.cpp)
target_link_libraries(reader)
add_executable(reader ${SOURCES})
