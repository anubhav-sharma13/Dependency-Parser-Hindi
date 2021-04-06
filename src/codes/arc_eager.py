import sys
import re
import copy
from collections import deque

buffer=[]
line_state=[]
tags=[]
dependencies=[]
line_number=0
sentence_id = 0
stack=[]

not_parasble_sentences = []
not_parasble_sentences_ki = []

def check_orignal_dependencies():
	stack_top = stack[len(stack) - 1]
	buffer_top = buffer[len(buffer) - 1]

	for i in tags:
		if(i[0] == stack_top and i[1] == buffer_top):
			return i[2],i[3]

	return 0,0;		


def check_left_arc():
	stack_top = stack[len(stack) - 1]

	for i in dependencies:
		if(i[2] == stack_top):
			return 0

	return 1	

def check_right_arc():
	buffer_top = buffer[len(buffer) - 1]

	for i in dependencies:
		if(i[2] == buffer_top):
			return 0

	return 1			

def check_reduce():
	stack_top = stack[len(stack) - 1]

	for i in dependencies:
		if(i[2] == stack_top):
			return 1

	return 0

def left_arc(relation):
	stack_top = stack[len(stack) - 1]
	buffer_top = buffer[len(buffer) - 1]

	temp = []
	temp.append(buffer_top)
	temp.append(relation)
	temp.append(stack_top)

	dependencies.append(temp)

	stack.pop()

def right_arc(relation):
	stack_top = stack[len(stack) - 1]
	buffer_top = buffer[len(buffer) - 1]

	temp = []
	temp.append(stack_top)
	temp.append(relation)
	temp.append(buffer_top)

	dependencies.append(temp)

	buffer.pop()
	stack.append(buffer_top)

def reduce():
	stack.pop()

def shift():
	buffer_top = buffer[len(buffer) - 1]

	buffer.pop()
	stack.append(buffer_top)

def dependency_link():
	buffer_top = buffer[len(buffer) - 1]
	for i in range(len(stack)-2 , -1 , -1):
		stack_element = stack[i]
		for j in tags:
			if(j[0] == stack_element and j[1] == buffer_top):
				return 1

	return 0			




def is_parsable():
	while(not(len(stack) == 1 and len(buffer) == 1)):

		# print(stack[len(stack) - 1],end=' ')
		# if(len(buffer) > 0):
			# print(buffer[len(buffer) - 1])
		
		if(len(buffer) > 1 and len(stack) > 0):
			orignal_dependency,relation = check_orignal_dependencies()

			if(orignal_dependency == 0):

				if(len(stack) > 1):
					can_reduce = dependency_link()
					if(can_reduce == 1):
						can_reduce2 = check_reduce()
						if(can_reduce2 == 1):
							reduce()
							# print('reduce')
						else:
							return 0	
					else:
						shift()
						# print('shift')
				else:
					shift()
					# print('shift')								


			elif(orignal_dependency == 'L'):
				can_right_arc = check_right_arc()
				if(can_right_arc):
					right_arc(relation)
					# print('right_arc')
				else:
					return 0

			elif(orignal_dependency == 'R'):
				can_left_arc = check_left_arc()
				if(can_left_arc):
					left_arc(relation)
					# print('left_arc')
				else:
					return 0

		elif(len(stack) > 1 and len(buffer) == 1):
			can_reduce = check_reduce()
			if(can_reduce):
				reduce()
				# print('reduce')
			else:
				return 0

	if(stack[0] == 'ROOT' and buffer[0] == 'BLK'):
		return 1
	else:
		return 0															




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


		elif(pattern_head.match(line)):
			line_state = []
			line1 = line.split(';')
			line_state.append(line1[0].split(' ')[5])
			line_state.append(line1[1].split(' ')[6])
			line_state.append(line1[2].split(' ')[1])
			line_state.append(line1[3].split(' ')[1])

			tags.append(line_state)

		elif(pattern_root.match(line)):
			line_state = []
			line1 = line.split(';')
			line_state.append('ROOT')
			line_state.append(line1[1].split(' ')[6])
			line_state.append('L')
			line_state.append('ROOT')

			tags.append(line_state)

		elif(line_number == 8):
			buffer.clear()
			line1=line.strip()
			line2 = line1.split(' ')
			for i in line2:   
				buffer.append(i)
			buffer.reverse()


		elif(pattern_end.match(line)):
			initialiser="ROOT"
			stack.append(initialiser)


			flag = is_parsable()

			if(flag == 1):
				# print('parsable')
				a = 1
			else:
				# print('Not parsable')
				not_parasble_sentences.append(sentence_id)
				count+=1


			# print(dependencies)	

			flagki = 0	
			tags.clear()
			stack.clear()	
			buffer.clear()
			dependencies.clear()	

# print(count)
print(not_parasble_sentences)
# print(len(not_parasble_sentences))
        	

