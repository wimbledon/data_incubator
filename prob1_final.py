import math

def calculateDeviation(x,y,m,n):
	return abs(x/m - y/n)

def caculateDeviationStats(m,n):
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

	return array2d[m][n]


def calculateMeanAndStd(resultMap):
	totalCount = 0
	total = 0
	for k in resultMap:
		totalCount += resultMap[k]
		total += k * resultMap[k]

	mean = total / totalCount

	totalSquareDiff = 0
	for k in resultMap:
		totalSquareDiff += math.pow((k - mean),2) * resultMap[k]

	std = math.sqrt(totalSquareDiff / totalCount)

	return (mean, std)

def caculateCondProb(resultMap, cp, pt):
	totalCount = 0
	condCount = 0
	for k in resultMap:
		if k > cp:
			totalCount += resultMap[k]
		if k > pt:
			condCount += resultMap[k]

	return condCount / totalCount


s1 = caculateDeviationStats(11, 7)
s2 = caculateDeviationStats(23, 31)

print ('m:11, n:7, {}'.format(calculateMeanAndStd(s1)))
print ('m:23, n:31, {}'.format(calculateMeanAndStd(s2)))

print ('m:11, n:7, cp:0.2, pt:0.6, {}'.format(caculateCondProb(s1, 0.2, 0.6)))
print ('m:23, n:31, cp:0.2, pt:0.6, {}'.format(caculateCondProb(s2, 0.2, 0.6)))

