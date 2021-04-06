import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
import pickle

heads_name = []
word_data = {}	
known_dep = []
known_dep_pair = []
unknown_dep_pair = []
id1 = []
id2 = []
id3 = []
id4 = []

def get_unknown():
	for i in range(len(heads_name)):
		for j in range(i+1,len(heads_name)):
			pair = [heads_name[i],heads_name[j]]
			if(pair not in known_dep_pair):
				unknown_dep_pair.append(pair)

	for i in range(len(heads_name)):
		pair = ['ROOT',heads_name[i]]
		if(pair not in known_dep_pair):
			unknown_dep_pair.append(pair)			

							

def predict_L_R():

	with open('data_lists.json','r') as f:
		data = json.load(f)

	words = data['words']
	tags = data['tags']
	chunk_tags = data['chunk_tags']	
	psps = data['psp']

	words_len = len(data['words'])
	tags_len = len(data['tags'])
	chunk_tags_len = len(data['chunk_tags'])
	psps_len = len(data['psp'])

	row = []
	column = []
	data = []

	Y = []

	# arr.astype(int)
	# 0 1 2 3 4 5 0 1 2 3 4   0  1   2  3  4
	# 0 1 2 3 4 5 6 7 8 9 10 11  12 13 14  15

	""" words + tags + chunk_tags + psp + word + tags +  chunk_tags + psp """

	li = 0

	dep_pair = known_dep_pair + unknown_dep_pair

	for pairs in dep_pair:
		li += 1
		# print(li)

		a1 = word_data[pairs[0]].split(' ')
		a2 = word_data[pairs[1]].split(' ')

		if(a1[0] == 'H'):
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			column.append(words.index(a1[1]))
			column.append(tags.index(a1[4]) + len(words))
			column.append(chunk_tags.index(a1[3]) + len(words) + len(tags))
			column.append(psps.index(a1[8]) + len(words) + len(tags) + len(chunk_tags))
			# print(a1[1] , a1[4] ,a1[3] ,a1[8])
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)

		elif(a1[0] == 'ROOT'):
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			column.append(words.index('ROOT'))
			column.append(tags.index('ROOT') + len(words))
			column.append(chunk_tags.index('ROOT') + len(words) + len(tags))
			column.append(psps.index('NULL') + len(words) + len(tags) + len(chunk_tags))
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)

		z = len(words) + len(tags) + len(chunk_tags) + len(psps)
		row.append(li -1)
		row.append(li -1)
		row.append(li -1)
		row.append(li -1)
		column.append(z + words.index(a2[1]))
		column.append(z + tags.index(a2[4]) + len(words))
		column.append(z + chunk_tags.index(a2[3]) + len(words) + len(tags))
		column.append(z + psps.index(a2[8]) + len(words) + len(tags) + len(chunk_tags))
		# print(a2[1] , a2[4] ,a2[3] ,a2[8])
		data.append(1)
		data.append(1)
		data.append(1)
		data.append(1)

	X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+chunk_tags_len+psps_len)))


	loaded_model = pickle.load(open('model_L_R.sav', 'rb'))
	z = loaded_model.predict(X)

	return(z)


def predict_k1_k2():
	with open('data_lists.json','r') as f:
		data = json.load(f)

	words = data['words']
	tags = data['tags']
	chunk_tags = data['chunk_tags']	
	psps = data['psp']
	dependencies = ['L','R']

	words_len = len(data['words'])
	tags_len = len(data['tags'])
	chunk_tags_len = len(data['chunk_tags'])
	psps_len = len(data['psp'])
	dependencies_len = len(dependencies)

	row = []
	column = []
	data = []

	Y = []

	# arr.astype(int)
	# 0 1 2 3 4 5 0 1 2 3 4   0  1   2  3  4
	# 0 1 2 3 4 5 6 7 8 9 10 11  12 13 14  15

	""" words + tags + chunk_tags + psp + dep + word + tags +  chunk_tags + psp + dep """


	li = 0
	for pairs in known_dep:
		# print(li)

		a1 = word_data[pairs[0]].split(' ')
		a2 = word_data[pairs[1]].split(' ')
		a3 = pairs[2]

		li += 1
		# print(li)

		if(a1[0] == 'H'):
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			column.append(words.index(a1[1]))
			column.append(tags.index(a1[4]) + len(words))
			column.append(chunk_tags.index(a1[3]) + len(words) + len(tags))
			column.append(psps.index(a1[8]) + len(words) + len(tags) + len(chunk_tags))
			column.append(dependencies.index(a3) + len(words) + len(tags) + len(chunk_tags) + len(psps))
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)

		elif(a1[0] == 'ROOT'):
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			row.append(li -1)
			column.append(words.index('ROOT'))
			column.append(tags.index('ROOT') + len(words))
			column.append(chunk_tags.index('ROOT') + len(words) + len(tags))
			column.append(psps.index('NULL') + len(words) + len(tags) + len(chunk_tags))
			column.append(dependencies.index(a3) + len(words) + len(tags) + len(chunk_tags) + len(psps))
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)
			data.append(1)

		z = len(words) + len(tags) + len(chunk_tags) + len(psps) + len(dependencies)
		row.append(li -1)
		row.append(li -1)
		row.append(li -1)
		row.append(li -1)
		row.append(li -1)
		column.append(z + words.index(a2[1]))
		column.append(z + tags.index(a2[4]) + len(words))
		column.append(z + chunk_tags.index(a2[3]) + len(words) + len(tags))
		column.append(z + psps.index(a2[8]) + len(words) + len(tags) + len(chunk_tags))
		column.append(z + dependencies.index(a3) + len(words) + len(tags) + len(chunk_tags) + len(psps))
		data.append(1)
		data.append(1)
		data.append(1)
		data.append(1)
		data.append(1)


	X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+chunk_tags_len+psps_len+dependencies_len)))


	loaded_model = pickle.load(open('model_k1_k2.sav', 'rb'))
	z = loaded_model.predict(X)
	return(z)

