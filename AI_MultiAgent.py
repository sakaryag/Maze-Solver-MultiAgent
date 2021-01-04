# Python program to find the shortest
# path between a given source cell
# to a destination cell.
import sys
# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep


from collections import deque

class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == 0

	# for inserting an element in the queue
	def insert(self,node):
		self.queue.append(node)
	# for popping an element based on Priority
	def delete(self,dest):
		try:
			min = 0
			for i in range(len(self.queue)):
				if self.queue[i].dist +manhattan_dist(self.queue[i].pt.x,self.queue[i].pt.y,dest.x,dest.y) < self.queue[min].dist+manhattan_dist(self.queue[min].pt.x,self.queue[min].pt.y,dest.x,dest.y):
					min = i
			item = self.queue[min]
			del self.queue[min]
			return item
		except IndexError:
			print()
			exit()
	def clear(self):
		self.queue.clear()
class Point:
	def __init__(self,x: int, y: int):
		self.x = x
		self.y = y

class Node:
	def __init__(self,pt: Point, dist: int):
		self.pt = pt # The cordinates of the cell
		self.dist = dist # Cell's distance from the source


def isValid(row: int, col: int):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]



#check queue or stack if empty or not
def control_s(queue):
	out=False
	for agent in range(N):
		if not (len(queue[agent])==0):
			 out = out or True

	return out

#check priority queue if empty or not
def control(queue):
	out=False
	for agent in range(N):
		if not queue[agent].isEmpty():
			 out = out or True

	return out

# check any of neighbors Agent or not
def check_neighbors(maze,visited,row: int, col: int):
	count=0
	a_flag=False
	for i in range(4):
		r=row+rowNum[i]
		c=col+colNum[i]

		if maze[r][c] =="A":
			a_flag=True

	if a_flag==True:
		for i in range(4):
			r=row+rowNum[i]
			c=col+colNum[i]
			visited[r][c]=False
	visited[row][col]=False
	return visited


def BFS_Move(maze,queue,back,dest: Point,visited,distance,a):

	if(len(queue)==0):
		return (queue,distance,back,visited)

	curr = queue.popleft() # Dequeue the front cell
	pt = curr.pt

	# make previous node  empty
	maze[back.x][back.y] = "E"

	# make current node Agent

	maze[pt.x][pt.y] = "A"+str(a+1)

	print(a,"->",pt.x,pt.y)

	if pt.x == dest.x and pt.y == dest.y:
		print("Agent Arrived")
		queue.clear()

		return (queue,curr.dist+1,back,visited)
	move_count=0
	visited=check_neighbors(maze,visited,pt.x,pt.y)

	for i in range(4):
		row = pt.x + rowNum[i]
		col = pt.y + colNum[i]
		# if adjacent cell is valid, has path
		# and not visited yet, enqueue it.
		if (isValid(row,col) and maze[row][col] != "W" and maze[row][col].startswith("A")==False  and not visited[row][col]):

			visited[row][col] = True

			Adjcell = Node(Point(row,col),
								curr.dist+1)

			queue.append(Adjcell)
			move_count=move_count+1

	# if no way to go pass
	if move_count==0:
		Adjcell = Node(Point(pt.x,pt.y),
								curr.dist+1)
		queue.append(Adjcell)
		curr.dist=curr.dist+1 # pass

	back = Point(pt.x,pt.y)
	return (queue,curr.dist,back,visited)


def BFS_Init(maze):
	#node queue and back trace
	queue = [0 for i in range(N)]
	back = [0 for i in range(N)]

	#visited queue for all agents
	agent_visited = [[[False for k in range(COL)] for j in range(ROW)]  for i in range(N)]
	distance=[0 for i in range(N)]

	for agent in range(N):
		if maze[Source[agent].x][Source[agent].y]=="W" or maze[Destination[agent].x][Destination[agent].y]=="W":
			return distance
		agent_visited[agent][Source[agent].x][Source[agent].y] = True

		queue[agent]=deque()
		s = Node(Source[agent],0)
		queue[agent].append(s)
		back[agent]=Point(Source[agent].x,Source[agent].y)



	for row in maze:
		print(row)


	# Do a BFS starting from source cell
	#burdan sonra BFS_Move
	while control_s(queue):
		for a in range(N):
			queue[a],distance[a],back[a],agent_visited[a]=BFS_Move(maze,queue[a],back[a],Destination[a],agent_visited[a],distance[a],a)

	for row in maze:
		print(row)


	return distance

def DFS_Move(maze,stack,back,dest: Point,visited,distance,a):

	if(len(stack)==0):
		return (stack,distance,back,visited)

	curr = stack.pop() # Dequeue the back cell

	pt = curr.pt
	print(pt.x,pt.y,distance)

	maze[back.x][back.y] = "E"
	maze[pt.x][pt.y] = "A"+str(a+1)

	print(a,"->",pt.x,pt.y)
	if pt.x == dest.x and pt.y == dest.y:
		print("Agent Arrived")
		stack.clear()

		return (stack,curr.dist+1,back,visited)
	# Otherwise enqueue its adjacent cells
	move_count=0
	visited=check_neighbors(maze,visited,pt.x,pt.y)

	for i in range(4):
		row = pt.x + rowNum[i]
		col = pt.y + colNum[i]


		if (isValid(row,col) and maze[row][col] != "W" and maze[row][col].startswith("A")==False  and not visited[row][col]):

			visited[row][col] = True

			Adjcell = Node(Point(row,col),
								curr.dist+1)

			stack.append(Adjcell)
			move_count=move_count+1

	if move_count==0:
		Adjcell = Node(Point(pt.x,pt.y),
								curr.dist+1)
		stack.append(Adjcell)
		curr.dist=curr.dist+1 # pass

	back = Point(pt.x,pt.y)
	return (stack,curr.dist,back,visited)


