from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
import numpy as np
from array import array
from copy import deepcopy
import struct




class PointCloud2Wrapper():
    def __getitem__(self, index):
        pass
    def __len__(self):
        pass

class PointCloud2Wrapper_NumPy(PointCloud2Wrapper):
    
    def __init__(self, point_cloud_2:PointCloud2):
        self.points = PointCloud2Wrapper_NumPy._from_pointcloud2_to_numpy(
             data_fun = point_cloud_2.data,
             fields = point_cloud_2.fields,
             row_step = point_cloud_2.row_step,
             point_step = point_cloud_2.point_step,
             width = point_cloud_2.width,
             height = point_cloud_2.height
            )
        self._height = point_cloud_2.height 
        self._width = point_cloud_2.width
        # Для проверки
        assert (point_cloud_2.row_step % point_cloud_2.point_step)==0 , \
            "row step должен делиться на point step без остатка"

    def _from_pointcloud2_to_numpy(data_fun,fields:list[PointField], row_step, point_step,width,height):
        typle_field = {}
        data = data_fun
        for field in fields:
            datatype = "" 
            size = 0
            if field.datatype == 1:
                datatype = "int8"
                size = 1
            elif field.datatype == 2:
                datatype = "uint8"
                size = 1
            elif field.datatype == 3:
                datatype = "int16"
                size = 2
            elif field.datatype == 4:
                datatype = "uint16"
                size = 2
            elif field.datatype == 5:
                datatype = "int32"
                size = 4
            elif field.datatype == 6:
                datatype = "uint32"
                size = 4 
            elif field.datatype == 7:
                datatype = "float32"
                size = 4 
            elif field.datatype == 8:
                datatype = "float64"
                size = 8
            else:
                raise ValueError("Неизвестный формат данных")
            
            bytes_list = array('B')
            typle_field[field.name] = {"datatype":datatype,"bytes":bytes_list}
            
            number_of_points = width*height
            for start_index_point in range(0,number_of_points*point_step,point_step):
                start_index_point+=field.offset
                bytes_list[0:0]=(data[start_index_point:start_index_point+size])
        for field_name, field_tuple in typle_field.items():
            typle_field[field_name] = np.frombuffer(field_tuple["bytes"],dtype = field_tuple["datatype"])
        return typle_field

    def __getitem__(self, index):
        pass
# In [73]: a = array('b',[0,0,25,0,0,0,0,0])

# In [74]: len(a)
# Out[74]: 8

# In [75]: np.frombuffer(a, dtype=np.uint32)
# Out[75]: array([1638400,       0], dtype=uint32)

            
            
            
    # Преоброзования массива в numpy

    def __getitem__(self, index):
        pass

    def __len__(self):
        pass

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

