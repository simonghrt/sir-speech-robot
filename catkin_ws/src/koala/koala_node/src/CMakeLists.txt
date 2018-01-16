
link_directories(${KTPROT_LINK_DIRECTORIES})
include_directories(include
  ${catkin_INCLUDE_DIRS}
  ${KTPROT_INCLUDE_DIRS}
)


add_executable(camera_node camera_node.cpp)
target_link_libraries(camera_node 
  ${catkin_LIBRARIES}  ktprot
  )

add_executable(camera_position_node camera_position_node.cpp)
target_link_libraries(camera_position_node 
  ${catkin_LIBRARIES}  ktprot
  )

add_executable(wheels_node wheels_node.cpp)
target_link_libraries(wheels_node 
  ${catkin_LIBRARIES}  ktprot
  )

add_executable(odom_node odom_node.cpp)
target_link_libraries(odom_node 
  ${catkin_LIBRARIES}  ktprot
  )
