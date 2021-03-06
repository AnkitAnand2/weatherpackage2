
import pandas as pd
import requests
import concurrent.futures

def api_call(city):
    """
    Using API Call to load the weather data into a json format
    """
    
    exception_not_happened = True
    try:
        url='http://api.openweathermap.org/data/2.5/forecast?units=metric&appid=5f1aaab27154e9d7a4c6e81336e9266a&q='

        resurl = url + city

        weather=requests.get(resurl).json()
        
        # Check if we had a failure (the forecast will fail in the same way).
        if weather['cod'] != '200':
            raise Exception(weather['message'])
    except Exception as e:
        exception_not_happened = False
        print ("Error in Argument:",e.args[0])
        
    if exception_not_happened:
        return weather
    
def weathercall(weather):
    
    """ 
    Converting the json data receined from the API call to Pandas Dataframe for proper visualization.
    """
    
    if weather:
        ls={}
        for x in range(len(weather.get('list'))):
            ls[weather.get('list')[x].get('dt_txt')]=[weather.get('list')[x].get('main').get('temp'),
                                                      weather.get('list')[x].get('main').get('feels_like'),
                                                      weather.get('list')[x].get('main').get('temp_min'),
                                                      weather.get('list')[x].get('main').get('temp_max'),
                                                      weather.get('list')[x].get('main').get('pressure'),
                                                      weather.get('list')[x].get('main').get('sea_level'),
                                                      weather.get('list')[x].get('main').get('humidity'),
                                                      weather.get('list')[x].get('weather')[0].get('main'),
                                                      weather.get('list')[x].get('weather')[0].get('description'),
                                                      weather.get('list')[x].get('clouds').get('all'),
                                                      weather.get('list')[x].get('wind').get('speed'),
                                                      weather.get('list')[x].get('visibility'),
                                                      weather.get('list')[x].get('rain')]

        col_name=['Temp','Feels_Like','Temp_Min','Temp_Max','Pressure','Sea_Level','Humidity','Weather_Con',
                      'Description','Clouds','Wind_Speed','Visibility','Rain']
        df= pd.DataFrame(ls)
        df_t=df.T
        df_t.columns=col_name
        df_t.fillna('Not Available',inplace=True)
        return df_t
    
    
def forecast():
    """
    Running two threads one for the main function and 
    other for the API call
    With Proper synchronization
    """
    
    print("Welcome to the Weather Forecasting Platform")
    city=input("Enter the City Name you want the forecast for: ")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(api_call, city)
        weather = future.result()
    result_forecast = weathercall(weather)
    print(result_forecast)





