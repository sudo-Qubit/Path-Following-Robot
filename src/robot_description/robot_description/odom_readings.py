import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class DisplayOdometry(Node):

    def __init__(self):
        super().__init__("display_odom_node")

        self.odom_sub = self.create_subscription(Odometry,
                                                "/odom",
                                                self.odom_callback,
                                                10)
        

    def odom_callback(self, odom_msg):
        position = odom_msg.pose.pose.position
        pos_x = position.x
        pos_y = position.y
        self.get_logger().info(f"PosX: {pos_x:.2f}, PosY: {pos_y:.2f}")


def main(args=None):
    
    rclpy.init(args=args)
    node = DisplayOdometry()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

    return None

if __name__ == "__main__":
    main()
