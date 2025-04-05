import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time

class RectangleMotion(Node):
    def __init__(self):
        super().__init__('rectangle_motion_odom')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) 
        self.odom_subscriber = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Store current position
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # Orientation (not used here)
        self.odom_received = False
        self.twist = Twist()

        self.get_logger().info("Waiting for odometry data...")

    def odom_callback(self, msg):
        """Update robot's position from odometry."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.odom_received = True

    def move_exact_distance(self, x=0.0, y=0.0,dist=0.0):
        """Moves the robot precisely 0.1m in the given direction using odometry feedback."""
        if not self.odom_received:
            self.get_logger().error("No odometry received. Cannot move.")
            return

        # Store the starting position
        start_x, start_y = self.x, self.y
        target_distance = dist # Move exactly 0.1m

        self.twist.linear.x = x
        self.twist.linear.y = y
        
        while rclpy.ok():
            rclpy.spin_once(self)  # Process odometry updates

            self.publisher_.publish(self.twist)

            # Calculate distance traveled
            dx = self.x - start_x
            dy = self.y - start_y
            distance_moved = math.sqrt(dx**2 + dy**2)

            if distance_moved >= target_distance:
                break
        print("publishing stop")
        # Stop the robot
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.publisher_.publish(self.twist)
        time.sleep(0.5)  # Small delay to stabilize

    def draw_square(self):
        """Executes the rectangle movement using odometry feedback."""
        while not self.odom_received:
            rclpy.spin_once(self)  # Wait for odometry

        if rclpy.ok():
            print("moving 1 ")
            self.move_exact_distance(x=0.1,dist=0.5)   # Move forward
            print("moving 2")
            self.move_exact_distance(y=0.1,dist=0.5)  # Strafe right
            print("moving 3")
            self.move_exact_distance(x=-0.1,dist=0.5)  # Move backward
            print("moving 4")
            self.move_exact_distance(y=-0.1,dist=0.5)   # Strafe left

def main():
    rclpy.init()
    node = RectangleMotion()
    try:
        print("gonna do it")
        node.draw_square()
        print("i did it")
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
