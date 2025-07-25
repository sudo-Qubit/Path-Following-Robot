cmake_minimum_required(VERSION 3.8)
project(simple_obstacle_avoidance)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(obstacle_avoidance_node src/obstacle_avoidance.cpp)
ament_target_dependencies(obstacle_avoidance_node rclcpp geometry_msgs sensor_msgs)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS
  obstacle_avoidance_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
