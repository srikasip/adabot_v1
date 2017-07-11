import sys

class StaticHelper:
  def __init__(self):
    self.initiated = True

  @staticmethod
  def GetStaticContent(fileLocation):
    try:
      extension_parts = fileLocation.split(".")
      ending = ""
      

      if len(extension_parts)>1:
        ending = extension_parts[1]

      if ending == "css":
        content_type = "text/css"
      elif ending == "js":
        content_type = "application/javascript"
      elif ending in ["jpg", "jpeg", "png", "gif"]:
        content_type = "image/" + ending
      elif ending == "svg":
        content_type = "image/svg+xml"
      elif ending ==  "ico":
        content_type = "image/x-icon"
      elif ending == "json":
        content_type = "application/json"
      else:
        content_type = ""

      if ending in ["css", "js", "svg", "json"]:
        with open(fileLocation) as myFile:
          data = myFile.read().encode('utf-8').strip()
      else:
        with open(fileLocation, "rb") as myFile:
          data = myFile.read()

      print("Resource SUCCESS: " + fileLocation)
      return data, content_type
      
    except:
      print ("Resource FAILURE: " + fileLocation)
      print (sys.exc_info()[0])
      return "", ""
