import Ada_Utilities as au 
from sqlalchemy.orm import sessionmaker, session

class ControllerObj:
  def __init__(self, classDict, datamodel):
    self.controllerName = classDict["name"]
    self.controllerDict = classDict
    self.datamodel = datamodel

  def writeController(self):
    #WriteController is the brain. 
    #It should create the overall object properties (things like session, etc)
    importText = self.importStatements()
    #It should create the basic class object as well
    initializer = self.getClassDefinition()
    #finally, it should write for the following methods: 
    #     1. Select all
    selectAllTxt = self.getSelectAll()
    #     2. Search for a few

    #     3. Get only 1 -- by id
    selectOne = self.getSelectByID()
  
    #     5. Insert 1
    insertOne = self.getInsertById()
    #     6. Batch Insert
    
    #     7. Update 1
    editOne = self.getEditById()
    #     8. Batch update a set
    
    #     9. Delete by ID
    deleteOneText = self.getDeleteById()
    
    #     10. Delete a set.

    allText = importText + initializer + selectAllTxt + selectOne + deleteOneText + insertOne + editOne

    return allText


  def importStatements(self):
    writeImportStatements = "import Ada_Utilities as au\n"
    writeImportStatements += "from sqlalchemy.orm import sessionmaker, session\n"
    writeImportStatements += "from Classes.ObjectsFile import " + ", ".join(list(self.datamodel.keys()))
    writeImportStatements += ", ENGINE, BASE, APPNAME\n"

    return writeImportStatements

  def getClassDefinition(self):
    classDefinition = "class " + self.controllerName + "Controller:\n"
    classDefinition += "\tdef __init__(self):\n"
    classDefinition += "\t\tSession = sessionmaker(bind=ENGINE)\n"
    classDefinition += "\t\tself.session = Session()\n"

    return classDefinition

  def getSelectAll(self):
    selectAll = "\tdef selectAll(self):\n"
    selectAll += "\t\tall"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").all()\n"
    selectAll += "\t\treturn all" + self.controllerDict["name"] + "\n"

    return selectAll


  def getSelectByID(self):
    returnStr = "\tdef selectbyID(self, send_id):\n"
    returnStr += "\t\tone"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").filter("+self.controllerDict["name"]+".ada_id == send_id).one()\n"
    returnStr += "\t\treturn one" + self.controllerDict["name"] + "\n"

    return returnStr

  def getDeleteById(self):
    returnStr ="\tdef deletebyID(self, send_id):\n"
    returnStr +="\t\ttry:\n"
    returnStr +="\t\t\tone"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").filter("+self.controllerDict["name"]+".ada_id == send_id).delete()\n"
    returnStr +="\t\t\tself.session.commit()\n"
    returnStr +="\t\t\treturn True\n"
    returnStr +="\t\texcept:\n"
    returnStr +="\t\t\treturn False\n"

    return returnStr

  def getEditById(self):
    returnStr = "\tdef editOne(self, params):\n"
    returnStr += "\t\tone"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").filter("+self.controllerDict["name"]+".ada_id == params['ada_id'])\n"
    #returnStr += "\t\tone"+self.controllerDict["name"]+".update({'name': params["name"], "color": params["color"]})\n"
    returnStr += "\t\tone"+self.controllerDict["name"]+".update({"
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnStr += "'"+thisProp["name"]+"': params['"+thisProp["name"]+"'],"


    if returnStr[-1] == ",":
      returnStr = returnStr[0:-1]

    returnStr += "})\n"
    returnStr += "\t\ttry:\n"
    returnStr += "\t\t\tself.session.commit()\n"
    returnStr += "\t\t\treturn True\n"
    returnStr += "\t\texcept:\n"
    returnStr += "\t\t\treturn False\n"

    return returnStr

  def getInsertById(self):
    returnStr = "\tdef insertOne(self, params):\n"
    returnStr += "\t\ttry:\n"
    returnStr += "\t\t\tnew"+self.controllerDict["name"]+" = "+self.controllerDict["name"]+"("
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnStr += "params['"+thisProp["name"]+"'],"


    if returnStr[-1] == ",":
      returnStr = returnStr[0:-1]

    returnStr += ")\n"
    returnStr += "\t\t\tself.session.add(new"+self.controllerDict["name"]+")\n"
    returnStr += "\t\t\tself.session.commit()\n"
    returnStr += "\t\t\treturn True\n"
    returnStr += "\t\texcept:\n"
    returnStr += "\t\t\treturn False\n"

    return returnStr


