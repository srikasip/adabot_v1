import Ada_Utilities as au
from sqlalchemy.orm import sessionmaker, session
from Classes.ObjectsFile import Person, Color, ENGINE, BASE, APPNAME
class PersonController:
	def __init__(self):
		Session = sessionmaker(bind=ENGINE)
		self.session = Session()
	def selectAll(self):
		allPerson = self.session.query(Person).all()
		return allPerson
	def selectbyID(self, send_id):
		onePerson = self.session.query(Person).filter(Person.ada_id == send_id).one()
		return onePerson
	def deletebyID(self, send_id):
		try:
			onePerson = self.session.query(Person).filter(Person.ada_id == send_id).delete()
			self.session.commit()
			return True
		except:
			return False
	def insertOne(self, params):
		try:
			newPerson = Person(params['name'],params['age'],params['ada_id'])
			self.session.add(newPerson)
			self.session.commit()
			return True
		except:
			return False
	def editOne(self, params):
		onePerson = self.session.query(Person).filter(Person.ada_id == params['ada_id'])
		onePerson.update({'name': params['name'],'age': params['age'],'ada_id': params['ada_id']})
		try:
			self.session.commit()
			return True
		except:
			return False





class PersonViewer:
	def __init__(self):
		pass

	def viewAll(self):
		a_PersonController = PersonController()
		allPerson = a_PersonController.selectAll()
		htmlSnippet = "<table>\n"
		htmlSnippet += "\t<tr>\n"
		htmlSnippet += "\t\t<th>name</th>\n"
		htmlSnippet += "\t\t<th>age</th>\n"
		htmlSnippet += "\t\t<th>ada_id</th>\n"
		htmlSnippet += "\t\t<th>Next</th>\n"
		htmlSnippet += "\t</tr>\n"
		for a_Person in allPerson:
			htmlSnippet += "\t<tr>\n"
			htmlSnippet += "\t\t<td>"+a_Person.name+"</td>\n"
			htmlSnippet += "\t\t<td>"+str(a_Person.age)+"</td>\n"
			htmlSnippet += "\t\t<td>"+str(a_Person.ada_id)+"</td>\n"
			htmlSnippet += "\t\t<td><a href='/Person?call=view&val="+str(a_Person.ada_id)+"'>View</a>"
			htmlSnippet += "<a href='/Person?call=edit&val="+str(a_Person.ada_id)+"'>Edit</a>"
			htmlSnippet += "<a href='/Person?call=delete&val="+str(a_Person.ada_id)+"'>Delete</a></td>\n"
			htmlSnippet += "\t</tr>\n"
		htmlSnippet += "</table>\n"
		htmlSnippet += "<a href='/Person?call=insert'>Create New Person</a></td>\n"
		return htmlSnippet
	def viewOneForm(self, sentIDValue):
		a_PersonController = PersonController()
		returnPerson = a_PersonController.selectbyID(sentIDValue)
		htmlSnippet = ""
		htmlSnippet += '<div id="div_PersonForm">\
'
		htmlSnippet += '\t<label class="form_label" for="lbl_name">name:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_name" data-param="name">'+returnPerson.name+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="lbl_age">age:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_age" data-param="age">'+returnPerson.age+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="lbl_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<label class="data_label" id="lbl_ada_id" data-param="ada_id">'+returnPerson.ada_id+'</label>\n'
		htmlSnippet += '\n'
		htmlSnippet += "<a href='/Person?call=edit&val="+str(returnPerson.ada_id)+"'>Edit</a>"
		htmlSnippet += "<a href='/Person'>Go Back</a>"
		htmlSnippet += '\n'
		htmlSnippet += '</div>\n'
		return htmlSnippet
	def deleteOne(self, sentIDValue):
		a_PersonController = PersonController()
		returnVal = a_PersonController.deletebyID(sentIDValue)
		if returnVal:
			htmlSnippet = 'Successful Deletion'
		else:
			htmlSnippet = 'Unsuccessful Deletion'
		return htmlSnippet, returnVal
	def insertOneForm(self):
		htmlSnippet = ""
		htmlSnippet += '<div id="div_PersonForm">\n'
		htmlSnippet += '\t<label class="form_label" for="txt_name">name:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_name" data-param="name" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_age">age:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_age" data-param="age" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_ada_id" data-param="ada_id" value="" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<button id="btn_submitPerson" class="submitButton">Submit</button>\n'
		htmlSnippet += "<a href='/Person'>Cancel</a>"
		htmlSnippet += '\n'
		htmlSnippet += '\t<script>\n'
		htmlSnippet += '\t\t$(document).ready(function(){\n'
		htmlSnippet += '\t\t\t$("#btn_submitPerson").click(function(){\n'
		htmlSnippet += '\t\t\t\tvar nameVal = $("#txt_name").val();\n'
		htmlSnippet += '\t\t\t\tvar ageVal = $("#txt_age").val();\n'
		htmlSnippet += '\t\t\t\tvar ada_idVal = $("#txt_ada_id").val();\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t\t\t\tif(nameVal != "" && ageVal != "" && ada_idVal != "" )\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t$.ajax({\n'
		htmlSnippet += '\t\t\t\t\t\tmethod: "POST",\n'
		htmlSnippet += '\t\t\t\t\t\turl: "Person",\n'
		htmlSnippet += '\t\t\t\t\t\tdata: {\n'
		htmlSnippet += '\t\t\t\t\t\t"values": { "name": nameVal,"age": ageVal,"ada_id": ada_idVal},\n'
		htmlSnippet += '\t\t\t\t\t\t"call" : "insert"\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\t})\n'
		htmlSnippet += '\t\t\t\t.done(function(msg) {\n'
		htmlSnippet += '\t\t\t\t\tif(msg == "Successful Insertion")\n'
		htmlSnippet += '\t\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t\twindow.location.replace("/Person");\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\telse\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\talert("Insertion Failed");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_name").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_age").val("");\n'
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
		a_PersonController = PersonController()
		returnPerson = a_PersonController.selectbyID(sentIDValue)
		htmlSnippet = ""
		htmlSnippet += '<div id="div_PersonForm">\n'
		htmlSnippet += '\t<label class="form_label" for="txt_name">name:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_name" data-param="name" value="'+returnPerson.name+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_age">age:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_age" data-param="age" value="'+returnPerson.age+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<label class="form_label" for="txt_ada_id">ada_id:</label>\n'
		htmlSnippet += '\t<input type="text" class="form_text" id="txt_ada_id" data-param="ada_id" value="'+returnPerson.ada_id+'" />\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t<button id="btn_submitPerson" class="submitButton">Submit</button>\n'
		htmlSnippet += "<a href='/Person'>Cancel</a>"
		htmlSnippet += '\n'
		htmlSnippet += '\t<script>\n'
		htmlSnippet += '\t\t$(document).ready(function(){\n'
		htmlSnippet += '\t\t\t$("#btn_submitPerson").click(function(){\n'
		htmlSnippet += '\t\t\t\tvar nameVal = $("#txt_name").val();\n'
		htmlSnippet += '\t\t\t\tvar ageVal = $("#txt_age").val();\n'
		htmlSnippet += '\t\t\t\tvar ada_idVal = $("#txt_ada_id").val();\n'
		htmlSnippet += '\n'
		htmlSnippet += '\t\t\t\tif(nameVal != "" && ageVal != "" && ada_idVal != "" )\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t$.ajax({\n'
		htmlSnippet += '\t\t\t\t\t\tmethod: "POST",\n'
		htmlSnippet += '\t\t\t\t\t\turl: "Person",\n'
		htmlSnippet += '\t\t\t\t\t\tdata: {\n'
		htmlSnippet += '\t\t\t\t\t\t"values": { "name": nameVal,"age": ageVal,"ada_id": ada_idVal,"ada_id": '+str(returnPerson.ada_id)+'},\n'
		htmlSnippet += '\t\t\t\t\t\t"call" : "edit"\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\t})\n'
		htmlSnippet += '\t\t\t\t.done(function(msg) {\n'
		htmlSnippet += '\t\t\t\t\tif(msg == "Successful Insertion")\n'
		htmlSnippet += '\t\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\t\twindow.location.replace("/Person");\n'
		htmlSnippet += '\t\t\t\t\t}\n'
		htmlSnippet += '\t\t\t\telse\n'
		htmlSnippet += '\t\t\t\t{\n'
		htmlSnippet += '\t\t\t\t\talert("Insertion Failed");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_name").val("");\n'
		htmlSnippet += '\t\t\t\t\t$("#txt_age").val("");\n'
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
		a_PersonController = PersonController()
		returnVal = a_PersonController.editOne(params["values"])
		if returnVal:
		  sendData = "Successful Insertion"
		else:
		  sendData = "Unsuccessful Insertion"
		return sendData
	def insertOneLoad(self, params):
		a_PersonController = PersonController()
		returnVal = a_PersonController.insertOne(params["values"])
		if returnVal:
		  sendData = "Successful Insertion"
		else:
		  sendData = "Unsuccessful Insertion"
		return sendData
