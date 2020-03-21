#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gmaps
import requests
from ipywidgets.embed import embed_minimal_html
import json

# In[2]:

class HeatMapper:

	def createHeatMap(self):
		gmaps.configure(api_key='AIzaSyCu4BBQA_f5u428YPwFB1Zls8UwFXaFN1g')

		covid19_data=requests.get('https://api.rootnet.in/covid19-in/stats/latest').json()
		covid19_contact=requests.get('https://api.rootnet.in/covid19-in/contacts').json()
		#covid19_data

		state_data={'Andaman And Nicobar': {'coordinates': [11.7400867, 92.6586401]}, 'Andhra Pradesh': {'coordinates': [15.9128998, 79.7399875]}, 'Arunachal Pradesh': {'coordinates': [28.2179994, 94.7277528]}, 'Assam': {'coordinates': [26.2006043, 92.9375739]}, 'Bihar': {'coordinates': [25.0960742, 85.31311939999999]}, 'Chandigarh': {'coordinates': [30.7333148, 76.7794179]}, 'Chhattisgarh': {'coordinates': [21.2786567, 81.8661442]}, 'Dadra And Nagar Haveli': {'coordinates': [20.1808672, 73.0169135]}, 'Delhi': {'coordinates': [28.7040592, 77.10249019999999]}, 'Goa': {'coordinates': [15.2993265, 74.12399599999999]}, 'Haryana': {'coordinates': [29.0587757, 76.085601]}, 'Himachal Pradesh': {'coordinates': [31.1048294, 77.17339009999999]}, 'Jammu and Kashmir': {'coordinates': [34.0233028, 75.7738873]}, 'Ladakh': {'coordinates': [34.2996176, 78.2931706]}, 'Jharkhand': {'coordinates': [23.6101808, 85.2799354]}, 'Karnataka': {'coordinates': [15.3172775, 75.7138884]}, 'Kerala': {'coordinates': [10.8505159, 76.2710833]}, 'Lakshadweep': {'coordinates': [10.3280265, 72.78463359999999]}, 'Madhya Pradesh': {'coordinates': [22.9734229, 78.6568942]}, 'Maharashtra': {'coordinates': [19.7514798, 75.7138884]}, 'Manipur': {'coordinates': [24.6637173, 93.90626879999999]}, 'Meghalaya': {'coordinates': [25.4670308, 91.366216]}, 'Mizoram': {'coordinates': [23.164543, 92.9375739]}, 'Nagaland': {'coordinates': [26.1584354, 94.5624426]}, 'Odisha': {'coordinates': [20.9516658, 85.0985236]}, 'Puducherry': {'coordinates': [11.9415524, 79.8082865]}, 'Punjab': {'coordinates': [31.1471305, 75.34121789999999]}, 'Rajasthan': {'coordinates': [27.0238036, 74.21793260000001]}, 'Sikkim': {'coordinates': [27.5329718, 88.5122178]}, 'Tamil Nadu': {'coordinates': [11.1271225, 78.6568942]}, 'Tripura': {'coordinates': [23.9408482, 91.9881527]}, 'Uttar Pradesh': {'coordinates': [26.8467088, 80.9461592]}, 'Uttarakhand': {'coordinates': [30.066753, 79.01929969999999]}, 'West Bengal': {'coordinates': [22.9867569, 87.8549755]}, 'Telengana': {'coordinates': [18.1124372, 79.01929969999999]}, 'Gujarat': {'coordinates': [22.258652, 71.1923805]}}



		for state in state_data:
			state_data[state]['weight']=0
			state_data[state]['stat']='<u>{}</u><br><br><b>NO INFO ON YET!!</b>'.format(state)



		# In[56]:




		if covid19_data['success']==True:
			for state in covid19_data['data']['regional']:
					state_data[state['loc']]['weight']=(state['confirmedCasesIndian']+state['confirmedCasesForeign'])
					state_data[state['loc']]['stat']="<u>{}</u><br><br><b>Confimed Cases Indian:</b> {}<br><br><b>Confirmed Cases Foreign:</b> {}<br><br><b>Deaths:</b> {}<br><br><b>Discharged:</b> {}".format(state['loc'],state['confirmedCasesIndian'],state['confirmedCasesForeign'],state['deaths'],state['discharged'])

		if covid19_contact['success']==True:
			for state in covid19_contact['data']['contacts']['regional']:
				if state['loc'] in state_data:
					state_data[state['loc']]['stat']+="<br><br><b>Contact Detail:</b> {}<br>".format(state['number'])

		# In[58]:


		locations=[state['coordinates'] for state in state_data.values() ]
		locations


		# In[59]:


		weights=[state['weight'] for state in state_data.values() ]
		weights


		# In[64]:


		fig = gmaps.figure(center=(23.5936832, 78.962883), zoom_level=4)
		heatmap=gmaps.heatmap_layer(locations, weights=weights)
		heatmap.point_radius=45
		fig.add_layer(heatmap)
		symbol_layer=gmaps.symbol_layer(locations,info_box_content=[state['stat'] for state in state_data.values()])
		fig.add_layer(symbol_layer)




		# In[66]:




		embed_minimal_html('./templates/export.html', views=[fig])


	def summaryData(self):
		covid19_data=requests.get('https://api.rootnet.in/covid19-in/stats/latest').json()
		if covid19_data['success']==True:
			with open('./data/data.json','w') as outputfile:
				json.dump(covid19_data,outputfile)

if '__main__'==__name__:
	createHeatMap()
	summaryData()