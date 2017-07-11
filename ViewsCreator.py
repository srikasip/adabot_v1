import Ada_Utilities as au 
from sqlalchemy.orm import sessionmaker, session

class ViewerObj:
  def __init__(self, classDict, datamodel):
    self.controllerName = classDict["name"]
    self.controllerDict = classDict
    self.datamodel = datamodel

  def writeViewer(self):
    #WriteController is the brain. 
    #It should create the overall object properties (things like session, etc)
    
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
    insertLoad = self.getLoadInsert()
    #     6. Batch Insert
    
    #     7. Update 1
    editOne = self.getEditById()
    editLoad = self.getLoadEdit()
    #     8. Batch update a set
    
    #     9. Delete by ID
    deleteOneText = self.getDeleteById()
    
    #     10. Delete a set.



    allText =  initializer + selectAllTxt + selectOne + deleteOneText + insertOne + editOne + editLoad + insertLoad

    return allText


  def importStatements(self):
    writeImportStatements = "import Ada_Utilities as au\n"
    writeImportStatements += "from sqlalchemy.orm import sessionmaker, session\n"
    writeImportStatements += "from Classes.ObjectsFile import " + ", ".join(list(self.datamodel.keys()))
    writeImportStatements += ", ENGINE, BASE, APPNAME\n"

    return writeImportStatements

  def getClassDefinition(self):
    classDefinition = "\n\nclass " + self.controllerName + "Viewer:\n"
    classDefinition += "\tdef __init__(self):\n"
    classDefinition += "\t\tpass\n\n"

    return classDefinition

  def getSelectAll(self):
    returnVal = "\tdef viewAll(self):\n"
    returnVal += "\t\ta_" + self.controllerName + "Controller = " + self.controllerName + "Controller()\n"
    returnVal += "\t\tall" + self.controllerName + " = a_" + self.controllerName + "Controller.selectAll()\n"
    returnVal += "\t\thtmlSnippet = \"<table>\\n\"\n"
    returnVal += "\t\thtmlSnippet += \"\\t<tr>\\n\"\n"
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += \"\\t\\t<th>"+thisProp["name"]+"</th>\\n\"\n"

    returnVal += "\t\thtmlSnippet += \"\\t\\t<th>Next</th>\\n\"\n"
    returnVal += "\t\thtmlSnippet += \"\\t</tr>\\n\"\n"
    returnVal += "\t\tfor a_" + self.controllerName + " in all" + self.controllerName + ":\n"
    returnVal += "\t\t\thtmlSnippet += \"\\t<tr>\\n\"\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        if thisProp["data_type"] == "string":
          returnVal += "\t\t\thtmlSnippet += \"\\t\\t<td>\"+a_" + self.controllerName + "."+thisProp["name"]+"+\"</td>\\n\"\n"
        else:
          returnVal += "\t\t\thtmlSnippet += \"\\t\\t<td>\"+str(a_" + self.controllerName + "."+thisProp["name"]+")+\"</td>\\n\"\n"

    returnVal += "\t\t\thtmlSnippet += \"\\t\\t<td><a href='/" + self.controllerName + "?call=view&val=\"+str(a_" + self.controllerName + ".ada_id)+\"'>View</a>\"\n"
    returnVal += "\t\t\thtmlSnippet += \"<a href='/" + self.controllerName + "?call=edit&val=\"+str(a_" + self.controllerName + ".ada_id)+\"'>Edit</a>\"\n"
    returnVal += "\t\t\thtmlSnippet += \"<a href='/" + self.controllerName + "?call=delete&val=\"+str(a_" + self.controllerName + ".ada_id)+\"'>Delete</a></td>\\n\"\n"
    returnVal += "\t\t\thtmlSnippet += \"\\t</tr>\\n\"\n"
    returnVal += "\t\thtmlSnippet += \"</table>\\n\"\n"
    returnVal += "\t\thtmlSnippet += \"<a href='/" + self.controllerName + "?call=insert'>Create New " + self.controllerName + "</a></td>\\n\"\n"
    returnVal += "\t\treturn htmlSnippet\n"

    return returnVal


  def getSelectByID(self):
    returnStr = "\tdef viewOneForm(self, sentIDValue):\n"
    returnStr += "\t\ta_"+self.controllerDict["name"]+"Controller = "+self.controllerDict["name"]+"Controller()\n"
    returnStr += "\t\treturn"+self.controllerDict["name"]+" = a_"+self.controllerDict["name"]+"Controller.selectbyID(sentIDValue)\n"
    returnStr += "\t\thtmlSnippet = \"\"\n"
    returnStr += "\t\thtmlSnippet += '<div id=\"div_"+self.controllerDict["name"]+"Form\">\\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnStr += "\t\thtmlSnippet += '\\t<label class=\"form_label\" for=\"lbl_"+thisProp["name"]+"\">"+thisProp["name"]+":</label>\\n'\n"
        returnStr += "\t\thtmlSnippet += '\\t<label class=\"data_label\" id=\"lbl_"+thisProp["name"]+"\" data-param=\""+thisProp["name"]+"\">'+return"+self.controllerDict["name"]+"."+thisProp["name"]+"+'</label>\\n'\n"
        returnStr += "\t\thtmlSnippet += '\\n'\n"


    returnStr += "\t\thtmlSnippet += \"<a href='/"+self.controllerDict["name"]+"?call=edit&val=\"+str(return"+self.controllerDict["name"]+".ada_id)+\"'>Edit</a>\"\n"
    returnStr += "\t\thtmlSnippet += \"<a href='/"+self.controllerDict["name"]+"'>Go Back</a>\"\n"
    returnStr += "\t\thtmlSnippet += '\\n'\n"
    returnStr += "\t\thtmlSnippet += '</div>\\n'\n"
    returnStr += "\t\treturn htmlSnippet\n"

    return returnStr

  def getDeleteById(self):
    returnStr = "\tdef deleteOne(self, sentIDValue):\n"
    returnStr += "\t\ta_"+self.controllerDict["name"]+"Controller = "+self.controllerDict["name"]+"Controller()\n"
    returnStr += "\t\treturnVal = a_"+self.controllerDict["name"]+"Controller.deletebyID(sentIDValue)\n"
    returnStr += "\t\tif returnVal:\n"
    returnStr += "\t\t\thtmlSnippet = 'Successful Deletion'\n"
    returnStr += "\t\telse:\n"
    returnStr += "\t\t\thtmlSnippet = 'Unsuccessful Deletion'\n"
    returnStr += "\t\treturn htmlSnippet, returnVal\n"

    return returnStr

  def getLoadEdit(self):
    returnVal = "\tdef editOneLoad(self, params):\n"
    returnVal += "\t\ta_"+self.controllerDict["name"]+"Controller = "+self.controllerDict["name"]+"Controller()\n"
    returnVal += "\t\treturnVal = a_"+self.controllerDict["name"]+"Controller.editOne(params[\"values\"])\n"
    returnVal += "\t\tif returnVal:\n"
    returnVal += "\t\t  sendData = \"Successful Insertion\"\n"
    returnVal += "\t\telse:\n"
    returnVal += "\t\t  sendData = \"Unsuccessful Insertion\"\n"
    returnVal += "\t\treturn sendData\n"
    return returnVal

  def getLoadInsert(self):
    returnVal = "\tdef insertOneLoad(self, params):\n"
    returnVal += "\t\ta_"+self.controllerDict["name"]+"Controller = "+self.controllerDict["name"]+"Controller()\n"
    returnVal += "\t\treturnVal = a_"+self.controllerDict["name"]+"Controller.insertOne(params[\"values\"])\n"
    returnVal += "\t\tif returnVal:\n"
    returnVal += "\t\t  sendData = \"Successful Insertion\"\n"
    returnVal += "\t\telse:\n"
    returnVal += "\t\t  sendData = \"Unsuccessful Insertion\"\n"
    returnVal += "\t\treturn sendData\n"
    return returnVal

  def getEditById(self):
    returnVal = "\tdef editOneForm(self, sentIDValue):\n"
    returnVal += "\t\ta_"+self.controllerDict["name"]+"Controller = "+self.controllerDict["name"]+"Controller()\n"
    returnVal += "\t\treturn"+self.controllerDict["name"]+" = a_"+self.controllerDict["name"]+"Controller.selectbyID(sentIDValue)\n"
    returnVal += "\t\thtmlSnippet = \"\"\n"
    returnVal += "\t\thtmlSnippet += '<div id=\"div_"+self.controllerDict["name"]+"Form\">\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t<label class=\"form_label\" for=\"txt_"+thisProp["name"]+"\">"+thisProp["name"]+":</label>\\n'\n"
        returnVal += "\t\thtmlSnippet += '\\t<input type=\"text\" class=\"form_text\" id=\"txt_"+thisProp["name"]+"\" data-param=\""+thisProp["name"]+"\" value=\"'+return"+self.controllerDict["name"]+"."+thisProp["name"]+"+'\" />\\n'\n"
        returnVal += "\t\thtmlSnippet += '\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\t<button id=\"btn_submit"+self.controllerDict["name"]+"\" class=\"submitButton\">Submit</button>\\n'\n"
    returnVal += "\t\thtmlSnippet += \"<a href='/"+self.controllerDict["name"]+"'>Cancel</a>\"\n"
    returnVal += "\t\thtmlSnippet += '\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t<script>\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t$(document).ready(function(){\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t$(\"#btn_submit"+self.controllerDict["name"]+"\").click(function(){\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\tvar "+thisProp["name"]+"Val = $(\"#txt_"+thisProp["name"]+"\").val();\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\tif("
    
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += thisProp["name"]+"Val != \"\" && "

    
    returnVal = returnVal[:-3]

    returnVal += ")\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t{\\n'\n"


    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t$.ajax({\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\tmethod: \"POST\",\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\turl: \""+self.controllerDict["name"]+"\",\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\tdata: {\\n'\n"
    

    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\t\"values\": { "
    
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\""+thisProp["name"]+"\": "+thisProp["name"]+"Val," 

    returnVal += "\"ada_id\": '+str(return"+self.controllerDict["name"]+".ada_id)+'},\\n'\n"


    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\t\"call\" : \"edit\"\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t})\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t.done(function(msg) {\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\tif(msg == \"Successful Insertion\")\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t{\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\twindow.location.replace(\"/"+self.controllerDict["name"]+"\");\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\telse\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t{\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\talert(\"Insertion Failed\");\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t$(\"#txt_"+thisProp["name"]+"\").val(\"\");\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t</script>\\n'\n"
    returnVal += "\t\thtmlSnippet += '</div>\\n'\n"
    returnVal += "\t\treturn htmlSnippet\n"

    return returnVal

  def getInsertById(self):
    returnVal = "\tdef insertOneForm(self):\n"
    returnVal += "\t\thtmlSnippet = \"\"\n"
    returnVal += "\t\thtmlSnippet += '<div id=\"div_"+self.controllerDict["name"]+"Form\">\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t<label class=\"form_label\" for=\"txt_"+thisProp["name"]+"\">"+thisProp["name"]+":</label>\\n'\n"
        returnVal += "\t\thtmlSnippet += '\\t<input type=\"text\" class=\"form_text\" id=\"txt_"+thisProp["name"]+"\" data-param=\""+thisProp["name"]+"\" value=\"\" />\\n'\n"
        returnVal += "\t\thtmlSnippet += '\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\t<button id=\"btn_submit"+self.controllerDict["name"]+"\" class=\"submitButton\">Submit</button>\\n'\n"
    returnVal += "\t\thtmlSnippet += \"<a href='/"+self.controllerDict["name"]+"'>Cancel</a>\"\n"
    returnVal += "\t\thtmlSnippet += '\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t<script>\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t$(document).ready(function(){\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t$(\"#btn_submit"+self.controllerDict["name"]+"\").click(function(){\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\tvar "+thisProp["name"]+"Val = $(\"#txt_"+thisProp["name"]+"\").val();\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\tif("
    
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += thisProp["name"]+"Val != \"\" && "

    
    returnVal = returnVal[:-3]

    returnVal += ")\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t{\\n'\n"


    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t$.ajax({\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\tmethod: \"POST\",\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\turl: \""+self.controllerDict["name"]+"\",\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\tdata: {\\n'\n"
    

    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\t\"values\": { "
    
    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\""+thisProp["name"]+"\": "+thisProp["name"]+"Val," 

    if returnVal[-1] == ",":
      returnVal = returnVal[:-1]
    returnVal += "},\\n'\n"


    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\t\"call\" : \"insert\"\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t})\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t.done(function(msg) {\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\tif(msg == \"Successful Insertion\")\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t{\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t\\twindow.location.replace(\"/"+self.controllerDict["name"]+"\");\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\telse\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t{\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\talert(\"Insertion Failed\");\\n'\n"

    for prop in self.controllerDict["properties"]:
      thisProp = self.controllerDict["properties"][prop]
      if thisProp["data_type"] in au.knownTypes and thisProp["is_Array"] != True:
        returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t\\t$(\"#txt_"+thisProp["name"]+"\").val(\"\");\\n'\n"

    returnVal += "\t\thtmlSnippet += '\\t\\t\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t}\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t\\t});\\n'\n"
    returnVal += "\t\thtmlSnippet += '\\t</script>\\n'\n"
    returnVal += "\t\thtmlSnippet += '</div>\\n'\n"
    returnVal += "\t\treturn htmlSnippet\n"

    return returnVal

