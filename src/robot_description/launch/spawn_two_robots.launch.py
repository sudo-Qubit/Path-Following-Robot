#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def generate_robot_group(robot_name, x, y, z):
    robot_desc_path = PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'urdf',
        'robot.xacro'
    ])

    # use of bash -c with full command as a single string
    robot_description_cmd = Command([
        TextSubstitution(text='bash -c "xacro --root robot '),
        robot_desc_path,
        TextSubstitution(text=' robot_name:='),
        robot_name,
        TextSubstitution(text=" | sed -n '/<robot/,/<\\/robot>/p'\"")
    ])

    return GroupAction([
        PushRosNamespace(robot_name),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'robot_description': robot_description_cmd
            }]
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_entity',
            output='screen',
            arguments=[
                '-name', robot_name,
                '-allow_renaming', 'true',
                '-topic', ['/', robot_name, '/robot_description'],
                '-x', str(x),
                '-y', str(y),
                '-z', str(z),
            ]
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name=[robot_name, TextSubstitution(text='_bridge')],
            output='screen',
            arguments=[
                ['/', robot_name, '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
                ['/', robot_name, '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
                ['/', robot_name, '/laser/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
                ['/', robot_name, '/imu@sensor_msgs/msg/Imu@gz.msgs.IMU'],
                ['/', robot_name, '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'],
                ['/', robot_name, '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image'],
                ['/', robot_name, '/camera/depth/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked'],
                ['/', robot_name, '/camera/depth@sensor_msgs/msg/Image@gz.msgs.Image'],
            ]
        ),
    ])


def generate_launch_description():
    robot1_name = LaunchConfiguration('robot1_name')
    # robot2_name = LaunchConfiguration('robot2_name')

    return LaunchDescription([
        DeclareLaunchArgument('robot1_name', default_value='robot1'),
        # DeclareLaunchArgument('robot2_name', default_value='robot2'),


        generate_robot_group(robot1_name, 0.0, 0.0, 0.5),
        # generate_robot_group(robot2_name, 0.0, -2.0, 0.5),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='clock_bridge',
            output='screen',
            arguments=['/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock']
        ),
    ])