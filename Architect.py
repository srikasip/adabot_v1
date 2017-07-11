import Ada_Utilities as autil

class Architect:
  def __init__(self, appName):
    self.appName = appName
    self.setProjectArchitecture()

  def setProjectArchitecture(self):
    #First Create a Project Folder
    directories = [
                    {"name": self.appName, "relative": ""},
                    {"name": "writerInstructions", "relative": self.appName},
                    {"name": "Classes", "relative": self.appName},
                    {"name": "static", "relative": self.appName},
                    {"name": "css", "relative": self.appName + "/static"},
                    {"name": "images", "relative": self.appName + "/static"},
                    {"name": "scripts", "relative": self.appName + "/static"}
                  ]

    for a_dir in directories:
      isSetCorrectly = autil.dirCreateCheck(a_dir["name"], a_dir["relative"])
      
      if isSetCorrectly != True:
        return False
    
    #Add the Root Directory Stuff: 
    rootFiles = [
                  "Ada_Utilities.py",
                  "Procfile",
                  "requirements.txt",
                  "StaticHelper.py",
                  "webserver.py",
                  "testlauncher.py"
                ]

    for root in rootFiles:
      readHandle = "BoilerPlateCode/" + root
      writeHandle = self.appName + "/" + root

      fileText = autil.getFileText(readHandle)
      autil.writeText(writeHandle, fileText)


    #Add Random File dependencies:
    #1. Add Classes __init__ file
    writeHandle = self.appName + "/Classes/__init__.py"
    autil.writeText(writeHandle, "")

    #2. #TODO: Add a default favicon to the images folder
    return True



  def loadTemplatePages(self):
    page_text = autil.getFileText("defaultLayout.html")

    for a_class in self.datamodel:
      classPageText = page_text.replace("ADABOT_TESTAPP_TITLE_PAGE", a_class)
      writeHandle = self.appName + "/static/" + a_class + ".html"
      autil.writeText(writeHandle, classPageText)
    return True


  def makeDynamicHelper(self):
    theText = self.getDynamicHelperText()
    writeHandle = self.appName + "/DynamicHelper.py"

    autil.writeText(writeHandle, theText)

  def getDynamicHelperText(self):

    handle = self.appName + "/writerInstructions/datamodel.json"
    self.datamodel = autil.getFileJSON(handle)

    classes = list(self.datamodel.keys())

    dynamicServer = "from bs4 import BeautifulSoup as bs\n"
    dynamicServer += "import json\n"
    dynamicServer += "from pprint import pprint\n"
    dynamicServer += "from datetime import datetime\n"
    dynamicServer += "import requests\n"
    dynamicServer += "import Ada_Utilities as au\n"
    dynamicServer += "from sqlalchemy.orm import sessionmaker, session\n"
    dynamicServer += "from Classes.ObjectsFile import *\n"
    for a_class in classes:
      dynamicServer += "from Classes."+a_class+" import "+a_class+"Viewer as "+a_class+"ViewCont\n"
    
    dynamicServer += "class DynamicHelper:\n"
    dynamicServer += "\tdef __init__(self):\n"
    dynamicServer += "\t\tself.initiated = True\n"
    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef PostDynamicContent(mainPath, params):\n"

    dynamicServer += "\t\tif mainPath == \""+classes[0].lower()+"\":\n"
    dynamicServer += "\t\t\t"+classes[0]+"Obj = "+classes[0]+"ViewCont()\n"
    dynamicServer += "\t\t\tdata, content_type = DynamicHelper.LoadData("+classes[0]+"Obj, params)\n"
    for a_class in classes[1:]:
      dynamicServer += "\t\telif mainPath == \""+a_class.lower()+"\":\n"
      dynamicServer += "\t\t\t"+a_class+"Obj = "+a_class+"ViewCont()\n"
      dynamicServer += "\t\t\tdata, content_type = DynamicHelper.LoadData("+a_class+"Obj, params)\n"
    dynamicServer += "\t\telse:\n"
    dynamicServer += "\t\t\tdata = \"This object is not handled\"\n"
    dynamicServer += "\t\t\tcontent_type = \"text/plain\"\n"
    dynamicServer += "\t\treturn data, content_type\n"


    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef GetDynamicContent(mainPath, params):\n"
    dynamicServer += "\t\t# if len(params)<= 0:\n"
    dynamicServer += "\t\tif mainPath == \""+classes[0].lower()+"\":\n"
    dynamicServer += "\t\t\t"+classes[0]+"Obj = "+classes[0]+"ViewCont()\n"
    dynamicServer += "\t\t\thandle = \"static/"+classes[0]+".html\"\n"
    dynamicServer += "\t\t\tdata = DynamicHelper.FetchFiles(handle, "+classes[0]+"Obj, params)\n"
    dynamicServer += "\t\t\tcontent_type = \"text/html\"\n"

    for a_class in classes[1:]:

      dynamicServer += "\t\telif mainPath == \""+a_class.lower()+"\":\n"
      dynamicServer += "\t\t\t"+a_class+"Obj = "+a_class+"ViewCont()\n"
      dynamicServer += "\t\t\thandle = \"static/"+a_class+".html\"\n"
      dynamicServer += "\t\t\tdata = DynamicHelper.FetchFiles(handle, "+a_class+"Obj, params)\n"
      dynamicServer += "\t\t\tcontent_type = \"text/html\"\n"

    dynamicServer += "\t\telse:\n"
    dynamicServer += "\t\t\tdata = \"<html><head></head><body>This page is not real</body></html>\"\n"
    dynamicServer += "\t\t\tcontent_type = \"text/html\"\n"
    dynamicServer += "\t\treturn data, content_type\n"


    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef LoadData(sentController, params):\n"
    dynamicServer += "\t\tif len(params) <=0:\n"
    dynamicServer += "\t\t\tdata = \"ERROR: No data to laod\"\n"
    dynamicServer += "\t\t\tcontent_type = \"text/plain\"\n"
    dynamicServer += "\t\telse: \n"
    dynamicServer += "\t\t\tif params[\"call\"] == \"insert\":\n"
    dynamicServer += "\t\t\t\tdata = sentController.insertOneLoad(params)\n"
    dynamicServer += "\t\t\t\tcontent_type = \"text/plain\"\n"
    dynamicServer += "\t\t\telif params[\"call\"] == \"edit\":\n"
    dynamicServer += "\t\t\t\tdata = sentController.editOneLoad(params)\n"
    dynamicServer += "\t\t\t\tcontent_type = \"text/plain\"\n"
    dynamicServer += "\t\t\telif params[\"call\"] == \"delete\":\n"
    dynamicServer += "\t\t\t\tidVal = int(params[\"val\"])\n"
    dynamicServer += "\t\t\t\tdata, isSuccess = sentController.deleteOne(idVal)\n"
    dynamicServer += "\t\t\t\tcontent_type = \"text/plain\"\n"
    dynamicServer += "\t\t\telse: \n"
    dynamicServer += "\t\t\t\tdata = \"Nothing to show for myself\"\n"
    dynamicServer += "\t\t\t\tcontent_type = \"text/plain\"\t\t\t\n"
    dynamicServer += "\t\treturn data, content_type\n"
    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef FetchFiles(filehandle, sentController, params):\n"
    dynamicServer += "\t\tif len(params)<=0:\n"
    dynamicServer += "\t\t\thtmlSnippet = sentController.viewAll()\n"
    dynamicServer += "\t\telse: \n"
    dynamicServer += "\t\t\tif params[\"call\"] == \"insert\":\n"
    dynamicServer += "\t\t\t\thtmlSnippet = sentController.insertOneForm()\n"
    dynamicServer += "\t\t\telif params[\"call\"] == \"edit\":\n"
    dynamicServer += "\t\t\t\tidVal = int(params[\"val\"])\n"
    dynamicServer += "\t\t\t\thtmlSnippet = sentController.editOneForm(idVal)\n"
    dynamicServer += "\t\t\telif params[\"call\"] == \"view\":\n"
    dynamicServer += "\t\t\t\tidVal = int(params[\"val\"])\n"
    dynamicServer += "\t\t\t\thtmlSnippet = sentController.viewOneForm(idVal)\n"
    dynamicServer += "\t\t\telif params[\"call\"] == \"delete\":\n"
    dynamicServer += "\t\t\t\tidVal = int(params[\"val\"])\n"
    dynamicServer += "\t\t\t\thtmlSnippet, isSuccess = sentController.deleteOne(idVal)\n"
    dynamicServer += "\t\t\t\tif isSuccess:\n"
    dynamicServer += "\t\t\t\t\thtmlSnippet = \"<div>Delete Successfully <br/><a href='/color'>Return to Colors</a></div>\"\n"
    dynamicServer += "\t\t\t\telse:\n"
    dynamicServer += "\t\t\t\t\thtmlSnippet = \"<div>Delete was Unsuccessful</div>\"\n"
    dynamicServer += "\t\t\telse:\n"
    dynamicServer += "\t\t\t\thtmlSnippet = \"<div>Do not have that yet.</div>\"\n"
    dynamicServer += "\t\tpageHtml = au.InsertBody(filehandle, htmlSnippet, tagName=\"body\")\n"
    dynamicServer += "\t\treturn pageHtml\n"
    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef LoadTemplates(pageUrl):\n"
    dynamicServer += "\t\tpageSoup = DynamicHelper.getUrlSoup(pageUrl)\n"
    dynamicServer += "\t\t#find all svgtemplate and all template blocks. I'll do it in two steps so has to handle nested htmlTemplates (might be kinda nice)\n"
    dynamicServer += "\t\t#doing htmltemplates first so that i can get the SVGs stored in templates\n"
    dynamicServer += "\t\ttemplateBlocks = pageSoup.find_all(\"htmltemplate\")\n"
    dynamicServer += "\t\t#support nested templating.\n"
    dynamicServer += "\t\twhile(len(templateBlocks) > 0):\n"
    dynamicServer += "\t\t\tfor block in templateBlocks:\n"
    dynamicServer += "\t\t\t\turl = block.get_text().strip()\n"
    dynamicServer += "\t\t\t\turl = \"static/\" + url\n"
    dynamicServer += "\t\t\t\tblockSoup = DynamicHelper.getUrlSoup(url)\n"
    dynamicServer += "\t\t\t\t#bring headers together\n"
    dynamicServer += "\t\t\t\tmainHead = pageSoup.find(\"head\")\n"
    dynamicServer += "\t\t\t\tmainHead.append(blockSoup.find(\"head\"))\n"
    dynamicServer += "\t\t\t\tmainHead.find(\"head\").unwrap()\n"
    dynamicServer += "\t\t\t\t#bring body content and put in the right place\n"
    dynamicServer += "\t\t\t\tblock.replaceWith((blockSoup.find(\"body\")).find(\"div\", {\"class\":\"template\"}))\n"
    dynamicServer += "\t\t\ttemplateBlocks = pageSoup.find_all(\"htmltemplate\")\n"
    dynamicServer += "\t\t#then to SVGs, which might be invoked in the main file or the template files. shouldn't actually matter, since they are now collapsed into pageSoup.\n"
    dynamicServer += "\t\tsvg_blocks = pageSoup.find_all('svgtemplate')\n"
    dynamicServer += "\t\tfor svg_block in svg_blocks:\n"
    dynamicServer += "\t\t\turl = svg_block.get_text().strip()\n"
    dynamicServer += "\t\t\turl = \"static/images/\" + url\n"
    dynamicServer += "\t\t\tsvg_soup = DynamicHelper.getUrlSoup(url)\n"
    dynamicServer += "\t\t\tsvg_block.replaceWith(svg_soup.find(\"svg\"))\n"
    dynamicServer += "\t\tdataString = (pageSoup.prettify()).encode('utf-8').strip()\n"
    dynamicServer += "\t\treturn dataString\n"
    dynamicServer += "\t@staticmethod \n"
    dynamicServer += "\tdef getUrlContent(pageURL):\n"
    dynamicServer += "\t\twith open(pageURL, \"r\") as myPage:\n"
    dynamicServer += "\t\t\tpageData = myPage.read()\n"
    dynamicServer += "\t\treturn pageData\n"
    dynamicServer += "\t@staticmethod\n"
    dynamicServer += "\tdef getUrlSoup(pageURL):\n"
    dynamicServer += "\t\tcontent = DynamicHelper.getUrlContent(pageURL)\n"
    dynamicServer += "\t\treturn bs(content, \"html.parser\")\n"


    return dynamicServer
