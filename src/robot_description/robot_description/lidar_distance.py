import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarDistance(Node):
    def __init__(self):
        super().__init__("display_scan_node")


        # Subscriber to get Lidar readings
        self.subscriber_lidar_ = self.create_subscription(
                LaserScan,
                '/laser/scan',
                self.laserscan_callback,
                10)
        


    def laserscan_callback(self, msg):
        min_distance = min(msg.ranges)
        self.get_logger().info(f"Range Min: {min_distance:.2f}")





def main(args=None):
    rclpy.init(args=args)
    node = LidarDistance()
    node.send_goal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()