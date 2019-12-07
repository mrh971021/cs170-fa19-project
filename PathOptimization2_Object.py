from dijkstra_manager import *
import random

class PathOptimization2:

	def __init__(self, source, Num_of_Vertex, adjacencyDic, dijkstra_manager, dropoff_order, home_order_to_index, list_of_locations):
		self.drop_seq = {}
		# drop_number: a dictionary: each key represents a vertex and the value represents the place the TA live in.
		self.source = source
		self.G = adjacencyDic
		#G = {1:[(2,70),(3,100),(6,50)], 2:....}
		# Grapth: 2D array, each edge defined as a tuple with two entry (vertex,weight)
		self.dijkstra_manager = dijkstra_manager
		# 2D array record the shortest path length between each two vertex (u,v)
		self.dropoff_order = dropoff_order
		# The order of TA drop off
		self.Num_of_Vertex= Num_of_Vertex

		self.home_order_to_index = home_order_to_index

		self.num_home = len(home_order_to_index)

		self.list_of_locations = list_of_locations

		self.path = [source]

		self.num_of_predict = 3


	def Dijkstra(self,u,v):
		return self.dijkstra_manager.dijkstra(u,v)
		# shortest_path, distance

	def AdjacencyMatrix_to_AdjacencyLst(self):
		pass

	def routeToPath(self):
		path = []
		curr = self.source
		while self.route[curr] != curr:
			path.append(curr)
			curr = self.route[curr]

		path.extend(self.Dijkstra(curr, self.source)[0])
		print("route", self.route)
		print("path",path)
		return path

	def getPossibleNeighbor(self,v,n):
		num_home = len(self.home_order_to_index)
		new_num_of_predict = self.num_of_predict

		if num_home - 1 - n < self.num_of_predict:
			new_num_of_predict = num_home - 1 - n

		possible_neighbor = []
		# print(v, "all neighbors: ", self.G.get(v))
		
		for i in range(new_num_of_predict):
			if v == self.home_order_to_index[n+i]: # Currently at nth home, must drop
				return [-1] 	# -1 for must drop
			shortest_path = self.Dijkstra(v, self.home_order_to_index[n+i])[0]
			possible_neighbor.append(shortest_path[1])
			
		if not possible_neighbor:	# No TA on bus
			return [-2]		# -2 for going home

		return possible_neighbor

	def addToDropDic(self, v, n):
		if v in self.drop_seq.keys():
			self.drop_seq[v].append(self.home_order_to_index[n])
		else:
			self.drop_seq[v] = [self.home_order_to_index[n]]

	def sumOfShortestPaths(self,v, n):
		result = 0
		num_home = len(self.home_order_to_index)
		new_num_of_predict = self.num_of_predict
		if num_home - 1 - n < self.num_of_predict:
			new_num_of_predict = num_home - 1 - n

		for i in range(new_num_of_predict):
			result += self.Dijkstra(v,self.home_order_to_index[n+i])[1]

		return result


	def greedy(self,v,n, curr_sum):
		possible_neighbor = self.getPossibleNeighbor(v,n)

		if possible_neighbor[0] == -2:
			self.path.extend(self.Dijkstra(v, self.source)[0][1:])

		elif possible_neighbor[0] == -1:
			self.addToDropDic(v, n)
			self.greedy(v, n+1, curr_sum)

		else:
			# print('possible_neighbor ', possible_neighbor)
			all_possible_sum = [self.sumOfShortestPaths(neighbor, n) \
				for neighbor in possible_neighbor]

			# print(all_possible_sum)
			min_sum = min(all_possible_sum)

			if curr_sum < min_sum:
				self.addToDropDic(v,n)
				self.greedy(v, n+1, curr_sum)

			else:
				next_node = possible_neighbor[all_possible_sum.index(min_sum)]
				self.path.append(next_node)
				self.greedy(next_node, n, min_sum)

		

	def RunPathOptimization(self):
		curr_sum = self.sumOfShortestPaths(self.source, 0)
		self.greedy(self.source, 0, curr_sum)

		print('finished running')
		return self.path, self.drop_seq


