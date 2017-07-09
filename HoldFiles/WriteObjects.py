import json
import Ada_Utilities as au

class WriteAppObject:
  #This initializes the DataModel for a new app.
  #You can consider this to be the competence of any new class object that is created
  def __init__(self, appName):
    self.appName = appName
    self.knownTypes = ["string", "datetime", "integer", "decimal"]
    self.parseDataModel()

  def parseDataModel(self):
    modelHandle = self.appName + "/writerInstructions/datamodel.json"
    objectLibraryHandle = self.appName + "/Classes"

    dataModel = au.getFileJSON(modelHandle)
    didCreate = au.dirCreateCheck(objectLibraryHandle)

    if didCreate:
      classes = list(dataModel.keys())

      for a_class in classes:
        classCode = ""
        importText = self.makeClassFileImports(dataModel[a_class])
        initText = self.makeClassFileInit(dataModel[a_class])
        getSetText = self.makeClassGetSet(dataModel[a_class])


        classTxt = importText + initText + getSetText
        classHandle = objectLibraryHandle + "/" + a_class  + ".py"

        au.writeText(classHandle, classTxt)
    else:
      print("Did not create...")



  def makeClassGetSet(self, classObj):
    getSets = ""

    for prop in classObj["properties"]:
      propObj = classObj["properties"][prop]
      getSet = "\n\tdef " + propObj["name"] + "(self):\n"
      getSet += "\t\treturn self._" + propObj["name"] + "\n"
      getSet += "\tdef set_" + propObj["name"] + "(self, sentVal):\n"
      getSet += "\t\tself._" + propObj["name"] + " = sentVal\n"

      getSets += getSet

    return getSets


  def makeClassFileInit(self, classObj):
    textObj = "class " + classObj["name"] + ":\n"
    textObj += "\tdef __init__(self):\n"
    for prop in classObj["properties"]:
      propObj = classObj["properties"][prop]
      textObj += "\t\tself._" + propObj["name"] + " = "

      if propObj["data_type"] == "integer":
        textObj += "0\n"
      elif propObj["data_type"] == "string":
        textObj += "''\n"
      elif propObj["data_type"] == "decimal":
        textObj += "0.0f\n"
      elif propObj["data_type"] == "datetime":
        textObj += "datetime.now()\n"
      else:
        textObj += propObj["data_type"]+"()\n"

    return textObj


  def makeClassFileImports(self, classObj):
    #Import Utilities
    importText = "import json\n"
    
    #Import DataBase Stuff
    importText += "from sqlalchemy import *\n"
    importText += "from sqlalchemy.ext.declarative import declarative_base\n"
    importText += "from datetime import datetime\n"

    #Import Relevant Other Classes
    for prop in classObj["properties"]:
      dtype = classObj["properties"][prop]["data_type"]
      if dtype not in self.knownTypes:
        importText += "from " + dtype + " import " + dtype + "\n"
    return importText

