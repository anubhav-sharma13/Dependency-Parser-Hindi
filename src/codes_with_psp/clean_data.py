NULL_index = []

import sys
import re

count = 0
flag = 0

with open(sys.argv[1], 'r') as f:
    for line in f:
        # print(count)
        if (line.rstrip()):
            line = re.sub('\s+',' ',line)
            troot = 0 
            line1 = line.split(' ')
            if (line1[0] == '<Sentence' and (line1[1].split('\'')[1] not in NULL_index)):
                count +=1
                print('<Sentence id=' + '\'' + str(count) + '\'>')
                flag = 1
            elif(line1[0].strip() == '</Sentence>' and flag == 1):
                print(line1[0].strip())
                flag = 0
            elif(flag == 1):
                print(line)
