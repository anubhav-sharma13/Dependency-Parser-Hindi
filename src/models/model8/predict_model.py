import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
import pickle
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


def metric_analysis(k,Y,z):
	ans=0
	if k==1110:
		ans=recall_score(Y, z, average='macro')
		print("recall score for averaged as macro : {}".format(ans))
	elif k==1:
		ans=recall_score(Y, z, average='micro')
		print("recall score for averaged as micro : {}".format(ans))
	elif k==200:
		ans=recall_score(Y, z, average='weighted')
		print("recall score for averaged as weighted : {}".format(ans))

	elif k==3:
		ans=f1_score(Y,z, average='macro')
		print("f1_score for average as macro : {}".format(ans))
	elif k==4:
		ans=f1_score(Y,z, average='micro')
		print("f1_score for average as micro : {}".format(ans))
	elif k==5:
		ans=f1_score(Y,z, average='weighted')
		print("f1_score for average as weighted : {}".format(ans))

	elif k==600:
		ans=precision_score(Y,z, average='macro')
		print("precision for average as macro : {}".format(ans))
	elif k==7:
		ans=precision_score(Y,z, average='micro')
		print("precision for average as micro : {}".format(ans))

	elif k==800:
		ans=precision_score(Y,z, average='weighted')
		print("precision for average as weighted : {}".format(ans))

	elif k==9:
		ans=confusion_matrix(Y,z)
		print("Confusion matrix is ")
		print(ans)

	return ans

with open('data_lists.json','r') as f:
	data = json.load(f)

words = data['words']
tags = data['tags']
psps = data['psp']

words_len = len(data['words'])
tags_len = len(data['tags'])
psps_len = len(data['psp'])

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
			arr = np.zeros((2*(words_len+tags_len+psps_len)))

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
					column.append(words.index(a1[1]))
					column.append(tags.index(a1[4]) + len(words))
					column.append(psps.index(a1[8]) + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				elif(a1[0] == 'ROOT'):
					row.append(li -1)
					row.append(li -1)
					row.append(li -1)
					column.append(words.index('ROOT'))
					column.append(tags.index('ROOT') + len(words))
					column.append(psps.index('NULL') + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				z = len(words) + len(tags) + len(psps)
				row.append(li -1)
				row.append(li -1)
				row.append(li -1)
				column.append(z + words.index(a2[2]))
				column.append(z + tags.index(a2[5]) + len(words))
				column.append(z + psps.index(a2[9]) + len(words) + len(tags))
				data.append(1)
				data.append(1)
				data.append(1)


				Y.append(a4)

X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+psps_len)))


loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)

for i in range(10):
	answer=metric_analysis(i,Y,z)

# print(len(Y))

# cnt = 0
# for i in range(len(Y)):
# 	if(Y[i] != z[i]):
# 		cnt += 1

# print(cnt)		

# cnt = 0
# for i in range(len(Y)):
# 	if(Y[i] != z[i]):
# 		cnt += 1

# print(((len(Y)-cnt)/len(Y))*100)