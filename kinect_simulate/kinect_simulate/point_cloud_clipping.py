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







class PointCloud2Wrapper_PurePython(PointCloud2Wrapper):
    def __init__(self, point_cloud_2:PointCloud2):
        self._date = deepcopy(point_cloud_2.data)
        self._fields:list[PointField] = deepcopy(point_cloud_2.fields)
        self._point_step = point_cloud_2.point_step
        self._row_step = point_cloud_2.row_step
        self._height = point_cloud_2.height 
        self._width = point_cloud_2.width
        # Для проверки
        assert (self._row_step % self._point_step)==0 , \
            "row step должен делиться на point step без остатка"

        # self.data_types:tuple(str,int) = {point_cloud_2}
    
    def __getitem__(self, index):
        if index == self.__len__():
            raise StopIteration
        point_start_index = index * self._point_step
        fields_turtle = {}
        for field in self._fields:
            dataflag = "" 
            size = 0
            if field.datatype == 1:
                dataflag = "b"
                size = 1
            elif field.datatype == 2:
                dataflag = "B"
                size = 1
            elif field.datatype == 3:
                dataflag = "h"
                size = 2
            elif field.datatype == 4:
                dataflag = "H"
                size = 2
            elif field.datatype == 5:
                dataflag = "i"
                size = 4
            elif field.datatype == 6:
                dataflag = "I"
                size = 4 
            elif field.datatype == 7:
                dataflag = "f"
                size = 4 
            elif field.datatype == 8:
                dataflag = "d"
                size = 8
            else:
                raise ValueError("Неизвестный формат данных")
            field_start_index = point_start_index + field.offset
            field_value = struct.unpack(dataflag, self._date[field_start_index:field_start_index+size])
            fields_turtle[field.name] = field_value
        return fields_turtle
    
    def __len__(self):
        return self._width * self._height




class PointCloudClipping(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            PointCloud2,
            'points',
            self.clipping_and_publish,
            QoSProfile(reliability=QoSReliabilityPolicy.BEST_EFFORT,depth=5))
        
    def clipping_and_publish(self, msg:PointCloud2):
        pcw = PointCloud2Wrapper_PurePython(msg)
        self.get_logger().info('I heard msg with points: %s' % len(pcw))




def main(args=None):
    rclpy.init(args=args)
    point_cloud_clipping = PointCloudClipping()
    
    rclpy.spin(point_cloud_clipping)
    


if __name__ == '__main__':
    # main()
    print(int("1"))
