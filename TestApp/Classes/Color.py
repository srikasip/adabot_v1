import Ada_Utilities as au
from sqlalchemy.orm import sessionmaker, session
from Classes.ObjectsFile import Person, Color, ENGINE, BASE, APPNAME
class ColorController:
	def __init__(self):
		Session = sessionmaker(bind=ENGINE)
		self.session = Session()
	def selectAll(self):
		allColor = self.session.query(Color).all()
		return allColor
	def selectbyID(self, send_id):
		oneColor = self.session.query(Color).filter(Color.ada_id == send_id).one()
		return oneColor
	def deletebyID(self, send_id):
		try:
			oneColor = self.session.query(Color).filter(Color.ada_id == send_id).delete()
			self.session.commit()
			return True
		except:
			return False
	def insertOne(self, params):
		try:
			newColor = Color(params['name'],params['color'],params['ada_id'])
			self.session.add(newColor)
			self.session.commit()
			return True
		except:
			return False
	def editOne(self, params):
		oneColor = self.session.query(Color).filter(Color.ada_id == params['ada_id'])
		oneColor.update({'name': params['name'],'color': params['color'],'ada_id': params['ada_id']})
		try:
			self.session.commit()
			return True
		except:
			return False





class ColorViewer:
	def __init__(self):
		pass

	def viewAll(self):
		a_ColorController = ColorController()
		allColor = a_ColorController.selectAll()
		htmlSnippet = "<table>\n"
		htmlSnippet += "\t<tr>\n"
		htmlSnippet += "\t\t<th>name</th>\n"
		htmlSnippet += "\t\t<th>color</th>\n"
		htmlSnippet += "\t\t<th>ada_id</th>\n"
		htmlSnippet += "\t\t<th>Next</th>\n"
		htmlSnippet += "\t</tr>\n"
		for a_Color in allColor:
			htmlSnippet += "\t<tr>\n"
			htmlSnippet += "\t\t<td>"+a_Color.name+"</td>\n"
			htmlSnippet += "\t\t<td>"+a_Color.color+"</td>\n"
			htmlSnippet += "\t\t<td>"+str(a_Color.ada_id)+"</td>\n"
			htmlSnippet += "\t\t<td><a href='/Color?call=view&val="+str(a_Color.ada_id)+"'>View</a>"
			htmlSnippet += "<a href='/Color?call=edit&val="+str(a_Color.ada_id)+"'>Edit</a>"
			htmlSnippet += "<a href='/Color?call=delete&val="+str(a_Color.ada_id)+"'>Delete</a></td>\n"
			htmlSnippet += "\t</tr>\n"
		htmlSnippet += "</table>\n"
		htmlSnippet += "<a href='/Color?call=insert'>Create New Color</a></td>\n"
		return htmlSnippet
	def viewOneForm(self, sentIDValue):
		a_ColorController = ColorController()
		returnColor = a_ColorController.selectbyID(sentIDValue)
		htmlSnippet = ""
		htmlSnippet += '<div id="div_ColorForm">\
'
		htmlSnippet += '\t<label class="form_label" for="lbl_name">name:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_name" data-param="name">'+returnColor.name+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="lbl_color">color:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_color" data-param="color">'+returnColor.color+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="lbl_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_ada_id" data-param="ada_id">'+returnColor.ada_id+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += "<a href='/Color?call=edit&val="+str(returnColor.ada_id)+"'>Edit</a>"
		htmlSnippet += "<a href='/Color'>Go Back</a>"
		htmlSnippet += '\n'
		htmlSnippet += '</div>\n'
		return htmlSnippet
	def deleteOne(self, sentIDValue):
		a_ColorController = ColorController()
		returnVal = a_ColorController.deletebyID(sentIDValue)
		if returnVal:
			htmlSnippet = 'Successful Deletion'
		else:
			htmlSnippet = 'Unsuccessful Deletion'
		return htmlSnippet, returnVal
	def insertOneForm(self):
		htmlSnippet = ""
		htmlSnippet += '<div id="div_ColorForm">\n'
		htmlSnippet += '\t<label class="form_label" for="txt_name">name:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_name" data-param="name" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_color">color:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_color" data-param="color" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_ada_id" data-param="ada_id" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<button id="btn_submitColor" class="submitButton">Submit</button>\n'
		htmlSnippet += "<a href='/Color'>Cancel</a>"
		htmlSnippet += '\n'
		htmlSnippet += '\t<script>\n'
		htmlSnippet += '\t\t$(document).ready(function(){\n'
		htmlSnippet += '\t\t\t$("#btn_submitColor").click(function(){\n'
		htmlSnippet += '\t\t\t\tvar nameVal = $("#txt_name").val();\n'
		htmlSnippet += '\t\t\t\tvar colorVal = $("#txt_color").val();\n'
		htmlSnippet += '\t\t\t\tvar ada_idVal = $("#txt_ada_id").val();\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t\t\t\tif(nameVal != "" && colorVal != "" && ada_idVal != "" )\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t$.ajax({\n'
		htmlSnippet += '\t\t\t\t\t\tmethod: "POST",\n'
		htmlSnippet += '\t\t\t\t\t\turl: "Color",\n'
		htmlSnippet += '\t\t\t\t\t\tdata: {\n'
		htmlSnippet += '\t\t\t\t\t\t"values": { "name": nameVal,"color": colorVal,"ada_id": ada_idVal},\n'
		htmlSnippet += '\t\t\t\t\t\t"call" : "insert"\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\t})\n'
		htmlSnippet += '\t\t\t\t.done(function(msg) {\n'
		htmlSnippet += '\t\t\t\t\tif(msg == "Successful Insertion")\n'
		htmlSnippet += '\t\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t\twindow.location.replace("/Color");\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\telse\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\talert("Insertion Failed");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_name").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_color").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_ada_id").val("");\n'
		htmlSnippet += '\t\t\t\t}\n'
		htmlSnippet += '\t\t\t});\n'
		htmlSnippet += '\t\t}\n'
		htmlSnippet += '\t\t});\n'
		htmlSnippet += '\t\t});\n'
		htmlSnippet += '\t</script>\n'
		htmlSnippet += '</div>\n'
		return htmlSnippet
	def editOneForm(self, sentIDValue):
		a_ColorController = ColorController()
		returnColor = a_ColorController.selectbyID(sentIDValue)
		htmlSnippet = ""
		htmlSnippet += '<div id="div_ColorForm">\n'
		htmlSnippet += '\t<label class="form_label" for="txt_name">name:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_name" data-param="name" value="'+returnColor.name+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_color">color:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_color" data-param="color" value="'+returnColor.color+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_ada_id" data-param="ada_id" value="'+returnColor.ada_id+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<button id="btn_submitColor" class="submitButton">Submit</button>\n'
		htmlSnippet += "<a href='/Color'>Cancel</a>"
		htmlSnippet += '\n'
		htmlSnippet += '\t<script>\n'
		htmlSnippet += '\t\t$(document).ready(function(){\n'
		htmlSnippet += '\t\t\t$("#btn_submitColor").click(function(){\n'
		htmlSnippet += '\t\t\t\tvar nameVal = $("#txt_name").val();\n'
		htmlSnippet += '\t\t\t\tvar colorVal = $("#txt_color").val();\n'
		htmlSnippet += '\t\t\t\tvar ada_idVal = $("#txt_ada_id").val();\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t\t\t\tif(nameVal != "" && colorVal != "" && ada_idVal != "" )\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t$.ajax({\n'
		htmlSnippet += '\t\t\t\t\t\tmethod: "POST",\n'
		htmlSnippet += '\t\t\t\t\t\turl: "Color",\n'
		htmlSnippet += '\t\t\t\t\t\tdata: {\n'
		htmlSnippet += '\t\t\t\t\t\t"values": { "name": nameVal,"color": colorVal,"ada_id": ada_idVal,"ada_id": '+str(returnColor.ada_id)+'},\n'
		htmlSnippet += '\t\t\t\t\t\t"call" : "edit"\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\t})\n'
		htmlSnippet += '\t\t\t\t.done(function(msg) {\n'
		htmlSnippet += '\t\t\t\t\tif(msg == "Successful Insertion")\n'
		htmlSnippet += '\t\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t\twindow.location.replace("/Color");\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\telse\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\talert("Insertion Failed");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_name").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_color").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_ada_id").val("");\n'
		htmlSnippet += '\t\t\t\t}\n'
		htmlSnippet += '\t\t\t});\n'
		htmlSnippet += '\t\t}\n'
		htmlSnippet += '\t\t});\n'
		htmlSnippet += '\t\t});\n'
		htmlSnippet += '\t</script>\n'
		htmlSnippet += '</div>\n'
		return htmlSnippet
	def editOneLoad(self, params):
		a_ColorController = ColorController()
		returnVal = a_ColorController.editOne(params["values"])
		if returnVal:
		  sendData = "Successful Insertion"
		else:
		  sendData = "Unsuccessful Insertion"
		return sendData
	def insertOneLoad(self, params):
		a_ColorController = ColorController()
		returnVal = a_ColorController.insertOne(params["values"])
		if returnVal:
		  sendData = "Successful Insertion"
		else:
		  sendData = "Unsuccessful Insertion"
		return sendData
