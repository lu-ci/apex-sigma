import requests

from config import OpenWeatherMapKey as owm_key


async def weather(cmd, message, args):
    if args and args[0] and args[1]:
        city = args[0].rstrip(',')
        country = args[1]
    else:
        cmd.reply(cmd.help())
        return

    owm_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&appid=' + owm_key
    owm_json = requests.get(owm_url).json()
    kelvin = 273.16

    try:
        coord_lon = str(owm_json['coord']['lon'])
        coord_lat = str(owm_json['coord']['lat'])
        sys_country = str(owm_json['sys']['country'])
        sys_city = str(owm_json['name'])
        weather = str(owm_json['weather'][0]['main'])
        temp = (str(round(owm_json['main']['temp'] - kelvin)) + '°C')
        temp_f = (str(round((((owm_json['main']['temp'] - kelvin) * 9) / 5) + 32)) + '°F')
        humidity = (str(owm_json['main']['humidity']) + '%')
        pressure = (str(owm_json['main']['pressure']) + ' mb')
        temp_min_c = (str(round(owm_json['main']['temp_min'] - kelvin)) + '°C')
        temp_max_c = (str(round(owm_json['main']['temp_max'] - kelvin)) + '°C')
        temp_min_f = (str(round((((owm_json['main']['temp_min'] - kelvin) * 9) / 5) + 32)) + '°F')
        temp_max_f = (str(round((((owm_json['main']['temp_max'] - kelvin) * 9) / 5) + 32)) + '°F')

        if weather == 'Thunderstorm':
            icon = ':thunder_cloud_rain:'
        elif weather == 'Drizzle':
            icon = ':cloud:'
        elif weather == 'Rain':
            icon = ':cloud_rain:'
        elif weather == 'Snow':
            icon = ':cloud_snow:'
        elif weather == 'Clear':
            icon = ':sunny:'
        elif weather == 'Clouds':
            icon = ':white_sun_cloud:'
        elif weather == 'Extreme':
            icon = ':cloud_tornado:'
        else:
            icon = ':earth_americas:'

        weather_message = ('Weather in `' + sys_city + ', ' + sys_country + '` ' +
                           'Lat: `' + coord_lat + '` | Lon: `' + coord_lon + '`\n\n' +
                           'Current State: `' + weather + '` ' + icon + '\n\n' +
                           'Details:\n```Current: ' + temp + ' (' + temp_f + ')\n' +
                           'High: ' + temp_max_c + ' (' + temp_max_f + ')\n' +
                           'Low: ' + temp_min_c + ' (' + temp_min_f + ')\n' +
                           'Humidity: ' + humidity + '\nPressure: ' + pressure + '\n```')
        await cmd.reply(weather_message)
    except:
        try:
            owm_error_code = str(owm_json['cod'])
            if owm_error_code == '404':
                await cmd.reply('Error: Requested location not found!')
        except:
            await cmd.reply('Something went wrong, and we don\'t know what!')
