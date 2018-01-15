
add_library(koala_driver
  koala_video.cpp
  koala_wheels.cpp
  koala_camera_position.cpp
  )
target_link_libraries(koala_driver ${catkin_LIBRARIES} jpeg ktprot)