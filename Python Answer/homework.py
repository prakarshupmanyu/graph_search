#!/usr/bin/python
import sys

#Function to read the input file. Input file is should be in the format as defined in the problem statement.
def readInputFile(fileName):
	file = open(fileName, 'r')
	returnVal = {}
	returnVal['algorithm'] = file.readline().rstrip('\n').rstrip('\r')
	returnVal['startState'] = file.readline().rstrip('\n').rstrip('\r')
	returnVal['goalState'] = file.readline().rstrip('\n').rstrip('\r')
	returnVal['numTrafficlines'] = int(file.readline().rstrip('\n').rstrip('\r'))

	adjList = {}

	i = 0
	while i < returnVal['numTrafficlines']:
		lineList = file.readline().rstrip('\n').rstrip('\r').split(' ')
		if not lineList[0] in adjList:
			adjList[lineList[0]] = []	#for dictionary of list of dictionaries
		adjList[lineList[0]].append({lineList[1]:lineList[2]})
		i += 1

	sundayLines = {}
	returnVal['numSundayLine'] = int(file.readline().rstrip('\n').rstrip('\r'))
	i = 0
	while i < returnVal['numSundayLine']:
		lineList = file.readline().rstrip('\n').rstrip('\r').split(' ')
		if not lineList[0] in sundayLines:
			sundayLines[lineList[0]] = lineList[1]
		i += 1

	returnVal['adjList'] = adjList
	returnVal['sundayLines'] = sundayLines
	file.close()
	return returnVal

#This is only for cases other than A* because then the heuristic Sunday distances have no impact. Changing them to zero here so that we can have a genric code based addition later in the code for all algorithms
def changeSundayTrafficToZero(fileData):
	for key in fileData['sundayLines']:
		fileData['sundayLines'][key] = 0
	return fileData

def getNodeKeyIndexInParentNodeLOD(LOD, node):
	for index, dic in enumerate(LOD):
		if node in dic:
			return index

def createOutputFile(inputData, path):
	outputFile = open("output.txt", 'w')
	pathCost = 0
	parentNode = ''
	for node in path:
		if parentNode:	#Won't enter this block for the first time
			if inputData['algorithm'] == 'BFS' or inputData['algorithm'] == 'DFS':
				pathCost += 1
			else:
				print inputData['adjList'][parentNode]
				keyOfNodeInParentNode = getNodeKeyIndexInParentNodeLOD(inputData['adjList'][parentNode], node)
				pathCost += int(inputData['adjList'][parentNode][keyOfNodeInParentNode][node])
		outputLine = str(node) + " " + str(pathCost) + "\n"
		outputFile.write(outputLine)
		parentNode = node
	outputFile.close()

def getPathFromParent(ss, gs, parentMapping):
	print ss
	print gs
	print parentMapping
	path = []
	currentNode = gs
	while currentNode != ss:
		path.append(currentNode)
		currentNode = parentMapping[currentNode]
	path.append(currentNode)
	path.reverse()
	print path
	return path

def getBFSOutput(inputData):
	print "I am here : getBFSOutput"
	parentMapping = {}
	pathQueue = [inputData['startState']]
	while 1:
		if not pathQueue:
			print "Failure: No Solution"
			return "Failure: No Solution"
		city = pathQueue.pop(0)
		if city == inputData['goalState']:
			return getPathFromParent(inputData['startState'], city, parentMapping)
		else:
			if city in inputData['adjList']:
				for adjNodes in inputData['adjList'][city]:
					pathQueue.extend(adjNodes.keys())
					if not adjNodes.keys()[0] in parentMapping:	#this check is only there in BFS
						parentMapping[adjNodes.keys()[0]] = city

def childInQueue(child, queue):
	state = child.keys()[0]
	print state
	print queue
	index = 1
	for node in queue:
		if state == node.keys()[0]:
			print "child is in queue"
			return index
		index += 1
	print "child is NOT in queue"
	return False

def insertChildInSortedPosition(child, queue, pathCost, parent, sundayLines):
	print "Inserting "+str(child)+" into queue "+str(queue)+". New cost is : "+str(pathCost)
	state = child.keys()[0]
	newNode = {state:[pathCost,parent]}
	insertPosition = 0
	for existingNode in queue:
		print "Comparing ("+str(existingNode.values()[0][0])+" + "+str(sundayLines[existingNode.keys()[0]])+") and ("+str(pathCost)+" + "+str(sundayLines[state])+")"
		cost = existingNode.values()[0][0] + int(sundayLines[existingNode.keys()[0]])
		if int(cost) <= int(pathCost) + int(sundayLines[state]):
			print "new cost is higher"
			insertPosition += 1
		else:
			break;
	queue.insert(insertPosition, newNode)
	print "new queue : "+str(queue)
	return queue

