from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="topic_pkg",
            executable="sub_odom_node",
            output="screen"),
    ])