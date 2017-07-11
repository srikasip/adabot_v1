import json
import Ada_Utilities as au
from ClassObj import ClassObj as Cobj

class ObjectCreator:
  def __init__(self, appName):
    self.appName = appName
    self.WriteClassFile()

  def WriteClassFile(self):
    txtObjects = ""
    classFile = self.appName + "/Classes/ObjectsFile.py"

    importTxt = self.getImportText()
    baseTxt = self.getBaseText()
    objectText = self.getObjectText()
    fireupText = self.getFireupText()

    txtObjects = importTxt + "\n"
    txtObjects += baseTxt + "\n"
    txtObjects += objectText + "\n"
    txtObjects += fireupText + "\n"

    au.writeText(classFile, txtObjects)

  def getObjectText(self):
    #first lets get the data model
    datamodelHandle = self.appName + "/writerInstructions/datamodel.json"
    self.datamodel = au.getFileJSON(datamodelHandle)

    #next let's create dictionary keyed on class name that holds a working Class
    classesDict = {}
    classes = list(self.datamodel.keys())
    
    for a_class in classes:
      classDict = self.datamodel[a_class]
      newClassObj = self.parseClass(a_class, self.datamodel[a_class], classesDict)
      
      for a_newClass in newClassObj:
        classesDict[a_newClass] = newClassObj[a_newClass]


    classText = ""
    for a_classDict in classesDict:
      tempClass = classesDict[a_classDict]

      classText += tempClass.getClassText()
      classText += "\n"

    return classText

  def parseClass(self, className, sentClass, allClasses):
    newClassObj = Cobj(className)
    propKeys = list(sentClass["properties"].keys())
    classesToSend = {}
    for propKey in propKeys:
      prop = sentClass["properties"][propKey]
      if prop["is_Array"] != True:
        newClassObj.newProperty(prop)
      else:
        if prop["data_type"] in au.knownTypes:
          pivotClass = newClassObj.addKnownArray(prop, sentClass)
          classesToSend[pivotClass.className] = pivotClass
        else:
          if prop["data_type"] not in list(allClasses.keys()):
            moreClasses = self.parseClass(prop["data_type"], self.datamodel[prop["data_type"]], allClasses)
            for a_newClass in moreClasses:
              classesToSend[a_newClass] = moreClasses[a_newClass]

            class2 = classesToSend[prop["data_type"]]
          else:
            class2 = allClasses[prop["data_type"]]

          spawnedClasses = newClassObj.addUnknownArray(prop, sentClass, self.datamodel[prop["data_type"]], class2)
          class2Obj = spawnedClasses["class2"]
          pivotObj = spawnedClasses["pivotTable"]

          classesToSend[class2Obj.className] = class2Obj
          classesToSend[pivotObj.className] = pivotObj


    classesToSend[className] = newClassObj

    return classesToSend

  def getImportText(self):
    importTxt = "from sqlalchemy.ext.declarative import declarative_base\n"
    importTxt += "from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine\n"
    importTxt += "from sqlalchemy.orm import backref, mapper, relation\n"

    return importTxt

  def getBaseText(self):
    baseTxt = "BASE = declarative_base()\n"
    baseTxt += "APPNAME = '"+self.appName+"'\n"

    return baseTxt

  def getFireupText(self):
    fireupText = "ENGINE = create_engine('sqlite:///adaDB_"+self.appName+".db', echo=False)\n"
    fireupText += "BASE.metadata.create_all(ENGINE)\n"
    return fireupText
