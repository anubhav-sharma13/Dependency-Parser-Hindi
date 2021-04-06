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

words_len = len(data['words'])

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
					column.append(words.index(a1[1]))
					data.append(1)

				elif(a1[0] == 'ROOT'):
					row.append(li -1)
					column.append(words.index('ROOT'))
					data.append(1)

				z = len(words)
				row.append(li -1)
				column.append(z + words.index(a2[2]))
				data.append(1)


				Y.append(a4)

X = csr_matrix((data, (row, column)) , shape=(li,2*words_len))

clf = LinearSVC()
clf.fit(X, Y)

pickle.dump(clf, open('finalised_model.sav', 'wb'))