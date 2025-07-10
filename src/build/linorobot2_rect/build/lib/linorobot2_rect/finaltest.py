import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowPath
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class FollowPathClient(Node):
    def __init__(self):
        super().__init__('follow_path_client')
        self._action_client = ActionClient(self, FollowPath, 'follow_path')

        self.declare_parameter('path_coordinates',
            [0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            2.0, 1.0]
        )
        
        self.path_coords = self.get_parameter('path_coordinates').get_parameter_value().double_array_value
        self.send_goal()

    def generate_path(self):
        path = Path()
        path.header.frame_id = 'map'

        for coord in zip(*[iter(self.path_coords)] * 2):
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = coord[0]
            pose.pose.position.y = coord[1]
            pose.pose.orientation.w = 1.0  # Facing forward
            path.poses.append(pose)

        return path

    def send_goal(self):
        self._action_client.wait_for_server()

        goal_msg = FollowPath.Goal()
        goal_msg.path = self.generate_path()
        goal_msg.controller_id = ''  # Use default
        goal_msg.goal_checker_id = ''  # Use default

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected 😢')
            return

        self.get_logger().info('Goal accepted 👍')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        # self.get_logger().info(f'Following path, error: {feedback.current_error:.2f}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Path completed with result: {result}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = FollowPathClient()
    rclpy.spin(client)

if __name__ == '__main__':
    main()
