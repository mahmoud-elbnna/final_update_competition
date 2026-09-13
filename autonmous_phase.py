import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from std_msgs.msg import Float32

class autonmousnode(Node):

    def __init__(self):
        super().__init__('autonmouspublisher')
        self.publisher_ = self.create_publisher(Twist, '/auto_cmd_vel', 10)
        self.screw_subscription = self.create_subscription(Point, '/vision/scroll_target', self.detectscroll_callback, 10)
        self.wall_subscribtion = self.create_subscription(Float32, '/ultrasonic_distance', self.detectwall_callback, 10)
        
        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.detectionscroll_received = False
        self.scroll_x_offset = 0.0
        self.current_wall_distance = 100.0

        self.judge_pause_active = False
        self.pause_start_time = None
        self.pause_duration = 5.0 
        self.target_processed = False
        self.detection_count = 0

    def detectscroll_callback(self, msg):
        if msg.z == 1.0:
            self.detectionscroll_received = True
        else:
            self.detectionscroll_received = False
            self.target_processed = False
            
        self.scroll_x_offset = msg.x

    def detectwall_callback(self, msg):
        self.current_wall_distance = msg.data

    def timer_callback(self):
        twist_msg = Twist()

        if self.judge_pause_active:
            elapsed = (self.get_clock().now() - self.pause_start_time).nanoseconds / 1e9
            
            if elapsed < self.pause_duration:
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                self.publisher_.publish(twist_msg)
                return
            else:
                self.judge_pause_active = False
                self.target_processed = True

        if self.detectionscroll_received and not self.target_processed:
            if self.current_wall_distance <= 12.0:
                self.judge_pause_active = True
                self.pause_start_time = self.get_clock().now()
                self.detection_count += 1
                
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
            else:
                twist_msg.linear.x = 0.2
                twist_msg.angular.z = -0.5 * self.scroll_x_offset

        elif self.current_wall_distance < 20.0:
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.6

        else:
            twist_msg.linear.x = 0.15
            twist_msg.angular.z = 0.3

        self.publisher_.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    autonmous_node = autonmousnode()
    try:
        rclpy.spin(autonmous_node)
    except KeyboardInterrupt:
        pass
    finally:
        autonmous_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
