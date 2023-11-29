#!/usr/bin/python

import logging
from waveshare_epd import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont
import time

import logging
import json
import urllib.request
import netifaces as ni


logging.basicConfig(level=logging.DEBUG)

SERVICES = {
    'ZAW': 'zaw',
}

class JumomindAbfallApi(object):
    def __init__(self, service):
        self.service = service
        self.base_url = 'https://{}.jumomind.com/mmapp/api.php'.format(self.service)

    def _request(self, endpoint):
                return urllib.request.urlopen(self.base_url + endpoint)

    def get_dates(self, city_id, area_id):
        return self._request('?r=dates/0&city_id={}&area_id={}'.format(city_id, area_id))


def main():
    
    epd = epd2in13_V2.EPD()
    logging.info("init")
    epd.init(epd.FULL_UPDATE)
	
    api = JumomindAbfallApi(SERVICES['ZAW'])
    city_id = xx  
    area_id = xxx 

    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    
    logging.info('Getting list of DATES')
    with api.get_dates(city_id, area_id) as resp:
        print('DATES:')
        try:
            dates = json.loads(resp.read().decode())
            var_1=dates[0]
            var_2=dates[1]
            var_3=dates[2]
        except Exception as e:
            logging.error('Failed to get list of DATES, Msg: {}'.format(e))
            sys.exit(3)
            


    
    image = Image.new('1', (epd2in13_V2.EPD_HEIGHT,epd2in13_V2.EPD_WIDTH), 255)  
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('fonts/Roboto-Thin.ttf', 14)
    font2 = ImageFont.truetype('fonts/DroidSans.ttf', 13)
    font3 = ImageFont.truetype('fonts/Roboto-Light.ttf', 10)
    font4 = ImageFont.truetype('fonts/Roboto-Thin.ttf', 12)
    font5 = ImageFont.truetype('fonts/Verdana_Bold.ttf', 20)

    draw.rectangle((0, 0, 250, 35), fill = 0)
    draw.text((5, 5), 'Abfall Calendar', font = font5, fill = 255)

    start_y = 35
    offset_y_1 = 20
    offset_y_2 = 45 
    
    day1 = var_1['day'], '->', var_1['title']


    draw.text((0, start_y), ('{:5.10s}'.format(var_1['day'])), font=font2) 
    draw.text((25, 48), ('{:5.50s}'.format(var_1['title'])), font=font2)

    draw.text((0, 61), ('{:5.10s}'.format(var_2['day'])), font=font2)
    draw.text((25, 74), ('{:5.50s}'.format(var_2['title'])), font=font2)

    draw.text((0, 87), ('{:5.10s}'.format(var_3['day'])), font=font2)
    draw.text((25, 100), ('{:5.50s}'.format(var_3['title'])), font=font2)

    current_time = time.strftime("%H:%M:%S, %d.%m.%Y")
    draw.text((6, 111), current_time + ' IP: ' + ip, font=font3)

    logging.info("clear and display the results")
    epd.Clear(0xFF)
    epd.display(epd.getbuffer(image.rotate(180,expand=True)))
    epd.sleep()
    
if __name__ == '__main__':
    main()