def predict_dependencies():
	get_unknown()
	z = predict_L_R()

	flag = 0
	for i in range(len(z)):
		if(i<len(known_dep)):
			if(known_dep[i][2] != z[i]):
				flag = 1
				break
		else:
			if(z[i] != 'U'):
				flag = 1
				break

	if(flag == 0):
		id2.append(id1[0])
		z = predict_k1_k2()
		flag1 = 0
		for i in range(len(known_dep)):
			if(z[i] != known_dep[i][3]):
				flag1 = 1
				break

		if(flag1 == 0):
			id3.append(id1[0])

	z = predict_k1_k2()
	flag1 = 0
	for i in range(len(known_dep)):
		if(z[i] != known_dep[i][3]):
			flag1 = 1
			break

	if(flag1 == 0):
		id4.append(id1[0])				





line_number = 0
with open(sys.argv[1], 'r') as f:
	count = 0
	for line in f:
		sentence_idd = 0
		line_number += 1
		line = re.sub('\s+',' ',line)

		pattern_start=re.compile("<S+")
		pattern_end=re.compile("</S+")
		pattern_head=re.compile("H+")
		pattern_root=re.compile("ROOT+")

		if(pattern_start.match(line)):
			line_number = 0
			sentence_id = line.split('\'')[1]
			print(sentence_id)
			id1.append(sentence_id)

		elif(pattern_end.match(line)):
			predict_dependencies()
			
			heads_name.clear()
			id1.clear()
			word_data.clear()
			known_dep.clear()
			known_dep_pair.clear()
			unknown_dep_pair.clear()

		elif(line_number == 8):
			heads_name.clear()
			line1=line.strip()
			line2 = line1.split(' ')
			for i in line2:   
				heads_name.append(i)

		elif(pattern_head.match(line)):
			line_state = []
			line_state_pairs = []
			line1 = line.split(';')
			line_state.append(line1[0].split(' ')[5])
			line_state_pairs.append(line1[0].split(' ')[5])
			line_state.append(line1[1].split(' ')[6])
			line_state_pairs.append(line1[1].split(' ')[6])
			line_state.append(line1[2].split(' ')[1])
			line_state.append(line1[3].split(' ')[1])

			known_dep.append(line_state)
			known_dep_pair.append(line_state_pairs)

			if(line_state[0] not in word_data):
				word_data[line_state[0]] = line1[0].strip()
			if(line_state[1] not in word_data):
				word_data[line_state[1]] = line1[1].strip()	

		elif(pattern_root.match(line)):
			line_state = []
			line_state_pairs = []
			line1 = line.split(';')
			line_state.append('ROOT')
			line_state_pairs.append('ROOT')
			line_state.append(line1[1].split(' ')[6])
			line_state_pairs.append(line1[1].split(' ')[6])
			line_state.append('L')
			line_state.append(line1[3].split(' ')[1])

			known_dep.append(line_state)
			known_dep_pair.append(line_state_pairs)

			if(line_state[0] not in word_data):
				word_data[line_state[0]] = line1[0].strip()	
			if(line_state[1] not in word_data):
				word_data[line_state[1]] = line1[1].strip()

print('**********************')
print(id2)
print(len(id2))
print(id3)
print(len(id3))
print(id4)
print(len(id4))