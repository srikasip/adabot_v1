import json
import Ada_Utilities as au

class InitCreator:
  #This initializes the DataModel for a new app.
  #You can consider this to be the competence of any new class object that is created
  def __init__(self, appName):
    self.appName = appName
    writeableArr = []
    #Just create the engine and create the base 
    writeableArr.append(self.getImportText())
    writeableArr.append("BASE = declarative_base()")
    writeableArr.append("ENGINE = create_engine('sqlite:///adaDB_"+self.appName+".db', echo=False)")
    writeableArr.append("APPNAME = '"+self.appName+"'")

    #and write them both to a file with everything i need
    fileHandle = self.appName + "/Initializer.py"
    writeableTxt = "\n".join(writeableArr)
    
    au.writeText(fileHandle, writeableTxt)

  def getImportText(self):
    importTxt = "from sqlalchemy import create_engine\n"
    importTxt += "from sqlalchemy.ext.declarative import declarative_base\n"

    return importTxt