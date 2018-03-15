import pyowm
def getWeather(location):
        OWM_KEY=''
        owm = pyowm.OWM(OWM_KEY)
    	weather = owm.weather_at_place(location).get_weather()
    	temperatures = weather.get_temperature(unit='celsius')
    	weather = {}
    	weather['currentTemperature'] = temperatures['temp']
    	weather['minTemperature'] = temperatures['temp_min']
    	weather['maxTemperature'] = temperatures['temp_max']
    	return weather
