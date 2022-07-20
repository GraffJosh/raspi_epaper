

from datetime import datetime
import logging
from providers.acquire import Acquire
from collections import namedtuple
import requests

CalEventTuple = namedtuple('calEvent', ['title','start_time','is_allday'])

class CalendarEvents(Acquire):
    DEFAULT=CalEventTuple(title='',start_time=None,is_allday=False)
    def __init__(self) -> None:
        pass

    def cache_name(self):
        return "cal_events"

    def acquire(self):
        pass 
        r = requests.get(
            "https://script.google.com/macros/s/AKfycbwa8cPXWmKFQPSh8Fb_BDiJ2ti70Ef7_-T0-PnGYKmG4uBxC7w9b92RQB7Kfe60aHOD/exec",
            )
        print(r.text)
        print("events[0]",r.json()['events'][0])
        return r.status_code,r.text

    def get(self):
        try:
            cal_data = self.load()
            print("cal_data: ",cal_data)
            if cal_data is None or cal_data['events'][0] is None:
                return self.DEFAULT
            next_events= []
            for event in cal_data['events']:
                start_time = datetime.strptime(event['start_time'],)
                allday = event['is_allday']
                print("start time",start_time)
                next_events.append(CalEventTuple(title=event['title'],start_time=start_time,is_allday=allday))
                
            return next_events
        
        except Exception as e:
            logging.exception(e)
            return self.DEFAULT

        pass

cal = CalendarEvents()
cal.get()
# cal.acquire()