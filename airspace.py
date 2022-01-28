# Jackson Spray
# Given airspace data .xml file,
# Create a map of the US with airspaces overlayed

import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap


def showFormat(root):
	print("\n\n")
	for x in root[0]:
		print(x.tag, x.attrib)

def printAllAirspaceNames(root):
	print("\n\n")
	for x in root.findall('ASP'):
		asp = x.find('NAME').text
		return asp

def aspByName(root, name):
	for x in root.findall('ASP'):
		asp = x.find('NAME').text
		if (asp == name):
			print(asp)

def aspHeight(root, name):
	for x in root.findall('ASP'):
		asp = x.find('NAME').text
		if (asp == name):
			return x.find('ALTLIMIT_TOP').find('ALT').text

def aspGeo(root, name):
	for x in root.findall('ASP'):
		asp = x.find('NAME').text
		if (asp == name):
			value = x.find('GEOMETRY').find('POLYGON').text
			return value

def getAspCount(root):
	count = 0
	for x in root.findall('ASP'):
		count = count + 1
	return count

def graph(arr):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	#United States
	bot_left_lat  =24
	bot_left_lon  =-125
	top_right_lat =50
	top_right_lon = -67

	#DFW Area
	# bot_left_lat  =32.4
	# bot_left_lon  =-97.7
	# top_right_lat =33.4
	# top_right_lon = -96.4

	m = Basemap(resolution='i', projection='cyl', llcrnrlon=bot_left_lon, llcrnrlat=bot_left_lat, urcrnrlon=top_right_lon, urcrnrlat=top_right_lat)
	m.drawcoastlines(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
	m.drawstates()
	m.drawcountries()
	maps = ['ESRI_Imagery_World_2D',    # 0
	        'ESRI_StreetMap_World_2D',  # 1
	        'NatGeo_World_Map',         # 2
	        'NGS_Topo_US_2D',           # 3
	        'Ocean_Basemap',            # 4
	        'USA_Topo_Maps',            # 5
	        'World_Imagery',            # 6
	        'World_Physical_Map',       # 7
	        'World_Shaded_Relief',      # 8
	        'World_Street_Map',         # 9
	        'World_Terrain_Base',       # 10
	        'World_Topo_Map'            # 11
	        ]
	print("Loading image from ArcGIS server....")
	m.arcgisimage(service=maps[6], xpixels=1000, verbose=False)
	print("....finished.")
	patches = []
	for asp in arr:
		patches.append(Polygon(np.array(asp)))
	ax.add_collection(PatchCollection(patches, facecolor='lightgreen', edgecolor='k', linewidths=1.5, alpha=0.3))
	plt.title('Airspaces')
	plt.show()



def main():
	tree = ET.parse("airspaceData.xml")
	root = tree.getroot()
	aspCoordinates = []
	count = 0
	aspNames = []
	lats = []
	longs = []
	Coords = []
	for x in root.findall('ASP'):
		asp = x.find('NAME').text
		aspNames.append(asp)
		bigPoly = aspGeo(root, asp)
		Coords.clear()
		Coords = bigPoly.split()
		lats.clear()
		longs.clear()
		length = len(Coords)
		bigArr = [[0 for i in range(2)] for j in range(length//2)]
		it = 0
		for i in range(0, length):
			try:
				if (i % 2 == 0):
					bigArr[it][0] = Coords[i].replace(',','')
				elif (i % 2 != 0):
					bigArr[it][1] = Coords[i].replace(',','')
					it = it + 1
			except IndexError:
				break
		try:
			while True:
				bigArr.remove([0,0])
		except ValueError:
				pass
		count = count + 1
		aspCoordinates.append(bigArr)
	graph(aspCoordinates)

	
if __name__ == "__main__":
    main()

