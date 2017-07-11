from bs4 import BeautifulSoup as bs
import json
from pprint import pprint
from datetime import datetime
import requests
import Ada_Utilities as au

from sqlalchemy.orm import sessionmaker, session
from Classes.ObjectsFile import Color, Person, ENGINE, BASE, APPNAME
from Classes.Color import ColorViewer as colorViewCont
from Classes.Person import PersonViewer as personViewCont


class DynamicHelper:
  def __init__(self):
    self.initiated = True

  @staticmethod
  def PostDynamicContent(mainPath, params):
    if mainPath == "color":
      ColorObj = colorViewCont()
      data, content_type = DynamicHelper.LoadData(ColorObj, params)
    else:
      data = "Only Color is handled"
      content_type = "text/plain"

    return data, content_type


  @staticmethod
  def GetDynamicContent(mainPath, params):
    # if len(params)<= 0:
    if mainPath == "color":
      ColorObj = colorViewCont()
      handle = "static/color.html"

      data = DynamicHelper.FetchFiles(handle, ColorObj, params)
      content_type = "text/html"

    elif mainPath == "person":
      PersonObj = personViewCont()
      handle = "static/person.html"

      data = DynamicHelper.FetchFiles(handle, PersonObj, params)
      content_type = "text/html"

    elif mainPath == "hold":
      handle = "static/holdPage.html"
      data = au.getFileText(handle)
      content_type = "text/html"
    else:
      data = "<html><head></head><body>This page is not real</body></html>"
      content_type = "text/html"

    return data, content_type


  @staticmethod
  def LoadData(sentController, params):
    if len(params) <=0:
      data = "ERROR: No data to laod"
      content_type = "text/plain"
    
    else: 
      if params["call"] == "insert":
        data = sentController.insertOneLoad(params)
        content_type = "text/plain"
      elif params["call"] == "edit":
        data = sentController.editOneLoad(params)
        content_type = "text/plain"
      elif params["call"] == "delete":
        idVal = int(params["val"])
        data, isSuccess = sentController.deleteOne(idVal)
        content_type = "text/plain"
      else: 
        data = "Nothing to show for myself"
        content_type = "text/plain"      

    return data, content_type


  @staticmethod
  def FetchFiles(filehandle, sentController, params):
    if len(params)<=0:
      htmlSnippet = sentController.viewAll()
    else: 
      if params["call"] == "insert":
        htmlSnippet = sentController.insertOneForm()
      elif params["call"] == "edit":
        idVal = int(params["val"])
        htmlSnippet = sentController.editOneForm(idVal)
      elif params["call"] == "view":
        idVal = int(params["val"])
        htmlSnippet = sentController.viewOneForm(idVal)
      elif params["call"] == "delete":
        idVal = int(params["val"])
        htmlSnippet, isSuccess = sentController.deleteOne(idVal)
        if isSuccess:
          htmlSnippet = "<div>Delete Successfully <br/><a href='/color'>Return to Colors</a></div>"
        else:
          htmlSnippet = "<div>Delete was Unsuccessful</div>"

      else:
        htmlSnippet = "<div>Do not have that yet.</div>"

    pageHtml = au.InsertBody(filehandle, htmlSnippet, tagName="body")

    return pageHtml

  @staticmethod
  def LoadTemplates(pageUrl):
    pageSoup = DynamicHelper.getUrlSoup(pageUrl)


    #find all svgtemplate and all template blocks. I'll do it in two steps so has to handle nested htmlTemplates (might be kinda nice)
    
    #doing htmltemplates first so that i can get the SVGs stored in templates
    templateBlocks = pageSoup.find_all("htmltemplate")
    
    #support nested templating.
    while(len(templateBlocks) > 0):
      for block in templateBlocks:
        url = block.get_text().strip()
        url = "static/" + url
        blockSoup = DynamicHelper.getUrlSoup(url)
        
        #bring headers together
        mainHead = pageSoup.find("head")
        mainHead.append(blockSoup.find("head"))
        mainHead.find("head").unwrap()


        #bring body content and put in the right place
        block.replaceWith((blockSoup.find("body")).find("div", {"class":"template"}))

      templateBlocks = pageSoup.find_all("htmltemplate")


    #then to SVGs, which might be invoked in the main file or the template files. shouldn't actually matter, since they are now collapsed into pageSoup.
    svg_blocks = pageSoup.find_all('svgtemplate')
    for svg_block in svg_blocks:
      url = svg_block.get_text().strip()
      url = "static/images/" + url
      svg_soup = DynamicHelper.getUrlSoup(url)
      svg_block.replaceWith(svg_soup.find("svg"))


    dataString = (pageSoup.prettify()).encode('utf-8').strip()

    return dataString


  @staticmethod 
  def getUrlContent(pageURL):
    with open(pageURL, "r") as myPage:
      pageData = myPage.read()

    return pageData

  @staticmethod
  def getUrlSoup(pageURL):
    content = DynamicHelper.getUrlContent(pageURL)
    return bs(content, "html.parser")
