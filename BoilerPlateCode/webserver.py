from StaticHelper import StaticHelper as static
from DynamicHelper import DynamicHelper as dynamic
from pprint import pprint
import json
from cgi import parse_qs

def app(environ, start_response):
  data = ""

  if environ['REQUEST_METHOD'] == 'POST':
    data, content_type = PostRequests(environ)
  else:
    data, content_type = GetRequests(environ)

  start_response("200 OK", [
    ("Content-Type", content_type),
    ("Content-Length", str(len(data)))
  ])

  if data:
    #FOR Python 2:
    #return iter([data])

    #FOR Python 3:
    #return [bytes(data, 'utf-8')]
    #Safer encoding function:
    return [bytes(data.encode('utf-8'))]
  else:
    return ""

def PostRequests(environ):
  mainPath, fullPath = GetPathString(environ["PATH_INFO"])
  if mainPath == "static":
    data, content_type = static.GetStaticContent(fullPath)

  else:
    try:
      request_body_size = int(environ['CONTENT_LENGTH'])
      request_body = environ['wsgi.input'].read(request_body_size)
      sentData = JSONfromQS(request_body)
      
      data, content_type = dynamic.PostDynamicContent(mainPath, sentData)

    except (TypeError, ValueError):
      data = "Error"
      content_type = "text/plain"
      raise

  return data, content_type


def GetRequests(environ):

  #Get Subpath and figure out which page the user should go to, but ignore "subpaths"
  mainPath, fullPath = GetPathString(environ["PATH_INFO"])

  #Get Params and put them in a sensible dictionary
  sentParams = environ["QUERY_STRING"].split('&')
  params = {}
  if len(sentParams)>0:
    for param in sentParams: 
      param = param.strip()
      parts = param.split("=")
      if len(parts)>=2:
        params[parts[0]] = parts[1]

  content_type = ""
  if mainPath != "static":
    #Route the user to the right page
    data, content_type = dynamic.GetDynamicContent(mainPath, params)

  elif mainPath == "static":
    #Get the static content resource that is being asked for
    data, content_type = static.GetStaticContent(fullPath)

  return data, content_type

def GetPathString(path_info):
  subpaths = path_info.split('/')
  mainPath = ""
  if len(subpaths)>=2:
    mainPath = subpaths[1]

  fullpath = path_info[1:]
  if fullpath == "favicon.ico":
    mainPath = "static"
    fullpath = "static/images/favicon.png"

  mainPath = mainPath.lower()
  return mainPath, fullpath

def JSONfromQS(sent_qs):
  parsed_body = parse_qs(sent_qs)
  sentData = {}
  
  for key in parsed_body:
    newKeyPath = key.replace("]", '')
    newKeys = [x for x in newKeyPath.split('[') if x]
    
    numKeys = len(newKeys)
    aDictionary = {}

    if len(parsed_body[key])>1:
      holdValue = parsed_body[key]
    elif len(parsed_body[key])==1:
      holdValue = parsed_body[key][0]
    else:
      holdValue = ""

    biferDict = sentData
    for biferIndex in range(0,numKeys):
      if newKeys[biferIndex] in list(biferDict.keys()):
        biferDict = biferDict[newKeys[biferIndex]]
      else:
        break

    for keyIndex in range(numKeys-1, biferIndex, -1):
      aDictionary[newKeys[keyIndex]] = holdValue
      holdValue = aDictionary
      aDictionary = {}


    biferDict[newKeys[biferIndex]] = holdValue

  return sentData
