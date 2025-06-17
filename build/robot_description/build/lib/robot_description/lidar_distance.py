import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class LidarDistance(Node):
    def __init__(self):
        super().__init__("display_scan_node")

        # Publisher to move the robot around
        # Didn't add a callback function since seng_goal() function
        # will publish to topic once, and topic will keep executing
        # that command until it get another
        self.publisher_ = self.create_publisher(
                Twist,
                '/cmd_vel',
                10)
        
        # Subscriber to get Lidar readings
        self.subscriber_lidar_ = self.create_subscription(
                LaserScan,
                '/laser/scan',
                self.laserscan_callback,
                10)
        

        self.linear_goal = 0.5
        self.angular_goal = 0.5

        self.send_goal()


    def laserscan_callback(self, msg):
        min_distance = min(msg.ranges)
        self.get_logger().info(f"Range Min: {min_distance:.2f}")


    
    def send_goal(self):
        action = Twist()
        action.linear.x = self.linear_goal
        action.angular.z = self.angular_goal
        self.publisher_.publish(action)


def main(args=None):
    rclpy.init(args=args)
    node = LidarDistance()
    node.send_goal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()