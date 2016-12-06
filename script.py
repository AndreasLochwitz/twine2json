# -*- coding: utf-8 -*-
import re
import json

def getTitle(storyContent):
    pattern = re.compile("[^:\ ][A-Za-zäöüßÄÖÜ\d\ .\[\|\]\"\']*")
    result = pattern.search(storyContent)
    return result.group(0)

def getContent(storyContent):
    pattern = re.compile("^[A-Za-z]{2}[A-Za-zäüößÄÖÜ\w\s\.\:]*", re.MULTILINE)
    result = pattern.search(storyContent)
    return result.group(0)

def getLinks(storyContent):
    pattern = re.compile("\[{2}[A-Za-zäöüß\s\d]*\|[A-Za-zäöüßÄÖÜ\s\d]*\]{2}", re.MULTILINE)
    result = pattern.findall(storyContent)
    return result

def getLinkDesc(link):
    pattern = re.compile("[^\[][A-Za-zäüößÄÖÜ\d\ ]*[^\|]")
    result = pattern.search(link)
    return result.group(0)

def getLinkTarget(link):
    pattern = re.compile("\|[A-Za-zäöüßÄÖÜ\s\d]*")
    result = pattern.search(link)
    result = result.group(0)[1:]
    return result

def readFile(fileName):
    f = open(fileName, 'rb')
    fileContent = f.read().decode('utf-8')
    f.close()
    return fileContent

def writeFile(fileName, fileContent):
    f = open(fileName, 'wb')
    f.write(fileContent.encode('utf-8'))
    f.flush()
    f.close()
    
# Datei lesen
storyContent = readFile('story.txt')
pattern = re.compile("::[\ A-Za-zäöüß\d\s.\[\|\]\"\']*")
storyParts = pattern.findall(storyContent)
resultDict = dict()
for i in range(len(storyParts)):
    currentItem = storyParts[i]
    title = getTitle(currentItem)
    content = getContent(currentItem)
    links = getLinks(currentItem)
    linksArray = []
    # Links extrahieren
    for i in range(len(links)):
        currentLink = links[i]
        linkDesc = getLinkDesc(links[i])
        linkTarget = getLinkTarget(links[i])
        linksArray.append({'desc':linkDesc, 'target': linkTarget})
    resultDict[title] = {'content': content, 'links': linksArray}
jsonData = json.dumps(resultDict, sort_keys=True, indent=4, ensure_ascii=False)
writeFile('story.json', jsonData)
