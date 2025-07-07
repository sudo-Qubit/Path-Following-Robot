cmake_minimum_required(VERSION 3.8)
project(topic_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(move_robot_node src/move_robot.cpp)
ament_target_dependencies(move_robot_node rclcpp geometry_msgs)

add_executable(sub_odom_node src/sub_odom.cpp)
ament_target_dependencies(sub_odom_node rclcpp nav_msgs)

install(TARGETS
  move_robot_node
  sub_odom_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)



ament_package()
