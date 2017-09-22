from crawler import JsonCrawler


class WeatherForecast:
    # TODO: implement
    def __init__(self, locations, notifications):
        self.locations = locations
        self.notifications = notifications

    def run(self):
        while True:
            for location in self.locations:
                JsonCrawler('https://www.metaweather.com/api/location/search/?query=%s' % location, location)
                woeid = JsonCrawler.get_by_name(location).get_data()[0]["woeid"]
                JsonCrawler('https://www.metaweather.com/api/location/%s' % woeid, location, active=True)
                weather = JsonCrawler.get_by_name(location).get_data()['consolidated_weather'][3]
                for notification in self.notifications:
                    if notification[0] == 'Light Cloud' and notification[1](weather["weather_state_name"]):
                        print("Light cloud in %s" % location)
                    if notification[0] == 'Ice age' and notification[1](weather["min_temp"]):
                        print("Ice age in %s" % location)



if __name__ == '__main__':
    forecast = WeatherForecast(['seoul', 'new york'],# 1132599, https://www.metaweather.com/api/location/2459115/
                            [('Light Cloud',lambda weather:weather == "Light Cloud"),('Ice age',lambda min_temp:min_temp < -30)])
        # TODO: set two conditions:
        # 1. 'Light cloud' : True if weather state contains light cloud
        # 2. 'Ice age' : True if minimum temperature is lower than -30 (degrees celsius)

    forecast.run()
