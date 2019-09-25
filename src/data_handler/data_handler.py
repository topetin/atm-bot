import json

def saveAtmData(red, atmId, atmIndex):
    prob = getProbability(atmIndex)
    data = getBanelcoFileData() if red == 'BANELCO' else getLinkFileData()
    atmsIds = data.get(prob)
    atmsIds.append(atmId)
    writeBanelcoFileData(data) if red == 'BANELCO' else writeLinkFileData(data)


def getProbability(atmIndex):
    if atmIndex == 0:
        return '0.7'
    elif atmIndex == 1:
        return '0.2'
    else:
        return '0.1'


def hasAvailableWithdraw(red, atmId):
    data = getBanelcoFileData() if red == 'BANELCO' else getLinkFileData()
    totalProb07 = data.get('0.7').count(atmId)
    totalProb02 = data.get('0.2').count(atmId)
    totalProb01 = data.get('0.1').count(atmId)
    pE = 0.7*totalProb07 + 0.2*totalProb02 + 0.1*totalProb01
    return pE < 1000


def getBanelcoFileData():
    with open('./data/banelco-data.json', 'r') as reader:
        data = json.load(reader)
    return data


def writeBanelcoFileData(data):
    with open('./data/banelco-data.json', 'w', encoding='utf-8') as writer:
        json.dump(data, writer, ensure_ascii=False, indent=4)


def getLinkFileData():
    with open('./data/link-data.json', 'r') as reader:
        data = json.load(reader)
    return data


def writeLinkFileData(data):
    with open('./data/link-data.json', 'w', encoding='utf-8') as writer:
        json.dump(data, writer, ensure_ascii=False, indent=4)
