import sys
import re
count = 0
cnt = 0
w = 0
# t = [' VAUX']
# head_tags = ['NP', 'JJP', 'CCP', 'VGNF', 'VGF', 'BLK', 'VGNN', 'RBP', 'FRAGP', 'NEGP']
head_const_tags = ''
head_tag = 0
# tt = []
# tt1 = []
tags = {
    'NP': [],
    'JJP': [],
    'CCP': [],
    'VGNF': [],
    'VGF': [],
    'BLK': [],
    'VGNN': [],
    'RBP': [],
    'FRAGP': [],
    'NEGP': []
}

with open(sys.argv[1], 'r') as f:
    for line in f:
        # print(count)
        if (line.rstrip()):
            line = re.sub('\s+',' ',line)
            troot = 0 
            line1 = line.split(' ')
            if (line1[0] == '<Sentence'):
                count +=1
                print('<Sentence id=' + '\'' + str(count) + '\'>')
            elif(line1[0].strip() == '</Sentence>'):
                print(line1[0].strip())    
            elif(line1[0].strip() == '))'):
                # if head_tag == "VGF" and head_const_tags in t: 
                    # if(str(count) not in tt1):
                        # cnt += 1
                        # tt1.append(str(count))

                if head_const_tags not in tags[str(head_tag)]:
                    tags[str(head_tag)].append(head_const_tags)
                troot = 0
                continue
            elif(line1[1] == '(('):
                head_const_tags = ''
                head_tag = 0
                name = 0
                drel = 0
                relation = 0
                relative = 0 
                if(line1[2].split('_')[0] == 'NULL'):
                    head_tag = line1[2].split('_')[2]
                else:
                    head_tag = line1[2]
                        
                for i in range(4,len(line1)):
                    if(line1[i].split('=')[0] == 'name'):
                        name = line1[i].split('=')[1].split('\'')[1]
                    elif(line1[i].split('=')[0] == 'drel' or line1[i].split('=')[0] == 'dmrel'):
                        drel = 1
                        relation = line1[i].split('=')[1].split('\'')[1].split(':')[0]
                        relative = line1[i].split('=')[1].split('\'')[1].split(':')[1]

                print('H' + ' ' + head_tag + ' ',end = ' ')        

                if(name != 0):
                    print(name + ' ',end=' ')
                else:
                    print('NULL ',end=' ')

                if(drel != 0):
                    print(relation + ' ' + relative)
                else:
                    print('NULL ROOT')
            else:
                troot = line1[1]
                troot_tag = line1[2]
                troot_lemma = line1[4].split('=')[1].split('\'')[1].split(',')[0]
                print('T ' + troot + ' ' + troot_tag + ' ' + troot_lemma)
                head_const_tags = head_const_tags + ' ' + troot_tag

# print(tags['NP'])
# print()
# print()
# print(tags['VGF'])
# print()
# print()
# print(tags['VGNF'])
# print()
# print()
# print(tags['JJP'])
# print()
# print()
# print(tags['CCP'])
# print()
# print()
# print(tags['BLK'])
# print()
# print()
# print(tags['VGNN'])
# print()
# print()
# print(tags['RBP'])
# print()
# print()
# print(tags['FRAGP'])
# print()
# print()
# print(tags['NEGP'])
# print()
# print()
# for i in tags['VGF']:
    # j = i.split(' ')
    # if('VM' in j):
    # if (("NEG" in j)):
    # if(('NN' in j) or ('PRP' in j) or ('NNP' in j) or ('QF' in j) or ('QC' in j) or ('QO' in j) or ('NST' in j) or ('WQ' in j)):
    # if(('NN' in j) or ('PRP' in j) or ('NNP' in j)):
    # if(('JJ' not in j)):
        # continue
    # else:
        # if(('NN' in j) or ('PRP' in j) or ('NNP' in j) or ('NST' in j)):
            # continue
        # if(i not in tt):
            # tt.append(i)

# print(tt)

# print(cnt)

# print(tt1)

# print(len(tt1))

# print(count)

# print(cnt_fragp)

# remove all sentences with possible chunks with head as NP and having NNC or NNPC without NN or NNP or PRP
# remove all sentences with possible chunks with head as NP having JJ without NN or NNP or PRP or NST
# remove all sentences with possible chunks with head as NEGP having no NEG
# remove all sentences with possible chunks with head as FRAGP
# remove all sentences with possible chunks with head as VGF having no VM
# remove all sentences with missing word i.e having pos as NULL__x