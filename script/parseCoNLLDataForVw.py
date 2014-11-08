## This script is used to generate training/test files in VW format
## The dep label of each word is represented by (head_word_id)+1+(taghash[dep_tag]<<8)

from sys import argv
import os
import shelve


def load_hash(filename):
	hash = {}
	if not os.path.isfile(filename):
		return hash
	for line in open(filename).readlines():
		hash[line.split()[0]] = int(line.strip().split()[1])
	return hash

def save_hash(hash, filename):
	writer = open(filename,'w')
	for key in hash:
		writer.write(key+" "+str(hash[key])+'\n')
	writer.close()



if __name__ == '__main__':
	if len(argv) != 3:
		print 'parseDepData.py input'
	hasRoot = False
	taghash = load_hash(argv[1].split('_')[0]+".tagMap")
	wordhash = load_hash(argv[1].split('_')[0]+".wordMap")
	if len(taghash)==0:
		taghash['ROOT'] = 1;
	hi = len(taghash)+1
	wi = len(wordhash)+1
	data = open(argv[1]).readlines()
	writer = open(argv[1]+'.vw','w')
	for line in data:
		if line == '\n':
			writer.write('\n')
			continue
		splits = line.replace(":","CON").split()
		tag = splits[-3]
		if tag not in taghash:
			taghash[tag] = hi
			hi+=1
		if tag == 'ROOT':
			hasRoot= True;
		word = splits[1]
		if word not in wordhash:
			wordhash[word] = wi
			wi+=1
		for feature in splits[5].split('|'):
			if feature not in wordhash:
				wordhash[feature] = wi
				wi+=1
		writer.write('%s | w=%s cp=%s fp=%s %s\n'%(int(splits[-4])+1+(taghash[tag]<<8), wordhash[splits[1]], splits[3], splits[4]," ".join(["f="+str(wordhash[x]) for x in splits[5].split('|') ])))
	writer.close()

	save_hash(taghash, argv[1].split('_')[0]+".tagMap")
	save_hash(wordhash, argv[1].split('_')[0]+".wordMap")

	print 'totalNumWord', len(wordhash)
	print 'totalNumTag', len(taghash)
	print 'hasRoot', hasRoot
