from io import StringIO
import pandas as pd

# Columns to be selected
columnsToSelect = ['Area', 'Conc.']

# Decimal seperators
inDecimalSep = '.'
outDecimalSep = '.'

# Replicate number seperator
# e.g. triplicate measurement of sample1:
# sample1_1, sample1_2, sample1_3
# ==> replSep = '_'
replSep = '_'


# Helper Functions
def getSampleName(singleRunData):
    filePath = singleRunData.split('\n')[0].split('\t')[1]  # type: str
    sampleName = filePath.split('\\')[-1].rsplit('.', 1)[0]

    return sampleName


with open("test.txt") as file:
    lines = file.readlines()

data = []

for line in lines:
    if "Header" in line:
        data.append('')
    elif ("MS Quantitative Results" or "# of IDs") in line:
        pass
    else:
        data[-1] += line

pdData = []
sampleNames = [getSampleName(singleRunData) for singleRunData in data]

for line in data:
    li = (StringIO(line))

    pdData.append(pd.read_csv(li, sep="\t", header=4, decimal=inDecimalSep, index_col=False).set_index('ID#'))

results = pd.concat(pdData, keys=sampleNames)  # type: pd.DataFrame
results.set_index(results.index.set_names(['sample', 'ID#']), inplace=True)


def transposeOnColumn(df, columnName):
    return df.pivot(columns='Name', values=columnName)


selected = [results[['Name', column]] for column in columnsToSelect]
transposed = []


for sel in selected:

    newTable = pd.DataFrame.pivot_table(sel, index='sample', columns=['Name'])
    newTable.index = pd.Categorical(newTable.index, sampleNames)
    newTable.sort_index(inplace=True)
    transposed.append(newTable)

    # TODO: change order of samples from alphabetic to GC data order

for index, el in enumerate(transposed):
    filename = "test" + columnsToSelect[index] + ".txt"
    el.to_csv(filename, sep='\t', decimal=outDecimalSep)


def getSampleNameForDuplicates(sampleName: str, duplicateSeperator: str) -> str:
    return sampleName.rsplit(duplicateSeperator, 1)[0]


def selectDuplicateSamples(df: pd.DataFrame, sampleName: str, duplicateSeperator: str):
    query = lambda datafr: sampleName in datafr.sample
    return df.loc[query]


# concTransposed = transposed[0]
# uniqueSampleNames = set([getSampleNameForDuplicates(name, replSep) for name in [getSampleName(singleRunData) for singleRunData in data]])
# duplicates = []
# for sam in uniqueSampleNames:
#     #selection = concTransposed.index.isin([sam])
#     selection = [getSampleNameForDuplicates(index, replSep) == sam for index in concTransposed.index]
#     duplicates.append(concTransposed[selection])

#duplSelected = selectDuplicateSamples(pd.concat(transposed), [getSampleName(singleRunData) for singleRunData in data][0], '_')


