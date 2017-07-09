import Ada_Utilities as au
from ControllerObj import ControllerObj as CObj


class ControllerCreator:
  def __init__(self, appName):
    self.appName = appName

    datamodelHandle = self.appName + "/writerInstructions/datamodel.json"
    self.datamodel = au.getFileJSON(datamodelHandle)

    for a_classHandle in self.datamodel:
      aClassController = CObj(self.datamodel[a_classHandle], self.datamodel)
      classText = aClassController.writeController()
      fileHandle = self.appName + "/" + a_classHandle + ".py"

      au.writeText(fileHandle, classText)

