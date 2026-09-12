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

    def detectscroll_callback(self, msg):
        if msg.z == 1.0:
            self.detectionscroll_received = True
        else:
            self.detectionscroll_received = False
        self.scroll_x_offset = msg.x

    def detectwall_callback(self, msg):
        self.current_wall_distance = msg.data

    def execute_detectwall_callback(self):
        if self.current_wall_distance < 20.0:
            twist_msg = Twist()
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.6
            return twist_msg
        return None
            
    def execute_detectscroll_callback(self):
        if self.detectionscroll_received:
            twist_msg = Twist()
            if self.current_wall_distance <= 12.0:
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
            else:
                twist_msg.linear.x = 0.2
                twist_msg.angular.z = -0.5 * self.scroll_x_offset
            return twist_msg
        return None

    def timer_callback(self):
        wall_action = self.execute_detectwall_callback()
        scroll_action = self.execute_detectscroll_callback()

        if wall_action != None:
            twist_msg = wall_action
        elif scroll_action != None:
            twist_msg = scroll_action
        else:
            twist_msg = Twist()
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.3

        self.publisher_.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    autonmous_node = autonmousnode()
    rclpy.spin(autonmous_node)
    autonmous_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()