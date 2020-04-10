
from flask import Flask,render_template,request,send_file,jsonify
from dataFetcher import HeatMapper
import json
from UnofficalAPI import InternalDataAPI
# from apscheduler.scheduler import Scheduler



# sched = Scheduler()
# sched.daemonic = False
# sched.start()


app=Flask(__name__)

@app.route('/')
def index():
	triggerData()
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

@app.route('/triggerData')
def triggerData():
	print('triggerring new data')
	HeatMapper().createHeatMap()
	print('triggerring new data')
	HeatMapper().summaryData()
	return 'trigger hit'

# @sched.scheduled_job('interval', seconds=10)
# def test():
# 	print ("TEST SUCCESS")

@app.route('/unofficalData')
def unofficalData():
	internalData=InternalDataAPI()
	return jsonify(result=internalData.convertToConsumedJSON(internalData.fetchData()))

@app.route('/test')
def test():
	return jsonify(result=InternalDataAPI().fetchData())


if __name__=='__main__':
	# sched.configure(timezone='Asia/Kolkata')
	# sched.add_cron_job(test, minute='0-10')
	app.run(debug=True,threaded=True,port=5000)


