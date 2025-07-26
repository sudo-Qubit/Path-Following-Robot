#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
import math

class RobotMotionSim(Node):
    def __init__(self):
        super().__init__('robot_motion_sim')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.cmd_vel_sub = self.create_subscription(Twist, 'my_robot/cmd_vel', self.cmd_vel_callback, 10)
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20 Hz to match Gazebo
        self.vx = 0.0
        self.vth = 0.0
        self.x, self.y, self.theta = 0.0, 0.0, 0.0
        self.wheel_positions = [0.0, 0.0]  # Left, Right
        self.get_logger().info('Robot motion simulator started')

    def cmd_vel_callback(self, msg):
        self.vx = msg.linear.x
        self.vth = msg.angular.z

    def timer_callback(self):
        dt = 0.05
        self.x += self.vx * math.cos(self.theta) * dt
        self.y += self.vx * math.sin(self.theta) * dt
        self.theta += self.vth * dt

        # Publish TF
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'link_chassis'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(self.theta / 2.0)
        t.transform.rotation.w = math.cos(self.theta / 2.0)
        self.tf_broadcaster.sendTransform(t)

        # Publish wheel joint states
        wheel_radius = 0.4  # From URDF
        wheel_separation = 1.66  # From URDF
        linear_vel = self.vx / wheel_radius
        angular_vel = self.vth * wheel_separation / (2.0 * wheel_radius)
        self.wheel_positions[0] += (linear_vel - angular_vel) * dt  # Left wheel
        self.wheel_positions[1] += (linear_vel + angular_vel) * dt  # Right wheel

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = ['joint_chassis_left_wheel', 'joint_chassis_right_wheel']
        js.position = self.wheel_positions
        self.joint_state_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = RobotMotionSim()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()