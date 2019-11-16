from pyowm import OWM
import tweepy
import schedule
import time
import config    #seperate config file

def get_weather_query(owm):
    """Takes the owm auth and returns the weather object at a given location."""

    city_id = 4068590   #Currently Huntsville, AL
    obs = owm.weather_at_id(city_id)
    w = obs.get_weather()
    return w

def initTweepy():
    """Initializes the Twitter authorization."""

    #OAth config
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    #OAth process
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #Interface creation
    return tweepy.API(auth)

def write_to_dict(forecast):
    """Takes the forecast object and returns a dictionary of the important data."""

    weather_dict = {}

    weather_dict.update({'temp_current':forecast.get_temperature('fahrenheit')})
    # humidity
    weather_dict.update({'humidity':forecast.get_humidity})
    # wind_speed
    weather_dict.update({'wind':forecast.get_wind('miles_hour')})
    # pressure
    weather_dict.update({'pressure':forecast.get_pressure()})
    #weather_description
    weather_dict.update({'weather_desc':forecast.get_detailed_status()})
    return weather_dict

def write_tweet_string(weather_dict=dict):
    """Takes the weather dictionary and returns the tweet string."""

    temp_string = weather_dict['temp_current']['temp']

    wind_string = weather_dict['wind']['speed']
    wind_dir_string = convert_headings(weather_dict['wind']['deg'])
    pressure_string = weather_dict['pressure']['press']
    weather_desc_string = weather_dict['weather_desc']

    tweet_string = "The temperature is " + str(temp_string) + "F and the wind is blowing at " + str(round(wind_string, 2)) + "mph from the " + str(wind_dir_string) + " (" + str(round(weather_dict['wind']['deg'], 2)) + "°). The pressure is " + str(pressure_string) + "mb. The weather can be described as '" + str(weather_desc_string) + ".'"
    return tweet_string

def convert_headings(wind_heading=int):
    """Takes a degree input and returns a compass direction."""

    headings = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
    wind_heading = wind_heading % 360
    index = round(wind_heading/ 22.5)
    return headings[index]

def setup_forecast():
    return get_weather_query(owm)

#openweathermap key
OWM_API_key = config.OWM_API_key
owm = OWM(OWM_API_key)

#initialize Tweepy authentication
tweepy_api = initTweepy()

forecast = setup_forecast()

weather_dict = write_to_dict(forecast)
print(write_tweet_string(weather_dict))

username = config.username
tweet_string = write_tweet_string(weather_dict)
tweepy_api.update_status(username + ' ' + tweet_string)