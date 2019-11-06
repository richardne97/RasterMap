import requests
import xml.etree.ElementTree
import re
import os
from enum import Enum


class DescriptorTypes(Enum):
    DDX = 'ddx'
    DAS = 'das'
    DDS = 'dds'


class RasterMapApi:

    def __init__(self, url="http://192.168.12.15/NCHC"):
        self.url = url

    def GetRegionList(self):
        """Get region list. 取得區域基本資料列表"""
        regions = requests.get("{0}/RasterMap/Regions/List/All".format(self.url)).json()
        return regions

    def GetEventList(self, region):
        """Get event list for a region. 取得指定區域中，所有事件列表，事件試以NetCDF檔案格式儲存"""
        response = requests.get("{0}/RasterMap/Events/List/{1}".format(self.url, region))
        if response.status_code == 200:
            return response.json()
        else:
            return "Request fail"

    def GetEventDescriptor(self, region, event, descriptorType):
        """ Get descriptor (XML format) from event file (.nc). The return type is xml.etree.ElementTree
            取得事件檔案中的詮釋資料，包括DDX, DDS, DAS
        """

        if not isinstance(descriptorType, DescriptorTypes):
            raise TypeError('descriptorType must be an instance of DescriptorTypes Enum')
        response = requests.get(
            "{0}/RasterMap/Get/Region/{1}/Event/{2}/{3}".format(self.url, region, event, descriptorType.value))
        if response.status_code == 200:
            return xml.etree.ElementTree.fromstring(response.content)
        else:
            return "Request fail"

    def GetEventNetCdfFile(self, region, event, outputFilePath=os.curdir):
        """ Download NetCDF file of an event
            下載某個事件的NetCDF檔案，並且寫入指定路徑
            :param region: region name
            :param event: event name
            :param outputFilePath: (optional) folder that save the downloaded file, if it is not assigned, it will be given as os.curdir
            :return: file name with full file path
        """
        response = requests.get("{0}/RasterMap/File/Download/Original/Region/{1}/Event/{2}/".format(self.url, region, event), allow_redirects=True)
        if response.status_code == 200:
            fileName = re.findall('filename=(.+)', response.headers.get('content-disposition'))
            fileNameFullPath = "{0}/{1}".format(outputFilePath, fileName[0])
            open(fileNameFullPath, 'wb').write(response.content)
            return fileNameFullPath
        else:
            return "Request fail"

    def GetEventASCIIFile(self, region, event, outputFilePath=os.curdir):
        """
        Download ASCII converted NetCDF filef of an event
        :param region: region name
        :param event: event name
        :param outputFilePath: (optional) folder that save the downloaded file, if it is not assigned, it will be given as os.curdir
        :return: file name with full file path
        """
        response = requests.get("{0}/RasterMap/File/Download/ASCII/Region/{1}/Event/{2}/".format(self.url, region, event))
        if response.status_code == 200:
            fileName = re.findall('filename=(.+)', response.headers.get('content-disposition'))
            fileNameFullPath = "{0}/{1}".format(outputFilePath, fileName[0])
            open(fileNameFullPath, 'wb').write(response.content)
            return fileNameFullPath
        else:
            return "Request fail"

    def GetEventASCII(self, region, event, outputFilePath=os.curdir):
        response = requests.get("{0}/RasterMap/NetCDF/DisplayText/Region/{1}/Event/{2}/".format(self.url, region, event))
        if response.status_code == 200:
            return response.contnet
        else:
            return "Request fail"

    def GetEventASCIIWithPreprocessor(self, region, event, preprocessor):
        body = {
                    "RegionId": region,
                    "EventId": event,
                    "Function": preprocessor
                }
        response = requests.post("{0}/RasterMap/NetCDF/Execute".format(self.url), data=body)
        if response.status_code == 200:
            return response.content
        else:
            return "Request fail"

    def GetGeoGrid(self, region, event, variableName, unixTimeInMin, luCorX, luCorY, rdCorX, rdCorY):
        """Get partial grid values from a netCDF file"""
        body = {
            "RegionId": region,
            "EventId": event,
            "VariableName": variableName,
            "UnixTimeInMin": unixTimeInMin,
            "LeftUpCornerX": luCorX,
            "LeftUpCornerY": luCorY,
            "RightDownCornerX": rdCorX,
            "RightDownCornerY": rdCorY
        }
        response = requests.post("{0}/RasterMap/NetCDF/Get".format(self.url), data=body)
        if response.status_code == 200:
            return response.content
        else:
            return "Request fail"
