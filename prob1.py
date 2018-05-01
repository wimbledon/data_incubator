import numpy as np
import math

def calculateDeviation(x,y,m,n):
	return abs(x/m - y/n)

def caculateDeviationStats(m,n,cp=None,pt=None):
	array2d = [[None for x in range(n+1)] for y in range(m+1)]

	for x in range(m+1):
		array2d[x][0] = [calculateDeviation(x,0,m,n)]

	for y in range(n+1):
		array2d[0][y] = [calculateDeviation(0,y,m,n)]


	for x in range(1, m+1):
		for y in range(1, n+1):
			newCells = array2d[x-1][y].copy()
			newCells.extend(array2d[x][y-1].copy())
			newD = calculateDeviation(x,y,m,n)
			array2d[x][y] = [max(newD, oldD) for oldD in newCells]

	result = array2d[m][n]
	if cp:
		result = [r for r in result if r > cp]

	condResult = [r for r in result if r > pt] if pt else []
	condProb = len(condResult) / len(result)

	return (np.mean(result), np.std(result), len(result), condProb)

def caculateDeviationStats2(m,n,cp=None,pt=None):
	array2d = [[None for x in range(n+1)] for y in range(m+1)]

	for x in range(m+1):
		array2d[x][0] = {calculateDeviation(x,0,m,n) : 1}

	for y in range(n+1):
		array2d[0][y] = {calculateDeviation(0,y,m,n) : 1}


	for x in range(1, m+1):
		for y in range(1, n+1):
			leftMap = array2d[x-1][y]
			topMap = array2d[x][y-1]
			allKeys = list(leftMap.keys())
			allKeys.extend(topMap.keys())
			allKeys = set(allKeys)
			
			newMap = {}
			updateCount = 0
			newD = calculateDeviation(x,y,m,n)
			for k in allKeys:
				c = 0
				if k in leftMap:
					c += leftMap[k]
				if k in topMap:
					c += topMap[k]

				if k < newD:
					updateCount += c
				else:
					newMap[k] = c

			if updateCount:
				newMap[newD] = newMap[newD] + updateCount if newD in newMap else updateCount
			
			array2d[x][y] = newMap

	resultMap = array2d[m][n]

	if cp:
		delKeys = []
		for k in resultMap:
			if k <= cp:
				delKeys.append(k)
		for k in delKeys:
			del resultMap[k]

	totalCount = 0
	total = 0
	condCount = 0
	for k in resultMap:
		totalCount += resultMap[k]
		total += k * resultMap[k]
		if pt and k > pt:
			condCount += resultMap[k]

	mean = total / totalCount
	totalSquareDiff = 0
	for k in resultMap:
		totalSquareDiff += math.pow((k - mean),2) * resultMap[k]

	std = math.sqrt(totalSquareDiff / totalCount)

	condProb = condCount / totalCount

	return (mean, std, totalCount, condProb)


print (caculateDeviationStats(11, 7))
print (caculateDeviationStats2(11, 7))
print (caculateDeviationStats2(23, 31))

print ('conditional:')
print (caculateDeviationStats(11, 7, 0.2, 0.6))
print (caculateDeviationStats2(11, 7, 0.2, 0.6))
print (caculateDeviationStats2(23, 31, 0.2, 0.6))

# print (caculateDeviationStats(23,31))


# m = 21
# n = 21

# array2d = [[0 for x in range(n)] for y in range(m)]

# def visitCell(x, y):
# 	array2d[x][y] += 1
# 	if x < m-1:
# 		visitCell(x+1, y)
# 	if y < n-1:
# 		visitCell(x, y+1)

# visitCell(0,0)

# for x in array2d:
# 	print (x)

	