import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

# ROS2 Launch System will look for this function definition #
def generate_launch_description():
    
    # Get package description and directory #
    package_description = "robot_description"
    package_directory = get_package_share_directory(package_description)

    # Load URDF File #
    urdf_file = "robot.urdf"
    robot_desc_path = os.path.join(package_directory, "urdf", urdf_file)
    print("URDF Loaded !")

    # Robot State Publisher (RSP) #
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher_node",
        output="screen",
        emulate_tty=True,
        parameters=[{'use_sim_time': True,
                     'robot_description': open(robot_desc_path).read()
                     }],
    )

    # Load Rviz Configuration file
    rviz_config_file = "config.rviz"
    rviz_config_path = os.path.join(package_directory, "rviz", rviz_config_file)

    # RViz2 Launch Configuration (RViz) #
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_node",
        output="screen",
        emulate_tty=True,
        parameters=[{"use_sim_time": True}],
        arguments=['-d', rviz_config_path],
    )


    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",  # Or "joint_state_publisher" if GUI is not needed
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )

    # # So that the robot can move in RViz2
    # motion_sim_node = Node(
    #     package="robot_description",
    #     executable="robot_motion_sim",
    #     name="robot_motion_sim",
    #     output="screen",
    #     emulate_tty=True,
    # )

    # test_laser_publisher_node = Node(
    #     package="robot_description",
    #     executable="test_laser_publisher",
    #     name="test_laser_publisher",
    #     output="screen",
    #     emulate_tty=True,
    # )

    # Create an Return the Launch Description Object #
    return LaunchDescription(
        [
            robot_state_publisher_node,
            rviz_node,
            joint_state_publisher_node,
            # motion_sim_node,
            # test_laser_publisher_node,
        ]
    )