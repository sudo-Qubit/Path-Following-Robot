#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class TestLaserPublisher(Node):
    def __init__(self):
        super().__init__('test_laser_publisher')
        self.publisher_ = self.create_publisher(LaserScan, 'my_robot/laser/scan', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20 Hz
        self.get_logger().info('Test laser publisher started')

    def timer_callback(self):
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'link_laser_scan'
        scan.angle_min = -1.570796  # From URDF
        scan.angle_max = 1.570796
        scan.angle_increment = (scan.angle_max - scan.angle_min) / 720
        scan.range_min = 0.20
        scan.range_max = 10.0
        scan.ranges = [5.0] * 720  # Dummy ranges
        self.publisher_.publish(scan)

def main(args=None):
    rclpy.init(args=args)
    node = TestLaserPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()