import zlib
import time
import datetime
import json
import csv
import csv
import json
import ast
import gzip
from io import BytesIO
import zlib, base64
import os
from os import listdir
import os.path
import sys
from os import listdir
from os.path import isfile, join
import os
from distutils.dir_util import copy_tree
from shutil import copytree,copy2
import random
import math

scalDict = {}
scalDict['CapeTown_SA']= 400
scalDict['Delhi_India']= 214
scalDict['Dubai_UAE']= 360
scalDict['London_UK']= 248
scalDict['Melbourne_AU']= 267
scalDict['MexicoCity_Mexico']= 480
scalDict['NY_US']= 700
scalDict['Paris_France']= 320
scalDict['Toronto_Canada']= 540
scalDict['Brussels']= 5280
scalDict['Chicago']= 5280


cityCoords = {}


cityCoords['Chicago'] = [
42.027509, -87.937992,
42.024449, -87.512272,

41.636632, -87.403782,
41.635606, -87.966831
]


cityCoords['Brussels'] = [
50.901529, 4.313933,
50.905209, 4.437873,
50.796182, 4.305350,
50.793578, 4.447829
]
cityCoords['CapeTown_SA'] = [
	#Upper left
	-33.883335, 18.406432,
	#upper right
	-33.916207, 18.482190,
	#lower right
	-33.986281, 18.416868,
	#lower left
	-33.928146, 18.367802
]
cityCoords['Delhi_India'] = [
	#Upper left
	28.646704, 77.210614,
	#upper right
	28.631700, 77.246496,
	#lower right
	28.604083, 77.224511,
	#lower left
	28.623785, 77.180172
	]
cityCoords['Dubai_UAE'] =[
	#Upper left
 	 25.240883, 55.266705,
	#upper right
	25.220604, 55.307707,
	#lower right
	25.164689, 55.287399,
	#lower left
	25.191280, 55.227056
	]
cityCoords['London_UK'] = [
	#Upper left
	 51.522228, -0.141252,
	#upper right
	51.505636, -0.094690,
	#lower right
	51.479329, -0.138679,
	#lower left
	51.502603, -0.183319

	]
cityCoords['Melbourne_AU'] = [
	#Upper left
	-37.797075, 144.929560,
	#upper right
	-37.785780, 144.990381,
	#lower right
	# - lr =
	-37.826746, 145.012124,
	# - ll =
	-37.832270, 144.950543


	]
cityCoords['MexicoCity_Mexico'] = [
	# ul =
	19.440709, -99.164739,
	# - ur =
	19.448003, -99.079002,
	# - lr =
	19.381734, -99.072126,
	# - ll =
	19.379098, -99.156144


	]
cityCoords['NY_US'] = [
	# - ul =
	40.770340, -73.994651,
	# - ur =
	40.758978, -73.958549,
	# - lr =
	40.741913, -73.972914,
	# - ll =
	40.753631, -74.007501
	]
cityCoords['Paris_France'] = [
	# - ul =
	48.871733, 2.342533,
	# - ur =
	48.857965, 2.394968,
	# - lr =
	48.812720, 2.361921,
	# - ll =
	48.821134, 2.298911

	]
cityCoords['Toronto_Canada'] = [
	# - ul =
	43.664690, -79.438654,
	# - ur =
	43.676751, -79.375619,
	# - lr =
	43.629573, -79.350675,
	# - ll =
	43.618387, -79.422794

	]



def haversine(coord1, coord2):
	R = 6372800  # Earth radius in meters
	lat1, lon1 = coord1
	lat2, lon2 = coord2

	phi1, phi2 = math.radians(lat1), math.radians(lat2)
	dphi       = math.radians(lat2 - lat1)
	dlambda    = math.radians(lon2 - lon1)

	a = math.sin(dphi/2)**2 + \
		math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

	return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))*3.28084

