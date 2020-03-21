
from flask import Flask,render_template,request,send_file
from dataFetcher import createHeatMap,summaryData
import json
# from apscheduler.scheduler import Scheduler



# sched = Scheduler()
# sched.daemonic = False
# sched.start()


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

@app.route('/triggerData')
def triggerData():
	print('triggerring new data')
	createHeatMap()
	print('triggerring new data')
	summaryData()
	return 'trigger hit'

# @sched.scheduled_job('interval', seconds=10)
# def test():
# 	print ("TEST SUCCESS")


if __name__=='__main__':
	# sched.configure(timezone='Asia/Kolkata')
	# sched.add_cron_job(test, minute='0-10')
	app.run(threaded=True,port=5000)


