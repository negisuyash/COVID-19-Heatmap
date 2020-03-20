
from flask import Flask,render_template,request,send_file
import json


# API_KEY='AIzaSyBx1SkG_lcKjI1HJ2cyRDMTnS1k9j0LxpU'

app=Flask(__name__)

@app.route('/')
def index():
	with open('./data/data.json','r') as inputfile:
		data=json.load(inputfile)
	deaths=data['data']['summary']['deaths']
	total=data['data']['summary']['total']
	confirmedCasesIndian=data['data']['summary']['confirmedCasesIndian']
	confirmedCasesForeign=data['data']['summary']['confirmedCasesForeign']
	return render_template('welcome.html',total=total,confirmedCasesIndian=confirmedCasesIndian,confirmedCasesForeign=confirmedCasesForeign,deaths=deaths)

@app.route('/getHeatMap')
def getHeatMap():
	return render_template('export.html')



if __name__=='__main__':
    app.run(threaded=True,port=5000)


