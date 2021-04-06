import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
import pickle

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



# arr.astype(int)
# 0 1 2 3 4 5 0 1 2 3 4   0  1   2  3  4
# 0 1 2 3 4 5 6 7 8 9 10 11  12 13 14  15

""" words + tags + chunk_tags + psp + dep + word + tags +  chunk_tags + psp + dep """
	
row = []
column = []
data = []

Y = []

li = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')
			a4 = line1[3].strip()

			if a3[1] != 'U':
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
					column.append(dependencies.index(a3[1]) + len(words) + len(tags) + len(chunk_tags) + len(psps))
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
					column.append(dependencies.index(a3[1]) + len(words) + len(tags) + len(chunk_tags) + len(psps))
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
				column.append(z + words.index(a2[2]))
				column.append(z + tags.index(a2[5]) + len(words))
				column.append(z + chunk_tags.index(a2[4]) + len(words) + len(tags))
				column.append(z + psps.index(a2[9]) + len(words) + len(tags) + len(chunk_tags))
				column.append(z + dependencies.index(a3[1]) + len(words) + len(tags) + len(chunk_tags) + len(psps))
				data.append(1)
				data.append(1)
				data.append(1)
				data.append(1)
				data.append(1)


				Y.append(a4)


X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+chunk_tags_len+psps_len+dependencies_len)))
clf = LinearSVC()
clf.fit(X, Y)
pickle.dump(clf, open('finalised_model.sav', 'wb'))

