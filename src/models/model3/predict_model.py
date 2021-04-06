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
	if k==0:
		ans=recall_score(Y, z, average='macro')
		print("recall score for averaged as macro : {}".format(ans))
	elif k==1:
		ans=recall_score(Y, z, average='micro')
		print("recall score for averaged as micro : {}".format(ans))
	elif k==2:
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

	elif k==6:
		ans=precision_score(Y,z, average='macro')
		print("precision for average as macro : {}".format(ans))
	elif k==7:
		ans=precision_score(Y,z, average='micro')
		print("precision for average as micro : {}".format(ans))

	elif k==8:
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

words_len = len(data['words'])
tags_len = len(data['tags'])

row = []
column = []
data = []

Y = []


li = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		li += 1
		# print(li)
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')

			if(a1[0] == 'H'):
				row.append(li -1)
				row.append(li -1)
				column.append(words.index(a1[1]))
				column.append(tags.index(a1[4]) + len(words))
				data.append(1)
				data.append(1)

			elif(a1[0] == 'ROOT'):
				row.append(li -1)
				row.append(li -1)
				column.append(words.index('ROOT'))
				column.append(tags.index('ROOT') + len(words))
				data.append(1)
				data.append(1)

			z = len(words) + len(tags)
			row.append(li -1)
			row.append(li -1)
			column.append(z + words.index(a2[2]))
			column.append(z + tags.index(a2[5]) + len(words))
			data.append(1)
			data.append(1)


			Y.append(a3[1])

X = csr_matrix((data, (row, column)) , shape=(li, 2*(words_len+tags_len)))

loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)

for i in range(10):
	answer=metric_analysis(i,Y,z)

# iu = 0
# pu = 0
# il = 0
# pl = 0
# ir = 0
# pr = 0
# cnt = 0
# for i in range(len(Y)):
# 	if(Y[i] == 'L'):
# 		il +=1
# 	if(Y[i] == 'R'):
# 		ir +=1
# 	if(Y[i] == 'U'):
# 		iu +=1		
# 	if(Y[i] != z[i]):
# 		if(Y[i] == 'L'):
# 			pl +=1
# 		if(Y[i] == 'R'):
# 			pr +=1
# 		if(Y[i] == 'U'):
# 			pu +=1
# 		cnt += 1

# print('*****************')
# print(cnt/len(Y))
# print('*****************')
# print(pl/il)
# print('*****************')
# print(pr/ir)
# print('*****************')
# print(pu/iu)

# cnt = 0
# for i in range(len(Y)):
# 	if(Y[i] != z[i]):
# 		cnt += 1

# print(((len(Y)-cnt)/len(Y))*100)