from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
import numpy as np
from array import array
from copy import deepcopy
import struct


class PointCloud2Wrapper_NumPy():
    pointfield_datatype_to_numpy_dtype = {1:"int8", 2:"uint8", 3:"int16",4:"uint16",5:"int32",6:"uint32",7:"float32",8:"float64"}


    def __init__(self, point_cloud_2: PointCloud2):
        self._fields = PointCloud2Wrapper_NumPy._from_pointcloud2_to_numpy(
            data_fun=point_cloud_2.data,
            fields=point_cloud_2.fields,
            row_step=point_cloud_2.row_step,
            point_step=point_cloud_2.point_step,
            width=point_cloud_2.width,
            height=point_cloud_2.height,
        )

        self._height = point_cloud_2.height
        self._width = point_cloud_2.width

        # Для проверки
        assert (
            point_cloud_2.row_step % point_cloud_2.point_step
        ) == 0, "row step должен делиться на point step без остатка"

    def _from_pointcloud2_to_numpy(
        data_fun, fields: list[PointField], row_step, point_step, width, height
    ):
        typle_field = {}
        data = data_fun
        for field in fields:
            datatype, size = PointCloud2Wrapper_NumPy._get_dtype_and_size(field)
            bytes_list = array("B")

            typle_field[field.name] = {"datatype": datatype, "bytes": bytes_list}

            number_of_points = width * height
            for start_index_point in range(
                0, number_of_points * point_step, point_step
            ):
                start_index_point += field.offset
                bytes_list[0:0] = data[start_index_point : start_index_point + size]
        for field_name, field_tuple in typle_field.items():
            typle_field[field_name] = np.frombuffer(
                field_tuple["bytes"], dtype=field_tuple["datatype"]
            )
        return typle_field

    def __getitem__(self, index):
        if index == self.__len__():
            raise StopIteration

        return_dict = {}
        for k, v in self._fields.items():
            return_dict[k] = v[index]
        return return_dict

    def __len__(self):
        return self._height * self._width

    def shape(self):
        return (self._width, self._height)

    def getPointCloud2(self):
        msg = PointCloud2()

    def _get_dtype_and_size(field: PointField) -> (str, int):
        dtype = PointCloud2Wrapper_NumPy.pointfield_datatype_to_numpy_dtype[field.datatype]
        size = int(int(dtype.split('t')[1])/8)

        return dtype, size
