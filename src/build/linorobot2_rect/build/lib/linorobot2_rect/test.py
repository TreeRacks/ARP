#! /usr/bin/env python3
from rclpy.node import Node
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.executors import ExternalShutdownException

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator

class AgentPathPlanner(Node):

    def __init__(self):
        super().__init__('agent_path_planner')
        self.declare_parameter('x_init', 3.0)
        self.declare_parameter('y_init', 2.5)
        self.declare_parameter('x_goal', 3.0)
        self.declare_parameter('y_goal', 7.0)
        self.setup_navigation()


    def setup_navigation(self):
        self.navigator = BasicNavigator()
        initial_pose = PoseStamped()
        goal_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        initial_pose.pose.position.x = self.get_parameter(
            'x_init').get_parameter_value().double_value
        initial_pose.pose.position.y = self.get_parameter(
            'y_init').get_parameter_value().double_value
        initial_pose.pose.orientation.z = 0.707
        initial_pose.pose.orientation.w = 0.707

        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = self.get_parameter(
            'x_goal').get_parameter_value().double_value
        goal_pose.pose.position.y = self.get_parameter(
            'y_goal').get_parameter_value().double_value
        goal_pose.pose.orientation.z = 0.707
        goal_pose.pose.orientation.w = 0.707

        #self.navigator.setInitialPose(initial_pose)
        self.navigator.waitUntilNav2Active()
        self.get_agent_path(initial_pose, goal_pose)

    def get_agent_path(self, initial_pose, goal_pose):
        path = self.navigator.getPath(initial_pose, goal_pose)
        self.info(path)
        return path


    def info(self, msg):
        self.get_logger().info(msg)
        return


def main(args=None):
    """ send the target pose to each robot in the fleet
    The fleet can be scaled up and down by changing the agents to generate 
    more edges 

    """
    rclpy.init(args=args)
    agent_path_planner = AgentPathPlanner()

    executor = SingleThreadedExecutor()
    executor.add_node(agent_path_planner)

    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
