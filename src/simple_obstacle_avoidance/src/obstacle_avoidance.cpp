#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

#include <algorithm>

using std::placeholders::_1;
using namespace std::chrono_literals;

class ObstacleAvoidance : public rclcpp::Node
{
public:
    ObstacleAvoidance()
    : Node("simple_obstacle_avoidance_node")
    {
        // Publisher to topic /cmd_vel to move the robot
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);

        // Subscription to topic /laser/scan to get Lidar readings
        subscriber_ = this->create_subscription<sensor_msgs::msg::LaserScan>("/laser/scan", 10, std::bind(&ObstacleAvoidance::laserscan_callback, this, _1));

    }
private:
    void laserscan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        int size = msg->ranges.size();
        int width = 200;
        // Front side of the robot
        int start_front = size/2 - width;
        int end_front = size/2 + width;

        auto min_it_front = std::min_element(msg->ranges.begin() + start_front, msg->ranges.begin() + end_front);
        //int minIndex_front = std::distance(msg->ranges.begin(), min_it_front);
        float min_distance_front = *min_it_front;

        // Right side of the robot
        int start_right = 0;
        int end_right = size/2 - (width + 1);

        auto min_it_right = std::min_element(msg->ranges.begin() + start_right, msg->ranges.begin() + end_right);
        //int minIndex_right = std::distance(msg->ranges.begin(), min_it_right);
        float min_distance_right = *min_it_right;

        // Left side of the robot
        int start_left = size/2 + (width + 1);
        int end_left = size - 1;

        auto min_it_left = std::min_element(msg->ranges.begin() + start_left, msg->ranges.begin() + end_left);
        //int minIndex_left = std::distance(msg->ranges.begin(), min_it_left);
        float min_distance_left = *min_it_left;

        // Command that the robot will execute
        auto action = geometry_msgs::msg::Twist();
        action.linear.x = 0.0;
        action.angular.z = 0.0;

        bool obstacle_front = (min_distance_front < distance_threshold);
        bool obstacle_right = (min_distance_right < distance_threshold);
        bool obstacle_left = (min_distance_left < distance_threshold);
        bool obstacle_right_left = obstacle_right && obstacle_left;

        
        if (obstacle_front) {
            action.linear.x = 0.0;
            action.angular.z = 0.5;
            
            if (!obstacle_right_left) {
                if (obstacle_right && !obstacle_left){
                    action.linear.x = 0.0;
                    action.angular.z = 0.5; // Obstacle to the right ==> Turn left
                    RCLCPP_INFO(this->get_logger(),"Obstacle to the right, turning left");
                } else if (obstacle_left && !obstacle_right) {
                    action.linear.x = 0.0;
                    action.angular.z = -0.5; // Obstacle to the left ==> Turn right
                    RCLCPP_INFO(this->get_logger(),"Obstacle to the left, turning right");
                }
            } else {
                action.linear.x = -1.0;
                action.angular.z = 0.0;
                RCLCPP_INFO(this->get_logger(),"Robot surrounded, turn left");
            } 
        } else {
            action.linear.x = 1.0;
            action.angular.z = 0.0; // No obstacle in front ==> Move forward
            RCLCPP_INFO(this->get_logger(),"No obstacle ahead, moving forward!");
        }
    

        publisher_->publish(action);
    }
    float distance_threshold = 1.0;
    float min_distance;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscriber_;
};


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ObstacleAvoidance>());
    rclcpp::shutdown();
    return 0;
}