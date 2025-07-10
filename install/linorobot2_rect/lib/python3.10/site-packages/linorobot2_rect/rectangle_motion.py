import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time
import RPi.GPIO as GPIO

GPIO_PIN = 16
GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD

ODOM_SCALE = 1.176

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

        GPIO.setup(GPIO_PIN, GPIO.OUT)
        self.get_logger().info("Waiting for odometry data...")

    def odom_callback(self, msg):
        """Update robot's position from odometry."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.odom_received = True

    # def move_exact_distance(self, x=0.0, dist=0.0):
    #     """Moves the robot precisely `dist` meters forward in x direction while maintaining y."""
    #     while not self.odom_received:
    #         rclpy.spin_once(self)  # Wait for odometry

    #     # Store the starting position
    #     start_x, start_y = self.x, self.y
    #     target_distance = dist / ODOM_SCALE
    #     print("start pos", start_x, start_y)

    #     self.twist.linear.x = x
    #     self.twist.linear.y = 0.0  # Move only in x direction

    #     while rclpy.ok():
    #         rclpy.spin_once(self)  # Process odometry updates

    #         # Optional: Apply small correction to keep y aligned
    #         y_error = start_y - self.y
    #         k_y = 1.0  # Proportional gain for correction (tune this)
    #         self.twist.linear.y = k_y * y_error  # Try to correct lateral drift

    #         self.publisher_.publish(self.twist)

    #         # Calculate distance traveled in x-y plane
    #         dx = self.x - start_x
    #         dy = self.y - start_y
    #         print("y error",dy)
    #         distance_moved = math.sqrt(dx**2 + dy**2)

    #         if distance_moved >= target_distance:
    #             break

    #     print("publishing stop")
    #     # Stop the robot
    #     self.twist.linear.x = 0.0
    #     self.twist.linear.y = 0.0
    #     self.publisher_.publish(self.twist)
    #     print("end pos", self.x, self.y)
    #     time.sleep(0.5)  # Small delay to stabilize

    def move_exact_distance(self, x=0.0, y=0.0,dist=0.0):
        """Moves the robot precisely 0.1m in the given direction using odometry feedback."""
        while not self.odom_received:
            rclpy.spin_once(self)  # Wait for odometry

        # Store the starting position
        start_x, start_y = self.x, self.y
        target_distance = dist/ODOM_SCALE # Move exactly 0.1m
        print("start pos",start_x,start_y)
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
        print("end pos", self.x,self.y)
        time.sleep(0.5)  # Small delay to stabilize

    def draw_square(self,x_len=0.5,y_len=0.5):
        """Executes the rectangle movement using odometry feedback."""
        while not self.odom_received:
            rclpy.spin_once(self)  # Wait for odometry

        if rclpy.ok():
            print("moving 1 ")
            self.spray(True)
            self.move_exact_distance(x=0.1,dist=x_len)   # Move forward
            self.spray(False)
            time.sleep(2)
            print("moving 2")
            self.spray(True)
            self.move_exact_distance(y=0.1,dist=y_len)  # Strafe right
            self.spray(False)
            time.sleep(2)
            print("moving 3")
            self.spray(True)
            self.move_exact_distance(x=-0.1,dist=x_len)  # Move backward
            self.spray(False)
            time.sleep(2)
            print("moving 4")
            self.spray(True)
            self.move_exact_distance(y=-0.1,dist=y_len)   # Strafe left
            self.spray(False)
            time.sleep(2)
            # self.move_exact_distance(y=0.10,dist=1.0)   # Move forward
            # print("moving 2")
            # self.move_exact_distance(x=0.10,dist=1.0)  # Strafe right
            # print("moving 3")
            # self.move_exact_distance(y=-0.10,dist=1.0)  # Move backward
            # print("moving 4")
            # self.move_exact_distance(x=-0.10,dist=1.0)   # Strafe left

    def draw_SFU(self):
        while not self.odom_received:
            rclpy.spin_once(self)  # Wait for odometry

        if rclpy.ok():
            self.spray(True)
            self.move_exact_distance(y=-0.1,dist=0.5) # L
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=0.1,dist=0.5) # D
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(y=0.1,dist=0.5)  # R
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=0.1,dist=0.5) # D
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(y=-0.1,dist=0.5) # L
            self.spray(False)
            time.sleep(2)
            # self.spray(True)
            self.move_exact_distance(y=0.1,dist=0.5*2) # Rx2
            # self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=-0.1,dist=0.5) # U
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(y=0.1,dist=0.5) # R
            self.spray(False)
            time.sleep(2)
            # self.spray(True)
            self.move_exact_distance(y=-0.1,dist=0.5) # L
            # self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=-0.1,dist=0.5) # U
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(y=0.1,dist=0.5) # Rx2
            self.spray(False)
            self.move_exact_distance(y=0.1,dist=0.5) # Rx2
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=0.1,dist=0.5*2) # Dx2
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(y=0.1,dist=0.5) # R
            self.spray(False)
            time.sleep(2)
            self.spray(True)
            self.move_exact_distance(x=-0.1,dist=0.5*2) # Ux2
            self.spray(False)
            time.sleep(2)

    def draw_triangle(self):
        """Executes the triangle movement using odometry feedback."""
        while not self.odom_received:
            rclpy.spin_once(self)  # Wait for odometry

        if rclpy.ok():
            self.move_exact_distance(x=0.10,y=0.1,dist=1)   # Move forward
            self.move_exact_distance(x=-0.10,y=0.1,dist=1)   # Move forward
            self.move_exact_distance(x=0.0,y=-0.1,dist=1)   # Move forward

    def spray(self,on: bool):
        if on:
            GPIO.output(GPIO_PIN, GPIO.HIGH)
        else:
            GPIO.output(GPIO_PIN, GPIO.LOW)
def main():
    print("running arp movement main")
    rclpy.init()
    node = RectangleMotion()
    try:
        print("gonna do it")
        node.draw_square(1.0,1.0)
        # node.move_exact_distance(x=0.15,dist=5.0)
        # node.draw_SFU()
        print("i did it")
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(GPIO_PIN, GPIO.LOW)
        GPIO.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
