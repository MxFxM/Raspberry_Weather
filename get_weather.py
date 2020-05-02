import configparser
import requests
import sys
from influxdb import InfluxDBClient
 
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']
 
def get_weather(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    r = requests.get(url)
    return r.json()

def get_body(weather):
    json_body = [{"measurement": "Oberderdingen",
                  "fields": {
                      "Temperature": weather['main']['temp'],
                      "Pressure": weather['main']['pressure'],
                      "Humidity": weather['main']['humidity'],
                      "Windspeed": weather['wind']['speed'],
                      "Winddirection": weather['wind']['deg'],
                      "Clouds": weather['clouds']['all']
                      }
                }]
    return json_body
 
def main():
    location = ""
    if len(sys.argv) != 2:
        #exit("Usage: {} LOCATION".format(sys.argv[0]))
        location = "Oberderdingen" # use this if no location given
    else:
        location = sys.argv[1]
 
    api_key = get_api_key()
    weather = get_weather(api_key, location)
 
    #print(weather['main']['temp'])
    print(weather)

    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'WEATHER')
    client.write_points(get_body(weather))
 
 
if __name__ == '__main__':
    main()
