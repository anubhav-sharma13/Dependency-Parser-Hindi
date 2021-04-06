import sys
import re
count = 0

head_list = {
    'JJP': ['JJ'],
    'JJP1': ['QF','QC','QO'],
    'VG*': ['VM'],
    'NEGP': ['NEG'],
    'RBP': ['RB'],
    'RBP1': ['NN','WQ'],
    'BLK': ['SYM'],
    'BLK1': ['UNK','RP','INJ'],
    'CCP': ['CC'],
    'CCP1': ['SYM'],
    'NP':['NN','PRP','NNP'],
    'NP1':['QC','QF','QO'],
    'NP2':['NST'],
    'NP3':['WQ']
}

sentence = ''
sentence_pos = ''
sentence_lemma = ''
heads = ''
heads_pos = ''
heads_o_pos = ''
heads_name = ''
heads_lemma = ''

dependencies = []

head = ''
head_name = ''
head_o_pos = ''
head_pos = ''
head_lemma = ''
head_relation = ''
head_relative_name = ''

chunk_words = []
chunk_pos = []
chunk_lemma = []

def find_head_jjp(head_o_pos):
    
    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['JJP']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['JJP1']):
            return i


def find_head_vg(head_o_pos):
    
    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['VG*']):
            return i

def find_head_negp(head_o_pos):

        for i in range(len(chunk_pos)-1 , -1 , -1):
            if(chunk_pos[i] in head_list['NEGP']):
                return i


def find_head_rbp(head_o_pos):

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['RBP']):
            return i    

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['RBP1']):
            return i


def find_head_blk(head_o_pos):

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['BLK']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['BLK1']):
            return i


def find_head_ccp(head_o_pos):

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['CCP']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['CCP1']):
            return i


def find_head_np(head_o_pos):

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['NP']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['NP1']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['NP2']):
            return i

    for i in range(len(chunk_pos)-1 , -1 , -1):
        if(chunk_pos[i] in head_list['NP3']):
            return i


def find_head(head_o_pos):
    if(head_o_pos == 'JJP'):
        return find_head_jjp(head_o_pos)
    if(head_o_pos == 'VGF' or head_o_pos == 'VGNN' or head_o_pos == 'VGNF'):
        return find_head_vg(head_o_pos)
    if(head_o_pos == 'NEGP'):
        return find_head_negp(head_o_pos)
    if(head_o_pos == 'RBP'):
        return find_head_rbp(head_o_pos)
    if(head_o_pos == 'BLK'):
        return find_head_blk(head_o_pos)
    if(head_o_pos == 'CCP'):
        return find_head_ccp(head_o_pos)
    if(head_o_pos == 'NP'):
        return find_head_np(head_o_pos)

with open(sys.argv[1], 'r') as f:
    for line in f:
        # print(count)
        if (line.rstrip()):
            line = re.sub('\s+',' ',line)
            line1 = line.split(' ')

            if (line1[0] == '<Sentence'):

                count +=1
                print('<Sentence id=' + '\'' + str(count) + '\'>')

            elif(line1[0].strip() == '</Sentence>'):

                index = find_head(head_o_pos)
                head = chunk_words[index]
                head_pos = chunk_pos[index]
                head_lemma = chunk_lemma[index]
                
                heads += head + ' '
                heads_pos += head_pos + ' '
                heads_o_pos += head_o_pos + ' '
                heads_name += head_name + ' '
                heads_lemma += head_lemma + ' '

                dependencies.append('H ' + head + ' ' + head_lemma + ' ' +  head_o_pos + ' ' + head_pos + ' ' + head_name + ' ' + head_relation + ' ' +  head_relative_name)

                print(sentence)
                print(sentence_lemma)
                print(sentence_pos)

                print(heads)
                print(heads_lemma)
                print(heads_o_pos)
                print(heads_pos)
                print(heads_name)

                for i in dependencies:
                    print(i)

                chunk_words = []
                chunk_pos = []
                chunk_lemma = []
                sentence = ''
                sentence_pos = ''
                sentence_lemma = ''
                heads = ''
                heads_pos = ''
                heads_o_pos = ''
                heads_name = ''
                heads_lemma = ''
                dependencies = []

                print(line1[0].strip())

            elif(line1[0] == 'H'):

                if(len(chunk_words)):
                    index = find_head(head_o_pos)
                    head = chunk_words[index]
                    head_pos = chunk_pos[index]
                    head_lemma = chunk_lemma[index]

                    heads += head + ' '
                    heads_pos += head_pos + ' '
                    heads_o_pos += head_o_pos + ' '
                    heads_name += head_name + ' '
                    heads_lemma += head_lemma + ' '

                    dependencies.append('H ' + head + ' ' + head_lemma + ' ' +  head_o_pos + ' ' + head_pos + ' ' + head_name + ' ' + head_relation + ' ' +  head_relative_name)

                head_o_pos = line1[1]
                head_name = line1[2]
                head_relation = line1[3]
                head_relative_name = line1[4]

                chunk_words = []
                chunk_pos = []
                chunk_lemma = []

            elif(line1[0] == 'T'):

                chunk_words.append(line1[1])
                chunk_pos.append(line1[2])
                chunk_lemma.append(line1[3])
                sentence += line1[1] + ' '
                sentence_pos += line1[2] + ' '
                sentence_lemma += line1[3] + ' '

                


            