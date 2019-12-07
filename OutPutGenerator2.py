# import utils
import sys


#################Test Parameter##################
Input_file_Header= '1_5'
Vertex_list = ['a1','a2','a3','a4']
route = [1,2,3,3]
#route_seq = [1,2,3,4]
drop_seq = {1: [1,2], 2:[2,3,1], 3:[3]}
s = 0



################Test Parameter###################


Output_file_Name = [Input_file_Header,'.out']
Output_file_Name = ''.join(Output_file_Name)
OutputFile = open(Output_file_Name,'w')

# Print the route of the car
v = s
PrintLine1 = []
route_seq = []
while(route[v]!= v):#this might be wrong!!!!!!!!!!
	route_seq.append(v) # do not have the back route!!!!!
	PrintLine1.append(Vertex_list[v]) # do not have the back route!!!!!
	v = route[v]
route_seq.append(v)
PrintLine1.append(Vertex_list[v])
PrintLine1 = ' '.join(PrintLine1)
print(PrintLine1, file = OutputFile)

# Print the number of location with drop off
Drop_location = drop_seq.keys()
PrintLine2 = len(Drop_location)
print(PrintLine2, file = OutputFile)

#Print all the TA in all dropping location
for i in route_seq:
	#print each location
	if i in drop_seq.keys():
		temp_printline = []
		temp_printline.append(Vertex_list[i])
		for j in drop_seq[i]:
			temp_printline.append(Vertex_list[j])
		temp_printline = ' '.join(temp_printline)
		print(temp_printline, file = OutputFile)

OutputFile.close()


