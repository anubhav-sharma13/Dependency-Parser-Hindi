import sys
import re
count = 0

dependencies = []
new_dependencies = []

def find_dependencies():
	for t in range(len(dependencies)):

		temp = []


		if (dependencies[t][7] != 'ROOT'):
			for j in range(len(dependencies)):
				if (dependencies[t][7] == dependencies[j][5]):

					if(t < j):
						for k in dependencies[t]:
							temp.append(k)

						temp.append(';')

						for k in dependencies[j]:
							temp.append(k)
					
						temp.append(';')
						
						temp.append('R')
						

					elif(j < t):
						for k in dependencies[j]:
							temp.append(k)
						
						temp.append(';')
						
						for k in dependencies[t]:
							temp.append(k)


						temp.append(';')
					
						
						temp.append('L')						

					temp.append(';')
					temp.append(dependencies[t][6])

					break

		else:
			temp.append('ROOT')
			temp.append(';')
			for k in dependencies[t]:
				temp.append(k)
			temp.append(';')
			temp.append('L')
			temp.append(';')
			temp.append('ROOT')

		new_dependencies.append(temp)

def print_dependencies():
	for t in new_dependencies:
		for j in t:
			print(j + ' ', end = ' ')
			# print('', end = ' ')
		print()

with open(sys.argv[1], 'r') as f:
	for line in f:
		#print(count)
		if (line.rstrip()):
			line = re.sub('\s+', ' ', line)
			line1 = line.split(' ')

			if (line1[0] == '<Sentence'):

				count += 1
				print('<Sentence id=' + '\'' + str(count) + '\'>')

			elif(line1[0].strip() == '</Sentence>'):

				find_dependencies()
				print_dependencies()

				dependencies = []
				new_dependencies = []

				print(line1[0].strip())

			elif(line1[0] == 'H'):

				dependencies.append(line1)

			else :
				print(line)