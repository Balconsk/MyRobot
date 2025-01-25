# from pointcloud2_wrapper import PointCloud2Wrapper_NumPy
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
import numpy as np
from array import array
from copy import deepcopy
import struct
from kinect_simulate.pointcloud2_wrapper import PointCloud2Wrapper_NumPy


class PointCloudClipping(Node):

    def __init__(self):
        super().__init__("minimal_subscriber")
        self.subscription = self.create_subscription(
            PointCloud2,
            "points",
            self.clipping_and_publish,
            QoSProfile(reliability=QoSReliabilityPolicy.BEST_EFFORT, depth=5),
        )

    def clipping_and_publish(self, msg: PointCloud2):
        pcw = PointCloud2Wrapper_NumPy(msg)
        self.get_logger().info("I heard msg with points: %s" % len(pcw))


def main(args=None):
    rclpy.init(args=args)
    point_cloud_clipping = PointCloudClipping()

    rclpy.spin(point_cloud_clipping)


if __name__ == "__main__":
    # main()
    print(int("1"))
