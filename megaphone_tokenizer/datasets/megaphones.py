import os.path
import numpy as np
from .. import tokenizer as tk

def load_data(test_split=0.2, seed=113, **kwargs):
    """Loads megaphone classification dataset.

    # Arguments
        test_split: Fraction of the dataset to be used as test data.
        seed: random seed for sample shuffling.

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """

    if kwargs:
        raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
    
    xs = []
    labels = []
    if os.path.isfile('.\\files\\tokens_number.txt') == False:
        raise Exception('theres no datafile. run generate_data_files_from_train_data_file method first')

    with open('.\\files\\tokens_number.txt', 'r', encoding='utf-8') as tokensFile:
        with open('.\\files\\labels.txt', 'r', encoding='utf-8') as labelFile:
            while True:
                line = tokensFile.readline().replace('\n', '')
                if not line: break
                xs.append(list(line.split(' ')))
            while True:
                line = labelFile.readline().replace('\n', '')
                if not line: break
                labels.append(line)

    xs = np.array(xs)
    labels = np.array(labels)

    np.random.seed(seed)
    indices = np.arange(len(xs))
    np.random.shuffle(indices)
    xs = xs[indices]
    labels = labels[indices]

    idx = int(round(len(xs) * (1 - test_split)))
    x_train, y_train = np.array(xs[:idx]), np.array(labels[:idx])
    x_test, y_test = np.array(xs[idx:]), np.array(labels[idx:])

    return (x_train, y_train), (x_test, y_test)

def generate_data_files_from_train_data_file(filePath=os.path.abspath(os.path.dirname(__file__)) + '\\files\\', trainDataFileName='170906_메가폰지도학습용.csv'):
    voca = set()
    tokensList = []

    with open(filePath + trainDataFileName, 'r', encoding='utf-8') as trainDataFile, open(filePath + 'tokens_text.txt', 'w', encoding='utf-8') as tokensFile, open(filePath + 'labels.txt', 'w') as labelFile:
        while True:
            line = trainDataFile.readline().replace('\n', '')
            if not line: break
            splited = line.split(',')
            msg = splited[0]
            label = splited[1]
            tokens = tk.tokenize_megaphone(msg)
            tokensList.append(tokens)
            for t in tokens:
                m = t[0]+'/'+t[1]
                voca.add(m)
                tokensFile.write(m + ' ')
            tokensFile.write('\n')
            labelFile.write(label + '\n')

    vocaList = list(voca)

    with open(filePath + 'vocabulary.txt', 'w', encoding='utf-8') as vocaFile:
        for v in vocaList:
            vocaFile.write(v + '\n')

    maxLen = 0

    with open(filePath + 'tokens_number.txt', 'w', encoding='utf-8') as numberTokensFile:
        for tr in tokensList:
            maxLen = len(tr) if len(tr) > maxLen else maxLen
            for t in tr:
                idx = vocaList.index(t[0]+'/'+t[1])
                numberTokensFile.write(str(idx) + ' ')
            numberTokensFile.write('\n')

    with open(filePath + 'meta.txt', 'w', encoding='utf-8') as metaFile:
        metaFile.write('number of sentences : ' + str(len(tokensList)) + '\n')
        metaFile.write('number of vocabulary : ' + str(len(vocaList)) + '\n')
        metaFile.write('token number of most longest sentence : ' + str(maxLen) + '\n')