import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *

# import dijkstra_solver
import TSP_solver
from dijkstra_manager import *
# import PathOptimization
# import OutPutGenerator2
# from PathOptimization_Object import *
from PathOptimization2_Object import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """

    dij_manager = dijkstra_manager(adjacency_matrix)
        # Output & Usage: 
        # shortest_path, distance = dij_manager.dijkstra(0,7)
    adjacencyDic = matrixToDic(adjacency_matrix)
    num_of_locations = len(adjacency_matrix)
    starting_index = list_of_locations.index(starting_car_location)
    location_order_index = TSP_solver.main(adjacency_matrix, starting_index, dij_manager)
    dropoff_order = [index for index in location_order_index if list_of_locations[index] in list_of_homes]
    
    # optimal_path_finder = PathOptimization(starting_index, num_of_locations, adjacencyDic, dij_manager, dropoff_order, dropoff_order, list_of_locations)
    # route, drop_seq = optimal_path_finder.RunPathOptimization()
    optimal_path_finder2 = PathOptimization2(starting_index, num_of_locations, adjacencyDic, dij_manager, dropoff_order, dropoff_order, list_of_locations)
    route, drop_seq = optimal_path_finder2.RunPathOptimization()
    #__init__(self, adjacencyDic, dijkstra_manager, dropoff_order):
    # drop_offs = indexToName(drop_seq_index, list_of_locations)
    print(route)
    print(drop_seq)

    return route, drop_seq

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    # print('here')
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    # print(adjacency_matrix)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)

def matrixToDic(adjacency_matrix):
    adjacencyDic = {}
    size = len(adjacency_matrix)
    for i in range(size):
        for j in range(i+1, size):
            entry = adjacency_matrix[i][j]
            if entry != 'x':
                if i in adjacencyDic.keys():
                    adjacencyDic[i].append((j, entry))
                else:
                    adjacencyDic[i] = [(j, entry)]
                if j in adjacencyDic.keys():
                    adjacencyDic[j].append((i, entry))
                else:
                    adjacencyDic[j] = [(i, entry)]

    return adjacencyDic

def indexToName(index_seq_index, list_of_locations):
	name_list = []
	for i in index_seq_index:
		# print("i: ", i)
		# print("len: ", len(list_of_homes))
		name_list.append(list_of_locations[i])

	return name_list

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
