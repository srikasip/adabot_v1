import json
import os
# from pattern.en import pluralize, singularize

knownTypes = ["integer", "string", "money", "decimal", "datetime"]

def dirCreateCheck(dirName, relativePath=''):
  try:  
    if relativePath == "":
      dirName = dirName
    else:
      dirName = relativePath + "/" + dirName
    
    if not os.path.exists(dirName):
      os.makedirs(dirName)

    return True

  except:
    return False

def getFileText(fileHandle):
  with open(fileHandle, "r") as readFile:
    txt = readFile.read()
  return txt

def getFileJSON(fileHandle):
  with open(fileHandle, "r") as readFile:
    txt = readFile.read()
    obj = json.loads(txt)

  return obj

def writeJSON(fileHandle, jsonObj):
  with open(fileHandle, "w") as writeFile:
    writeFile.write(jsonObj.dumps(self.classes, indent=2))

  return True

def writeText(fileHandle, writeText):
  with open(fileHandle, "w") as writeFile:
    writeFile.write(writeText)
  return True
