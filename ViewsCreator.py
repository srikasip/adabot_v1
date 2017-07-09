import Ada_Utilities as au

class ViewsCreator: 
  def __init__(self, appName, objectName):
    self.objectName = objectName
    self.appName = appName
    filehandle = appName + "/writerInstructions/datamodel.json"
  
    self.app_datamodel = au.getFileJSON(filehandle)
    self.objectModel = self.app_datamodel[objectName]

    # The views to be created are simple:
    # 0. Object Views Main Class
    # 1. Make a select * View for the model
    # 2. Make a select 1 View for the model
    # 2a. Delete the 1 object
    # 3. Make an Edit 1 view for the model

    # REACH:
    # 1a. Add a search box to filter
    # 1b. Make an update all (selected?)
    # 1c. Delete all sub-searched

  def makeViewsMainClass(self):
    
