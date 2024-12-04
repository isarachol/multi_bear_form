from math import sin, cos, pi
# import threading
import rclpy
from rclpy.node import Node
# from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion, Twist, Point
# from sensor_msgs.msg import JointState
# from tf2_ros import TransformBroadcaster, TransformStamped

# can try to modify this https://github.com/ros-teleop/teleop_twist_keyboard/blob/master/teleop_twist_keyboard.py
# Basically use Twist msg type to command velocity

class SingleStatePublisher(Node):

    def __init__(self):
        super().__init__('single_state_publisher')
        self.publisher_ = self.create_publisher(Twist, 'diff_cont/cmd_vel_unstamped', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0
        self.subscription = self.create_subscription(
            Point,
            'detected_ball',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, point):
        self.get_logger().info('x is: "%f"' % point.x)
        twist = Twist()
        twist.linear.x = 0.
        twist.linear.y = 0.
        twist.linear.z = 0.
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.
        if point.z < 0.2:
            if abs(point.x) > 0.1:
                twist.angular.x = 0.0
                twist.angular.y = 0.0
                twist.angular.z = -point.x
            elif point.y < 0.9:
                twist.linear.x = 0.5
                twist.linear.y = 0.
                twist.linear.z = 0.
        else:
            self.get_logger().info('Found ball!')
        self.publisher_.publish(twist)


    # def timer_callback(self):
    #     if self.i % 5 == 0:
    #         twist = Twist()
    #         twist.linear.x = 3.
    #         twist.linear.y = 0.
    #         twist.linear.z = 0.
    #         twist.angular.x = 0.0
    #         twist.angular.y = 0.0
    #         twist.angular.z = 2.
    #         self.publisher_.publish(twist)
    #     self.i += 1
    #     self.get_logger().info('Publishing: message number "%d"' % self.i)

# class MinimalSubscriber(Node):

#     def __init__(self):
#         super().__init__('minimal_subscriber')
#         self.subscription = self.create_subscription(
#             Point,
#             'detected_ball',
#             self.listener_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#     def listener_callback(self, point):
#         self.get_logger().info('x is: "%f"' % point.x)


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_subscriber = MinimalSubscriber()

#     rclpy.spin(minimal_subscriber)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_subscriber.destroy_node()
#     rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = SingleStatePublisher()
    # while rclpy.ok():
    #     node.get_logger().info('In while loop')
    #     rclpy.spin_once(node)
    # node.get_logger().info('out of while loop')
    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
