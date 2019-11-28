import RasterMap

client = RasterMap.RasterMapApi()
region = "Tainan"
event = 1
data_type = RasterMap.HydrologicalDataType.Flood

print("1- list Regions:")
regions = client.GetRegionList()
print(regions)

print("2- Metadata")
descriptor = client.GetEventDescriptor(region, event, data_type, RasterMap.DescriptorTypes.DAS)
print(descriptor)

print("3- Grid")
default_range = RasterMap.Range()
default_range.Start = 0
default_range.Step = 1
default_range.Stop = 2
grid = client.GetGeoGrid(region, event, data_type, "Depth", time_range=default_range, x_range=default_range,
                         y_rang=default_range)
print(grid)

print("4- Run Function")
function = "time[0:1:20]"
result = client.RunFunction(region, event, data_type, function)
print(result)

print("5- Downloading event file ....")
fileName = client.GetEventNetCDFFile(region, event, data_type)
print("File location: {0}".format(fileName))

print("6- Downloading event file as ASCII...")
ascii = client.GetEventASCIIFile(region, event, data_type)
print("ASCII file location{0}".format(ascii))
