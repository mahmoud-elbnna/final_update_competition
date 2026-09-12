import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import sys, select, termios, tty

class manualnode(Node):
    def __init__(self):
        super().__init__('manualnode')
        self.cmd_pub = self.create_publisher(Twist, '/manual_cmd_vel', 10)
        self.phase_pub = self.create_publisher(Float32, '/phase_detection', 10)
        self.manual_active = False
        
        self.is_tty = sys.stdin.isatty()
        if self.is_tty:
            self.settings = termios.tcgetattr(sys.stdin)
            self.get_logger().info('Manual Node Initialized in Interactive Mode.')
            self.get_logger().info('Press [SPACEBAR] to toggle Manual/Auto mode.')
            self.get_logger().info('Use [W/A/S/D] to drive when in Manual mode.')
            self.get_logger().info('Press [Q] to quit.')
        else:
            self.get_logger().warn('stdin is not a TTY terminal. Keyboard input disabled for this instance.')

        self.timer = self.create_timer(0.1, self.keyboard_loop)

    def get_key(self):
        if not self.is_tty:
            return ''
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if rlist else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def keyboard_loop(self):
        if not self.is_tty:
            return
            
        key = self.get_key()
        if key == '':
            return

        if key == ' ':
            self.manual_active = not self.manual_active
            msg = Float32()
            msg.data = 1.0 if self.manual_active else 0.0
            self.phase_pub.publish(msg)

        elif self.manual_active and key in ['w', 'a', 's', 'd']:
            twist = Twist()
            if key == 'w': twist.linear.x = 0.2
            elif key == 's': twist.linear.x = -0.2
            elif key == 'a': twist.angular.z = 0.5
            elif key == 'd': twist.angular.z = -0.5
            self.cmd_pub.publish(twist)

        elif key == 'q':
            stop_msg = Twist()
            self.cmd_pub.publish(stop_msg)
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = manualnode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()