def divideCordinates(cityName,mileFactor):

	cityCoordsList = cityCoords[cityName]

	upperLeft = (cityCoordsList[0],cityCoordsList[1])
	upperRight = (cityCoordsList[2],cityCoordsList[3])
	lowerRight = (cityCoordsList[4],cityCoordsList[5])
	lowerLeft = (cityCoordsList[6],cityCoordsList[7])

	upperHorizontalDistance = haversine(upperLeft, upperRight)
	lowerHorizontalDistance = haversine(lowerLeft, lowerRight)
	leftVerticalDistance = haversine(upperLeft, lowerLeft)
	rightVerticalDistance = haversine(upperRight, lowerRight)
	# print (upperHorizontalDistance,lowerHorizontalDistance)
	# print(leftVerticalDistance,rightVerticalDistance)

	maxVal =upperHorizontalDistance
	if maxVal < lowerHorizontalDistance:
		maxVal = lowerHorizontalDistance
	numOfCols = int(math.ceil(maxVal/mileFactor))

	maxVal =leftVerticalDistance
	if maxVal < rightVerticalDistance:
		maxVal = rightVerticalDistance
	numOfRows = int(math.ceil(maxVal/mileFactor))

	print(numOfRows,numOfCols)

	numberOfThreadsInRow = numOfRows
	leftColCoords = []
	#get left col coords
	x1 = cityCoordsList[0]
	y1 = cityCoordsList[1]
	x2 = cityCoordsList[6]
	y2 = cityCoordsList[7]

	slope = (y2-y1)/(x2-x1)
	yRatio = y2 - y1
	xRatio = x2 - x1

	i = 0

	cindex =0
	while i<= 1.0001:
		str3 = "%.6f" % (x1+((i) * xRatio))
		leftColCoords.append(float(str3))
		cindex += 1
		str3 = "%.6f" % (y1+((i) * yRatio))
		str3+="3"
		leftColCoords.append(float(str3))
		cindex += 1
		i = i + (1/(numberOfThreadsInRow-1))


	#right col coords
	numberOfThreadsInRow = numOfRows
	rightColCoords = []
	x1 = cityCoordsList[2]
	y1 = cityCoordsList[3]
	x2 = cityCoordsList[4]
	y2 = cityCoordsList[5]

	slope = (y2-y1)/(x2-x1)
	yRatio = y2 - y1
	xRatio = x2 - x1

	i = 0

	cindex =0
	while i<= 1.0001:
		str3 = "%.6f" % (x1+((i) * xRatio))
		rightColCoords.append(float(str3))
		cindex += 1
		str3 = "%.6f" % (y1+((i) * yRatio))
		str3+="3"
		rightColCoords.append(float(str3))
		cindex += 1
		i = i + (1/(numberOfThreadsInRow-1))



	cityDividedCoords = []

	j = 0
	while j<len(rightColCoords)-1:

		numberOfThreadsInRow = numOfRows
		newRowCords = []
		# print(j)
		x1 = leftColCoords[j]
		y1 = leftColCoords[j+1]
		x2 = rightColCoords[j]
		y2 = rightColCoords[j+1]

		slope = (y2-y1)/(x2-x1)
		yRatio = y2 - y1
		xRatio = x2 - x1

		i = 0

		cindex =0
		while i<= 1.0001:
			str3 = "%.6f" % (x1+((i) * xRatio))
			newRowCords.append(round(float(str3),5))
			cindex += 1
			str3 = "%.6f" % (y1+((i) * yRatio))
			str3+="3"
			newRowCords.append(round(float(str3),5))
			cindex += 1
			i = i + (1/(numberOfThreadsInRow-1))
		j+=2
		cityDividedCoords.append(newRowCords)
	# print(len(leftColCoords),len(rightColCoords))

	#get right col coords


	# print(len(cityDividedCoords))

	cityFileTxt = open('CityCoords2/'+cityName+'.txt','w')
	# print('var ',cityName,' = [',end=' ')
	cityFileTxt.write('var '+cityName+' = [')
	i = 0
	while i < len(cityDividedCoords)-1:
		j = 0

		item = []

		rowItems = 0
		while j < len(cityDividedCoords[i])-2:
			# print(len(cityCoords[i]))
			upperLeft = [cityDividedCoords[i][j],cityDividedCoords[i][j+1]]
			lowerRight = [cityDividedCoords[i+1][j+2],cityDividedCoords[i+1][j+3]]

			midX = (upperLeft[0]+lowerRight[0])/2
			midy = (upperLeft[1]+lowerRight[1])/2
			item.append(round(float(midX),5))
			item.append(round(float(midy),5))

			cityFileTxt.write(str(round(float(midX),5))+','+str(round(float(midy),5))+',')
			rowItems+=1
			j+=2
		# print(rowItems)
		i+=1

	cityFileTxt.write('];')
	cityFileTxt.close()


	# # for row in cityDividedCoords:
	# # 	for item in row:
	# # 		# print(item,end=',')
	# # 		cityFileTxt.write(str(item)+',')
	# # # print(']',end=';')
	# # cityFileTxt.write('];')
	# # cityFileTxt.close()


	cityFileTxt = open('CityCoords2/'+cityName+'Code.txt','w')
	cityFileTxt.write(' [')

	# print('var ',cityName,' = [',end=' ')
	# cityFileTxt.write('var '+cityName+'\n')
	for row in cityDividedCoords:
		# for item in row:
			# print(item,end=',')
		cityFileTxt.write(str(row)+',\n')
	cityFileTxt.write('];')
	cityFileTxt.close()
	# print(']',end=';')
	# cityFileTxt.write('];')


	# cityFileTxt = open('CityCoords/'+cityName+'.txt','w')
	# for row in cityDividedCoords:
	# 	for item in row:
	# 		# print(item,end=',')
	# 		cityFileTxt.write(str(row)+',')
	# cityFileTxt.close()
	# # print(']',end=';')
	# # cityFileTxt.write('];')




if __name__== "__main__":


	passedCity = sys.argv[1]
	mileFactor = scalDict[passedCity] # to achieve granularity
	divideCordinates(passedCity,mileFactor)
