import RasterMap
client = RasterMap.RasterMapApi()
region = client.GetRegionList()
events = client.GetEventList(region[0])
descriptor = client.GetEventDescriptor(region[0], events[0], RasterMap.DescriptorTypes.DDX)
grid = client.GetGeoGrid("demo", "1200230_20m_201606110100.nc", "Depth", 24426660, 120.181252, 22.7787, 120.21, 22.59)
#fileName = client.GetEventNetCdfFile("demo", "1200230_20m_201606110100.nc")
ascii = client.GetEventASCIIFile("demo", "1200230_20m_201606110100.nc")
print(ascii)

