

from datetime import datetime, timedelta
from time import time
from dateutil import parser
import logging
from providers.acquire import Acquire
from collections import namedtuple
import requests

CalEventTuple = namedtuple('calEvent', ['title','start_time','is_allday'])

class CalendarEvents(Acquire):
    DEFAULT=None #CalEventTuple(title='',start_time=None,is_allday=False)
    def __init__(self,cal_url:str,timeframe) -> None:
        self.cal_url =cal_url
        self.timeframe = int(timeframe)
        pass

    def cache_name(self):
        return "cal_events"

    def acquire(self):
        pass 
        r = requests.get(
            self.cal_url
            )
        # print(r.text)
        # print("events[0]",r.json()['events'][0])
        return r.status_code,r.text

    def get(self):
        try:
            cal_data = self.load()
            # print("cal_data: ",cal_data)
            if cal_data is None or cal_data['events'][0] is None:
                return self.DEFAULT
            next_events= []
            for event in cal_data['events']:
                start_time = parser.parse(event['start_time'])-timedelta(hours=7)
                start_time = start_time.replace(tzinfo=None)
                time_until = ((start_time-datetime.today()).total_seconds() // 60)
                allday = event['is_allday']
                # print("start time",start_time)
                # print("today: ",datetime.today())
                # print("difference: ",time_until)
                # print("time until ",event['title'],": ",(time_until))
                if not allday:
                    if (time_until) < self.timeframe and time_until > -10:
                        next_events.append(CalEventTuple(title=event['title'],start_time=start_time,is_allday=allday))
                else:
                    if time_until < (24*60) and time_until > (-1 * (15*60)):
                        next_events.append(CalEventTuple(title=event['title'],start_time=start_time,is_allday=allday))
                        
                
            return next_events
        
        except Exception as e:
            logging.exception(e)
            return self.DEFAULT

        pass


# cal.acquire()