import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class selectornode(Node):
    def __init__(self):
        super().__init__('selectornode')
        self.cmd_publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.auto_subscription = self.create_subscription(Twist, '/auto_cmd_vel', self.auto_callback, 10)
        self.manual_subscribtion = self.create_subscription(Twist, '/manual_cmd_vel', self.manual_callback, 10)
        self.detect_phase_subscription = self.create_subscription(Float32, '/phase_detection', self.detect_phase_callback, 10)
        self.manual_phase = False

    def detect_phase_callback(self, msg):
        self.manual_phase = bool(msg.data)
        if self.manual_phase:
            self.get_logger().info("Manual Phase Activated")
        else:
            self.get_logger().info("Auto Phase Activated")

    def auto_callback(self, msg):
        if not self.manual_phase:
            self.cmd_publisher_.publish(msg)

    def manual_callback(self, msg):
        if self.manual_phase:
            self.cmd_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    selector_node = selectornode()
    try:
        rclpy.spin(selector_node)
    except KeyboardInterrupt:
        pass
    finally:
        selector_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()