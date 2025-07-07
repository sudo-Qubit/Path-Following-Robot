#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"


class MoveRobot : public rclcpp::Node
{
public:
    MoveRobot() : Node("move_robot_node")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
        go_in_circle();
    }
private:
    void go_in_circle()
    {
        auto message = geometry_msgs::msg::Twist();
        message.linear.x = 1;
        message.angular.z = 1;
        publisher_->publish(message);
    }
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
};


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MoveRobot>());
    rclcpp::shutdown();
    return 0;
}

