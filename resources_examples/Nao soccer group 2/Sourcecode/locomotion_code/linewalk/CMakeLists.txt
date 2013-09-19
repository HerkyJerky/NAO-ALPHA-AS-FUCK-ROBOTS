cmake_minimum_required(VERSION 2.8)
project(linewalk)

include_directories(/home/tim/install/naoqi-sdk-1.14-linux32/include)
link_directories(/home/tim/install/naoqi-sdk-1.14-linux32/lib)

find_package(qibuild)

qi_create_lib(linewalk SHARED linewalk.hpp linewalk.cpp main.cpp)
qi_use_lib(linewalk ALCOMMON BOOST)
