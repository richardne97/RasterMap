import os
import re
from enum import Enum

import requests


class DescriptorTypes(Enum):
    DDX = 'ddx'
    DAS = 'das'
    DDS = 'dds'


class Range:
    def __init__(self):
        self.Start = 0
        self.Step = 0
        self.Stop = 0


class HydrologicalDataType(Enum):
    Flood = 'Flood'
    Rainfall = 'Rainfall'


class RasterMapApi:

    def __init__(self, url="http://203.145.220.28/NchcRESTApi"):
        self.url = url

    def GetRegionList(self):
        """Get region list. 取得區域基本資料列表"""
        regions = requests.get("{0}/RasterMap/Regions".format(self.url)).json()
        return regions

    def GetEventDescriptor(self, region, event, data_type, descriptor_type):
        """ Get descriptor (XML format) from event file (.nc). The return type is xml.etree.ElementTree
            取得事件檔案中的詮釋資料，包括DDX, DDS, DAS
        """

        if not isinstance(descriptor_type, DescriptorTypes):
            raise TypeError('descriptorType must be an instance of DescriptorTypes Enum')
        response = requests.get(
            "{0}/RasterMap/{1}/{2}/{3}/netcdf/{4}".format(self.url, region, event, data_type.value,
                                                          descriptor_type.value))
        if response.status_code == 200:
            return response.text
        else:
            return "Request fail"

    def GetEventASCIIFile(self, region, event, data_type, outputFilePath=os.curdir):
        """
        Download ASCII converted NetCDF file of an event
        :param data_type: hydrological type (flood or Rainfall)
        :param region: region name
        :param event: event name
        :param outputFilePath: (optional) folder that save the downloaded file, if it is not assigned, it will be given as os.curdir
        :return: file name with full file path
        """
        response = requests.get(
            "{0}/RasterMap/{1}/{2}/{3}/ascii/file".format(self.url, region, event, data_type.value))
        if response.status_code == 200:
            fileName = re.findall('filename=(.+)', response.headers.get('content-disposition'))
            fileNameFullPath = "{0}/{1}".format(outputFilePath, fileName[0])
            open(fileNameFullPath, 'wb').write(response.content)
            return fileNameFullPath
        else:
            return "Request fail"

    def GetEventNetCDFFile(self, region, event, data_type, outputFilePath=os.curdir):
        """ Download NetCDF file of an event
            下載某個事件的NetCDF檔案，並且寫入指定路徑
            :param region: region name
            :param event: event name
            :param outputFilePath: (optional) folder that save the downloaded file, if it is not assigned, it will be given as os.curdir
            :return: file name with full file path
        """
        response = requests.get(
            "{0}/RasterMap/{1}/{2}/{3}/netcdf/file".format(self.url, region, event, data_type.value),
            allow_redirects=True)
        if response.status_code == 200:
            fileName = re.findall('filename=(.+)', response.headers.get('content-disposition'))
            fileNameFullPath = "{0}/{1}".format(outputFilePath, fileName[0])
            open(fileNameFullPath, 'wb').write(response.content)
            return fileNameFullPath
        else:
            return "Request fail"

    def GetGeoGrid(self, region, event, data_type, variable_name, time_range, x_range, y_rang):
        """Get partial grid values from a netCDF file
        :param region: region name
        :param event: event ID
        :param data_type: Hydrological data type, value of the enum <RasterMap.HydrologicalDataType>
        :param variable_name: variable name
        :param time_range:time range object of type <RasterMap.Range>
        :param x_range: X range object of type <RasterMap.Range>
        :param y_rang: Y range object of type <RasterMap.Range>
        :return: a partial grid of the event in ascii format.
         """
        body = {
            "VariableName": variable_name,
            "Time": {
                "Start": time_range.Start,
                "Step": time_range.Step,
                "Stop": time_range.Stop
            },
            "X": {
                "Start": x_range.Start,
                "Step": x_range.Step,
                "Stop": x_range.Stop
            },
            "Y": {
                "Start": y_rang.Start,
                "Step": y_rang.Step,
                "Stop": y_rang.Stop
            }
        }
        response = requests.post(
            "{0}/RasterMap/{1}/{2}/{3}/ascii/partial".format(self.url, region, event, data_type.value), json=body)
        if response.status_code == 200:
            return response.text
        else:
            return "Request fail {0}".format(response.text)

    def RunFunction(self, region, event, data_type, function):
        """runs a function on a netCDF file"""
        body = {
            "Function": function
        }
        response = requests.post(
            "{0}/RasterMap/{1}/{2}/{3}/ascii/function".format(self.url, region, event, data_type.value), json=body)
        if response.status_code == 200:
            return response.text
        else:
            return "Request fail: {0}".format(response.text)