def getDFSOutput(inputData):
	print "I am here : getDFSOutput"
	enQueue = [{inputData['startState']:[0,'']}]	#open queue
	pathQueue = []	#closed queue
	parentMapping = {}
	while 1:
		print "Queue is : "+str(enQueue)
		if not enQueue:
			print "Failure: No Solution"
			return "Failure: No Solution"
		city = enQueue.pop(0)	#this is a dictionary
		state = city.keys()[0]
		nodePathCost = city[state][0]
		print "current Node : "+str(state)
		if state == inputData['goalState']:
			return getPathFromParent(inputData['startState'], state, parentMapping)
		else:
			childrenToAdd = []
			if state in inputData['adjList']:
				children = inputData['adjList'][state]
				print "children : "+str(children)
				for child in children:
					childNodeCost = int(nodePathCost) + 1
					childState = child.keys()[0]
					if not childInQueue(child, enQueue) and not childInQueue(child, pathQueue):
						childrenToAdd.append({childState:[childNodeCost,state]})
						parentMapping[childState] = state
					elif childInQueue(child, enQueue):
						index = childInQueue(child, enQueue) - 1	#index + 1 is returned
						if childNodeCost + int(inputData['sundayLines'][child.keys()[0]]) < int(enQueue[index].values()[0][0]) + int(inputData['sundayLines'][enQueue[index].keys()[0]]):
							print "replacing enqueue"
							del enQueue[index]
							childrenToAdd.append({childState:[childNodeCost,state]})
							parentMapping[childState] = state
							print "new enqeue : "+str(enQueue)
					elif childInQueue(child, pathQueue):
						index = childInQueue(child, pathQueue) - 1
						if childNodeCost + int(inputData['sundayLines'][child.keys()[0]]) < int(pathQueue[index].values()[0][0]) + int(inputData['sundayLines'][pathQueue[index].keys()[0]]):
							print "replacing pathQueue"
							del pathQueue[index]
							childrenToAdd.append({childState:[childNodeCost,state]})
							parentMapping[childState] = state
							print "new pathQueue : "+str(pathQueue)
				enQueue = childrenToAdd + enQueue
		pathQueue.append(city)
		print "PathQueue is : "+str(pathQueue)

#This algorithm is similar to A*. The only difference is that in A* we use heuristic values as well. So, for UCS we changed to heuristic values to zero above which makes this function reusable for A*.					
def getUCSOutput(inputData):
	print "I am here : getUCSOutput"
	enQueue = [{inputData['startState']:[0,'']}]	#open queue
	pathQueue = []	#closed queue
	parentMapping = {}
	while 1:
		if not enQueue:
			print "Failure: No Solution"
			return "Failure: No Solution"
		city = enQueue.pop(0)	#this is a dictionary
		state = city.keys()[0]
		nodePathCost = city[state][0]
		print "current Node : "+str(state)
		if state == inputData['goalState']:
			return getPathFromParent(inputData['startState'], state, parentMapping)
		else:
			children = []
			if state in inputData['adjList']:
				children = inputData['adjList'][state]
				print "children : "+str(children)
				for child in children:
					childNodeCost = nodePathCost + int(child.values()[0])
					if not childInQueue(child, enQueue) and not childInQueue(child, pathQueue):
						enQueue = insertChildInSortedPosition(child, enQueue, childNodeCost, state, inputData['sundayLines'])
						parentMapping[child.keys()[0]] = state
					elif childInQueue(child, enQueue):
						index = childInQueue(child, enQueue) - 1	#index + 1 is returned
						if childNodeCost + int(inputData['sundayLines'][child.keys()[0]]) < int(enQueue[index].values()[0][0]) + int(inputData['sundayLines'][enQueue[index].keys()[0]]):
							print "replacing enqueue"
							del enQueue[index]
							enQueue = insertChildInSortedPosition(child, enQueue, childNodeCost, state, inputData['sundayLines'])
							parentMapping[child.keys()[0]] = state
							print "new enqeue : "+str(enQueue)
					elif childInQueue(child, pathQueue):
						index = childInQueue(child, pathQueue) - 1
						if childNodeCost + int(inputData['sundayLines'][child.keys()[0]]) < int(pathQueue[index].values()[0][0]) + int(inputData['sundayLines'][pathQueue[index].keys()[0]]):
							print "replacing pathQueue"
							del pathQueue[index]
							pathQueue = insertChildInSortedPosition(child, pathQueue, childNodeCost, state, inputData['sundayLines'])
							parentMapping[child.keys()[0]] = state
							print "new pathQueue : "+str(pathQueue)
		pathQueue.append(city)
		print "PathQueue is : "+str(pathQueue)
					
def getAStarOutput(inputData):
	print "I am here : getAStarOutput"
	return getUCSOutput(inputData)

def main():
	#Program starts here. Input file should be in the same directory as homework.py (this file)
	fileData = readInputFile("input.txt")

	if fileData['algorithm'] != 'A*':
		fileData = changeSundayTrafficToZero(fileData)

	print fileData

	algoFunctionToCall = {'BFS':getBFSOutput,'DFS':getDFSOutput,'UCS':getUCSOutput,'A*':getAStarOutput}

	requiredPath = algoFunctionToCall[fileData['algorithm']](fileData)

	print requiredPath
	
	createOutputFile(fileData, requiredPath)

main()
