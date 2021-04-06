import sys
import re

heads_name = []
word_data = {}
unknown_dependencies_name = []
tags = []
tags_pair = []
flag = 0

def extract_unknown_dependencies():
	for dependency in tags:
		if(dependency[2] == 'R'):
			head_index = heads_name.index(dependency[1])
			dependent_index = heads_name.index(dependency[0])
			if (head_index - dependent_index) > 3:
				pair1 = [heads_name[dependent_index] , heads_name[head_index - 1]]
				pair2 = [heads_name[dependent_index] , heads_name[dependent_index + 1]]
				cnt = 0
				if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
					unknown_dependencies_name.append(pair1)
					cnt += 1
				if pair2 not in unknown_dependencies_name and pair2 not in tags_pair:
					unknown_dependencies_name.append(pair2)
					cnt += 1

				if(cnt < 2):
					for i in range(dependent_index + 2,head_index - 1):
						pair = [heads_name[dependent_index] , heads_name[i]]
						if pair not in unknown_dependencies_name and pair not in tags_pair:
							unknown_dependencies_name.append(pair)
							cnt += 1
						if(cnt == 2):
							break		

			elif (head_index - dependent_index) > 1:
				pair1 = [heads_name[dependent_index],heads_name[dependent_index + 1]]
				if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
					unknown_dependencies_name.append(pair1)
				elif (head_index - dependent_index) > 2:	
					pair = [heads_name[dependent_index],heads_name[dependent_index + 2]]
					if pair not in unknown_dependencies_name and pair not in tags_pair:
						unknown_dependencies_name.append(pair)

		elif(dependency[2] == 'L'):
			if(dependency[0] != 'ROOT' and dependency[1] != 'BLK'):
				head_index = heads_name.index(dependency[0])
				dependent_index = heads_name.index(dependency[1])
				if (dependent_index - head_index) > 3:
					pair1 = [heads_name[head_index + 1] , heads_name[dependent_index]]
					pair2 = [heads_name[dependent_index - 1] , heads_name[dependent_index]]
					cnt = 0
					if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
						unknown_dependencies_name.append(pair1)
						cnt += 1
					if pair2 not in unknown_dependencies_name and pair2 not in tags_pair:
						unknown_dependencies_name.append(pair2)
						cnt += 1

					if(cnt < 2):
						for i in range(dependent_index - 2,head_index + 1,-1):
							pair = [heads_name[i] , heads_name[dependent_index]]
							if pair not in unknown_dependencies_name and pair not in tags_pair:
								unknown_dependencies_name.append(pair)
								cnt += 1
							if(cnt == 2):
								break

				elif (head_index - dependent_index) > 1:
					pair1 = [heads_name[dependent_index - 1] , heads_name[dependent_index]]
					if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
						unknown_dependencies_name.append(pair1)
					elif (head_index - dependent_index) > 2:
						pair = [heads_name[dependent_index-2] , heads_name[dependent_index]]
						if pair not in unknown_dependencies_name and pair not in tags_pair:
							unknown_dependencies_name.append(pair)

			else:
				# for BLK and ROOT(for ex. 'vgf')
				dependent_index = heads_name.index(dependency[1])
				cnt = 0
				for i in range(dependent_index-1 , -1 , -1):
					pair = [heads_name[i], heads_name[dependent_index]]
					if(pair not in unknown_dependencies_name and pair not in tags_pair):
						unknown_dependencies_name.append(pair)
						cnt += 1
					if(cnt == 2):
						break
				cnt = 0
				for i in range(0 , dependent_index-1):
					pair = [heads_name[i], heads_name[dependent_index]]
					if(pair not in unknown_dependencies_name and pair not in tags_pair):
						unknown_dependencies_name.append(pair)
						cnt += 1
					if(cnt == 2):
						break

				# for ROOT 
				if(dependency[0] != 'ROOT'):
					dependent_index = heads_name.index(dependency[1])
					cnt = 0
					for i in range(dependent_index-1 , -1 , -1):
						pair = ['ROOT',heads_name[i]]
						if(pair not in unknown_dependencies_name and pair not in tags_pair):
							unknown_dependencies_name.append(pair)
							cnt += 1
						if(cnt == 2):
							break
					cnt = 0
					for i in range(0 , dependent_index-1):
						pair = ['ROOT',heads_name[i]]
						if(pair not in unknown_dependencies_name and pair not in tags_pair):
							unknown_dependencies_name.append(pair)
							cnt += 1
						if(cnt == 2):
							break 

def print_unknown_dependencies():
	for dependency in unknown_dependencies_name:
		print(word_data[dependency[0]].strip(),end = ' ')
		print(' ; ',end = ' ')
		print(word_data[dependency[1]].strip(),end = ' ')
		print(' ; ',end = ' ')
		print('U ; ',end = ' ')
		print('NULL')


line_number = 0
with open(sys.argv[1], 'r') as f:
	count = 0
	for line in f:
		line_number += 1
		line = re.sub('\s+',' ',line)

		pattern_start=re.compile("<S+")
		pattern_end=re.compile("</S+")
		pattern_head=re.compile("H+")
		pattern_root=re.compile("ROOT+")

		if(pattern_start.match(line)):
			line_number = 0
			sentence_id = line.split('\'')[1]
			# print(sentence_id)


		elif(pattern_end.match(line)):
			extract_unknown_dependencies()
			print_unknown_dependencies()
			# print('<end>')
			heads_name.clear()
			word_data.clear()
			unknown_dependencies_name.clear()
			tags.clear()
			tags_pair.clear()

		elif(line_number == 8):
			heads_name.clear()
			line1=line.strip()
			line2 = line1.split(' ')
			for i in line2:   
				heads_name.append(i)

		elif(pattern_head.match(line)):
			print(line)
			line_state = []
			line_state_pairs = []
			line1 = line.split(';')
			line_state.append(line1[0].split(' ')[5])
			line_state_pairs.append(line1[0].split(' ')[5])
			line_state.append(line1[1].split(' ')[6])
			line_state_pairs.append(line1[1].split(' ')[6])
			line_state.append(line1[2].split(' ')[1])

			tags.append(line_state)
			tags_pair.append(line_state_pairs)

			if(line_state[0] not in word_data):
				word_data[line_state[0]] = line1[0]
			if(line_state[1] not in word_data):
				word_data[line_state[1]] = line1[1]	

		elif(pattern_root.match(line)):
			print(line)
			line_state = []
			line_state_pairs = []
			line1 = line.split(';')
			line_state.append('ROOT')
			line_state_pairs.append('ROOT')
			line_state.append(line1[1].split(' ')[6])
			line_state_pairs.append(line1[1].split(' ')[6])
			line_state.append('L')

			tags.append(line_state)
			tags_pair.append(line_state_pairs)

			if(line_state[0] not in word_data):
				word_data[line_state[0]] = line1[0]	
			if(line_state[1] not in word_data):
				word_data[line_state[1]] = line1[1]	