def DFS_Init(maze):

	stack = [0 for i in range(N)]
	back = [0 for i in range(N)]


	agent_visited = [[[False for k in range(COL)] for j in range(ROW)]  for i in range(N)]
	distance=[0 for i in range(N)]

	for agent in range(N):
		if maze[Source[agent].x][Source[agent].y]=="W" or maze[Destination[agent].x][Destination[agent].y]=="W":
			return distance
		agent_visited[agent][Source[agent].x][Source[agent].y] = True

		stack[agent]=deque()
		s = Node(Source[agent],0)
		stack[agent].append(s)
		back[agent]=Point(Source[agent].x,Source[agent].y)

	for row in maze:
		print(row)



	while control_s(stack):
		for a in range(N):
			stack[a],distance[a],back[a],agent_visited[a]=DFS_Move(maze,stack[a],back[a],Destination[a],agent_visited[a],distance[a],a)

	for row in maze:
		print(row)

	return distance


def manhattan_dist (a,b,c,d):

	sum=abs(a-c)+abs(b-d)
	return sum


def Astar_Move(maze,queue,back,dest: Point,visited,distance,a):

	if(queue.isEmpty()):
		return (queue,distance,back,visited)

	curr = queue.delete(dest) # Dequeue with priority

	pt = curr.pt

	maze[back.x][back.y] = "E"
	maze[pt.x][pt.y] = "A"+str(a+1)
	print(a,"->",pt.x,pt.y)
	if pt.x == dest.x and pt.y == dest.y:
		print("Agent Arrived")
		queue.clear()
		return (queue,curr.dist+1,back,visited)
	# Otherwise enqueue its adjacent cells

	visited=check_neighbors(maze,visited,pt.x,pt.y)
	move_count=0
	for i in range(4):
		row = pt.x + rowNum[i]
		col = pt.y + colNum[i]

		if (isValid(row,col) and maze[row][col] != "W" and maze[row][col].startswith("A")==False  and not visited[row][col]):
			visited[row][col] = True

			Adjcell = Node(Point(row,col),
								curr.dist+1)
			queue.insert(Adjcell)

			move_count=move_count+1

	if move_count==0:
		Adjcell = Node(Point(pt.x,pt.y),
								curr.dist+1)
		queue.insert(Adjcell)
		curr.dist=curr.dist+1 # pass

	back = Point(pt.x,pt.y)


	return (queue,curr.dist,back,visited)
def Astar(maze):

	queue = [0 for i in range(N)]
	back = [0 for i in range(N)]
	print(Source[1].x,Source[1].y,Destination[1].x,Destination[1].y)

	agent_visited = [[[False for k in range(COL)] for j in range(ROW)]  for i in range(N)]
	distance=[0 for i in range(N)]
	for agent in range(N):
		if maze[Source[agent].x][Source[agent].y]=="W" or maze[Destination[agent].x][Destination[agent].y]=="W":
			return distance

		agent_visited[agent][Source[agent].x][Source[agent].y] = True

		queue[agent]=PriorityQueue()
		s = Node(Source[agent],0)
		queue[agent].insert(s)
		back[agent]=Point(Source[agent].x,Source[agent].y)


	for row in maze:
		print(row)



	while control(queue):
		for a in range(N):
			queue[a],distance[a],back[a],agent_visited[a]=Astar_Move(maze,queue[a],back[a],Destination[a],agent_visited[a],distance[a],a)

	for row in maze:
		print(row)
	return distance


def Selector(method):

	method_name = {
		"1": BFS_Init,
		"2": DFS_Init,
		"3": Astar,
	}
	ret=method_name[method]

	return ret
def main():

	print('Enter Your Choice:')
	print('1 -> BFS')
	print('2 -> DFS')
	print('3 -> A*')

	x= input()

	global Source,Destination
	global ROW, COL, N



	maze = []
	rowNum=0
	with open(sys.argv[1]) as arr:
		for line in arr:
			if rowNum==0:
				a = []
				for col in line.split('\t'):
					a.append(col.rstrip("\n"))

				ROW=int(a[0])
				COL=int(a[1])
				N=int(a[2])
				Source = [Point(0,0) for i in range(N)]
				Destination = [Point(0,0) for i in range(N)]


				rowNum=rowNum+1
			else:
				row = []
				colNum=0
				for col in line.split('\t'):
					temp=col.rstrip("\n")
					if(temp.startswith("A")):
						Source[int(temp.lstrip("A"))-1] = Point(rowNum-1,colNum)
					if(temp.startswith("G")):
						Destination[int(temp.lstrip("G"))-1] = Point(rowNum-1,colNum)
					row.append(temp)
					colNum=colNum+1
				maze.append(row)
				rowNum=rowNum+1



	if(ROW>=20 or ROW<=3 or COL>=20 or COL<=3 or N>=9 or N<=1):
		print("Constraint Failure")
	else:

		dist=[0 for i in range(N)]
		dist = Selector(x)(maze)
		original_stdout = sys.stdout # Save a reference to the original standard output
		f = open(sys.argv[2], "x")

		with open(sys.argv[2], 'w') as f:
			sys.stdout = f # Change the standard output to the file we created.
			for row in maze:
				print(row)
			sys.stdout = original_stdout
		if dist[0]!=-1:
			print("Shortest Path is",dist[0],dist[1])
		else:
			print("Shortest Path doesn't exist")



main()
