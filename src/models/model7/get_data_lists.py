import sys
import re
import json

words = []
root = []
tags = []
chunk_tags = []
psp = []

li = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		li += 1
		print(li)
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')

			if(a1[0] == 'H'):
				if a1[1] not in words:
					words.append(a1[1])
				if a1[2] not in root:
					root.append(a1[2])
				if a1[3] not in chunk_tags:
					chunk_tags.append(a1[3])
				if a1[4] not in tags:
					tags.append(a1[4])
				if a1[8] not in psp:
					psp.append(a1[8])	

			
			if a2[2] not in words:
				words.append(a2[2])
			if a2[3] not in root:
				root.append(a2[3])
			if a2[4] not in chunk_tags:
				chunk_tags.append(a2[4])
			if a2[5] not in tags:
				tags.append(a2[5])	
			if a2[9] not in psp:
				psp.append(a2[9])	


# print(len(words))					
# print(len(root))					
# print(len(tags))					
# print(len(chunk_tags))
# print(len(psp))
# print(psp)

words.append('ROOT')
root.append('ROOT')
tags.append('ROOT')
chunk_tags.append('ROOT')

data = {}
data['words'] = words
data['root'] = root
data['tags'] = tags
data['chunk_tags'] = chunk_tags
data['psp'] = psp

with open('data_lists.json','w') as f:
	json.dump(data,f)