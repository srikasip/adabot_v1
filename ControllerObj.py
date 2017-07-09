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
    
    #     6. Batch Insert
    
    #     7. Update 1
    
    #     8. Batch update a set
    
    #     9. Delete by ID
    deleteOneText = self.getDeleteById()
    
    #     10. Delete a set.

    allText = importText + initializer + selectAllTxt + selectOne + deleteOneText

    return allText


  def importStatements(self):
    writeImportStatements = "import Ada_Utilities as au\n"
    writeImportStatements += "from sqlalchemy.orm import sessionmaker, session\n"
    writeImportStatements += "from ObjectsFile import " + ", ".join(list(self.datamodel.keys()))
    writeImportStatements += ", ENGINE, BASE, APPNAME\n"

    return writeImportStatements

  def getClassDefinition(self):
    classDefinition = "class " + self.controllerName + "Controller:\n"
    classDefinition += "\tdef __init__(self):\n"
    classDefinition += "\t\tself.session = sessionmaker(bind=ENGINE)\n"

    return classDefinition

  def getSelectAll(self):
    selectAll = "\tdef selectAll(self):\n"
    selectAll += "\t\tall"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").all()\n"
    selectAll += "\t\treturn all" + self.controllerDict["name"] + "\n"

    return selectAll


  def getSelectByID(self):
    returnStr = "\tdef selectbyID(self, send_id):\n"
    returnStr += "\t\tone"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").filter("+self.controllerDict["name"]+".ada_id == send_id)\n"
    returnStr += "\t\treturn one" + self.controllerDict["name"] + "\n"

    return returnStr

  def getDeleteById(self):
    returnStr = "\tdef selectbyID(self, send_id):\n"
    returnStr += "\t\tone"+self.controllerDict["name"]+" = self.session.query("+self.controllerDict["name"]+").filter("+self.controllerDict["name"]+".ada_id == send_id).delete()\n"
    returnStr += "\t\tself.session.commit()\n"

    return returnStr







