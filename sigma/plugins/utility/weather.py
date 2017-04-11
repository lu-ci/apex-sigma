import aiohttp
from geopy.geocoders import Nominatim
from config import DarkSkySecretKey
from humanfriendly.tables import format_pretty_table as boop


async def weather(cmd, message, args):
    if args:
        location = ' '.join(args)
    else:
        await message.channel.send(cmd.help())
        return
    try:
        try:
            geolocator = Nominatim()
            loc_element = geolocator.geocode(location)
            latitude = loc_element.latitude
            longitude = loc_element.longitude
        except Exception as e:
            cmd.log.error(e)
            await message.channel.send('Unable to retrieve coordinates for ' + location)
            return
        # Data Collection
        dark_sky_url = 'https://api.darksky.net/forecast/' + DarkSkySecretKey + '/' + str(latitude) + ',' + str(
            longitude)
        async with aiohttp.ClientSession() as session:
            async with session.get(dark_sky_url) as data:
                data = await data.json()
        try:
            today_forecast = data['hourly']['summary']
            week_forecast = data['daily']['summary']
        except:
            today_forecast = 'Nothing'
            week_forecast = 'Nothing'
        current = data['currently']
        temp_f = current['temperature']
        temp_c = (temp_f - 32) / 1.8
        try:
            feel_f = current['apparentTemperature ']
            feel_c = (feel_f - 32) / 1.8
        except:
            feel_f = temp_f
            feel_c = temp_c
        summary = current['summary']
        precip_intensity_in = current['precipIntensity']
        precip_intensity_cm = precip_intensity_in * 2.54
        precip_chance = current['precipProbability'] * 100
        try:
            precip_type = current['precipType'].title()
        except:
            precip_type = 'None'
        dew_point_f = current['dewPoint']
        dew_point_c = (dew_point_f - 32) / 1.8
        humidity = current['humidity'] * 100
        wind_speed_mph = current['windSpeed']
        wind_speed_kph = wind_speed_mph * 1.609344
        if wind_speed_mph == 0:
            wind_bearing = 0
        else:
            wind_bearing = current['windBearing']
        try:
            visibility_mi = current['visibility']
            visibility_km = visibility_mi * 1.60934
        except:
            visibility_km = 0
            visibility_mi = 0
        cloud_cover = current['cloudCover'] * 100
        pressure = current['pressure']
        ozone = current['ozone']
        # Data Output
        out_list = []

        out_list.append(['Current State', summary])
        out_list.append(['Temperature', str(format(temp_c, '.2f')) + '°C (' + str(temp_f) + '°F)'])
        out_list.append(['Feels Like', str(format(feel_c, '.2f')) + '°C (' + str(feel_f) + '°F)'])
        out_list.append(['Dew Point', str(format(dew_point_c, '.2f')) + '°C (' + str(dew_point_f) + '°F)'])
        out_list.append(['Humidity', str(humidity) + '%'])
        out_list.append(['Precipitation Type', precip_type])
        out_list.append(['Precipitation Chance', str(precip_chance) + '%'])
        out_list.append(['Precipitation Intensity',
                         str(format(precip_intensity_cm, '.2f')) + ' cmh (' + str(precip_intensity_in) + ' inh)'])
        out_list.append(['Wind Speed', str(format(wind_speed_kph, '.2f')) + ' KPH (' + str(wind_speed_mph) + ' MPH)'])
        out_list.append(['Wind Direction', str(wind_bearing) + '°'])
        out_list.append(['Visibility', str(format(visibility_km, '.2f')) + ' KM (' + str(visibility_mi) + ' MI)'])
        out_list.append(['Cloud Cover', str(cloud_cover) + '%'])
        out_list.append(['Pressure', str(pressure) + ' mb'])
        out_list.append(['Ozone Density', str(ozone)])

        out_pretty_list = boop(out_list)

        out_text = 'Weather data for **' + location.title() + '**\nLocation: *(Lat: ' + str(latitude) + ', Long: ' + str(longitude) + ')*'
        out_text += '\n```haskell\n' + out_pretty_list + '\n```'
        forecasts = '```haskell\nUpcoming: \"' + today_forecast + '\"\nThis Week: \"' + week_forecast + '\"\n```\n'
        out_text += '\nForecasts:\n' + forecasts
        await message.channel.send(out_text)
    except Exception as e:
        cmd.log.error(e)
        await message.channel.send('Error Retrieving the data.')
