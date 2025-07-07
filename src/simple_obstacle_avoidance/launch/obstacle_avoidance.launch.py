from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_obstacle_avoidance',
            executable='obstacle_avoidance_node',
            name='obstacle_avoidance',
            output='screen'
        )
    ])