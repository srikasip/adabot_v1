import Ada_Utilities as au
from ControllerObj import ControllerObj as CObj
from ViewsCreator import ViewerObj as VObj


class ControllerCreator:
  def __init__(self, appName):
    self.appName = appName

    datamodelHandle = self.appName + "/writerInstructions/datamodel.json"
    self.datamodel = au.getFileJSON(datamodelHandle)

    for a_classHandle in self.datamodel:
      aClassController = CObj(self.datamodel[a_classHandle], self.datamodel)
      aViewController = VObj(self.datamodel[a_classHandle], self.datamodel)

      classText = aClassController.writeController()
      classText += "\n\n\n"
      classText += aViewController.writeViewer()
      
      fileHandle = self.appName + "/Classes/" + a_classHandle + ".py"

      au.writeText(fileHandle, classText)

