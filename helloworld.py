compounds = ['undecanal', '1-undecanol', 'dodecanal', 'dodecanol', 'dodecanoic acid']

#settings
columnsToExtract = ['Area', 'Conc']

#global variables
currentSample = ""
samples = {}
areaIndex = 0
concIndex = 0
colExtrIndex = {col: None for col in columnsToExtract} #type: dict[int]
idCount=0

def findStrIndexInArray(array, string):
    for index, el in enumerate(array):
        if string in el:
            return index
    raise ValueError('no such string')

with open("abc.txt") as file:
    lines = file.readlines()
    for line in lines:

        if 'Data File Name' in line:
            columns = line.split('\t') # type: list[str]
            currentSample = columns[-1].rsplit('\\', 1)[1].rstrip('.qgd') .rsplit('_', 1)[0]
            if currentSample not in samples:
                samples[currentSample] = {key: None for key in columnsToExtract}

        if 'IDs' in line:
            idCount = int(line.split('\t')[1])
            continue

        if line.startswith('ID'):
            cols = line.split('\t') #type: list[str]
            for key in colExtrIndex:
               colExtrIndex[key] = findStrIndexInArray(cols, key)

        if idCount>0:
            for id in range(idCount):
                cols = line.split('\t')
                for key in colExtrIndex:
                    # print(key)
                    # print(colExtrIndex[key])
                    # print(samples[currentSample])
                    samples[currentSample][key] = cols[colExtrIndex[key]]
            idCount-=1
            print(idCount)


for key in samples:
    print(key)
    for cols in samples[key]:
        print(cols + str(samples[key][cols]))

print('theEnd')
        # zeilenLager.append(zeile)


