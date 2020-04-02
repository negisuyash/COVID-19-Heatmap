# import gmaps
# import gmaps.datasets# Use google maps api
# gmaps.configure(api_key='AIzaSyBx1SkG_lcKjI1HJ2cyRDMTnS1k9j0LxpU') # Fill in with your API key# Get the dataset
# earthquake_df = gmaps.datasets.load_dataset_as_df('earthquakes')#Get the locations from the data set
# locations = earthquake_df[['latitude', 'longitude']]#Get the magnitude from the data
# weights = earthquake_df['magnitude']#Set up your map
# fig = gmaps.figure()
# fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
# fig

import requests

class InternalDataAPI:

    def fetchData(self):

        data=requests.get('https://api.rootnet.in/covid19-in/unofficial/covid19india.org').json()

        dataState={}
        for i in data['data']['rawPatientData']:
            if i['state'] in dataState:
                # print('under first condition')
                if i['status'] in dataState[i['state']]:
                    # print('adding new data point in '+i['state']+' under '+i['status'])
                    if i['nationality'] ==[]:
                        dataState[i['state']]['confirmedCasesIndian'][i['status']].append(i)
                    else:
                        dataState[i['state']]['confirmedCasesForeign'][i['status']].append(i)
                else:
                    # print('creating new data point in '+i['state']+' under '+i['status'])
                    if i['nationality'] == []:
                        dataState[i['state']]['confirmedCasesIndian'][i['status']]=[i]
                    else:
                        dataState[i['state']]['confirmedCasesForeign'][i['status']] = [i]
            else:
                dataState[i['state']]={'confirmedCasesIndian':{},'confirmedCasesForeign':{}}
                if i['nationality'] == []:
                    dataState[i['state']]['confirmedCasesIndian'][i['status']]=[i]
                else:
                    dataState[i['state']]['confirmedCasesForeign'][i['status']] = [i]
                # print('creating and adding new data point in ' + i['state'] + ' under ' + i['status'])
            print(dataState)

        return dataState

    def convertToConsumedJSON(self,dataState):
        confirmedCasesIndian=0
        confirmedCasesForeign=0
        discharged=0
        deaths=0
        regional=[]
        for state in dataState:
            stateConfirmedCasesIndian=0
            stateConfirmedCasesForeign=0
            stateDischarged=0
            stateDeath=0
            if 'Hospitalized' in dataState[state]['confirmedCasesIndian']:
                stateConfirmedCasesIndian+=len(dataState[state]['confirmedCasesIndian']['Hospitalized'])
                confirmedCasesIndian+=stateConfirmedCasesIndian
            if 'Hospitalized' in dataState[state]['confirmedCasesForeign']:
                stateConfirmedCasesForeign+=len(dataState[state]['confirmedCasesForeign']['Hospitalized'])
                confirmedCasesForeign+=stateConfirmedCasesForeign
            if 'Recovered' in dataState[state]['confirmedCasesIndian']:
                stateDischarged+=len(dataState[state]['confirmedCasesIndian']['Recovered'])
            if 'Recovered' in dataState[state]['confirmedCasesForeign']:
                stateDischarged += len(dataState[state]['confirmedCasesIndian']['Recovered'])
            discharged+=stateDischarged
            if 'Deceased' in dataState[state]['confirmedCasesIndian']:
                stateDeath+=len(dataState[state]['confirmedCasesIndian']['Deceased'])
            if 'Deceased' in dataState[state]['confirmedCasesForeign']:
                stateDeath += len(dataState[state]['confirmedCasesForeign']['Deceased'])
            deaths+=stateDeath
            print("confirmedCasesIndian:"+str(confirmedCasesIndian)+"\nconfirmedCasesForeign:"+str(confirmedCasesForeign)+"\ndischarged:"+str(discharged)+"\ndeaths:"+str(deaths))
            regional.append({'loc':state,'confirmedCasesIndian':stateConfirmedCasesIndian,'confirmedCasesForeign':stateConfirmedCasesForeign,'discharged':stateDischarged,'deaths':stateDeath})

        total=confirmedCasesIndian+confirmedCasesForeign

        responseJSON={'success':True,'data':{'summary':{'total':total,'confirmedCasesIndian':confirmedCasesIndian,'confirmedCasesForeign':confirmedCasesForeign,'deaths':deaths},'regional':regional}}



        return  responseJSON

if __name__=='__main__':
    print(InternalDataAPI().convertToConsumedJSON(InternalDataAPI().fetchData()))