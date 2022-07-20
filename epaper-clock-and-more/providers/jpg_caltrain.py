from providers.acquire import Acquire
from collections import namedtuple
import logging
import time
import gc

def time_from_str(time_str):
    time = time_str.split(':')
    try:
        pm = 0 if time[1][2:4]=='am' or int(time[0]) == 12 else 1
        hours = int(time[0])+12 if pm else int(time[0])
        minutes = int(time[1][0:2])
        # print(hours,minutes)
        return _create_time(hour=hours,minute=minutes)
    except:
        print(time)
        return _create_time()


def get_pdt():
    return time.localtime(time.mktime(time.localtime()))

_BASE_DATE = time.localtime(0)
_YEAR = 0
_MONTH  = 1
_DAY    = 2
_HOUR   = 3
_MINUTE = 4
_SECOND = 5
_WEEKDAY    = 6
_YEARDAY    = 7
def _create_time(year=None,month=None,day=None,hour=None,minute=None,second=None,weekday=None,yearday=None,dst=-1):
    curr_time = get_pdt()
    if not year : 
        _year = curr_time.tm_year
    else:
        _year = year
    if not month : 
        _month = curr_time.tm_mon
    else:
        _month = month
    if not day : 
        _day = curr_time.tm_mday
    else:
        _day = day
    if not hour : 
        _hour = curr_time.tm_hour
    else:
        _hour = hour
    if not minute : 
        _minute = curr_time.tm_min
    else:
        _minute = minute
    if not second : 
        _second = curr_time.tm_sec
    else:
        _second = second
    if not weekday : 
        _weekday = curr_time.tm_wday
    else:
        _weekday = weekday
    if not yearday : 
        _yearday = curr_time.tm_yday
    else:
        _yearday = yearday
    if not dst : 
        _dst = curr_time.dst
    else:
        _dst = dst
    
    return time.localtime(time.mktime((_year,_month,_day,_hour,_minute,_second,_weekday,_yearday,_dst)))

def _resolve_duration(start, end):
    start_time = time.mktime(start)
    end_time = time.mktime(end)
    seconds = end_time-start_time
    return seconds

caltrain_tuple = namedtuple('caltrain', ['departure_time','arrival_time','duration'])


class MicroCaltrain(Acquire):

    def __init__(self,filename="main/app/caltrain_data.csv",start='sf',end='law',walking_time=0) -> None:
        self.start = start
        self.end = end
        self.walking_time=walking_time
        self.filename=filename

    #a=start (sf,sv,law)
    #b=end (sf, sv, law)
    #direction=0/South 1/North
    #after=only get times after tuple
    #count=return n trains
    def next_trips(self, a='sf', b='law',direction=0, after=get_pdt(),count=1):
        # after = time.localtime(time.mktime(after)+(self.walking_time*60))
        trips_list = []
        with open(self.filename, "r") as csvfile:
            line=csvfile.readline().lower()
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            row =line.split(',')
            # print(row)
            dir_col = row.index("direction")
            days_col = row.index("days")
            sf_col = row.index("sf")
            sv_col = row.index("sv")
            law_col = row.index("law")

            departure_col = row.index(a)
            arrival_col = row.index(b)

            for line in csvfile:
                gc.collect()
                # line_Str=csvfile.readline()
                line=line.lower()
                line=line.rstrip('\n')
                line=line.rstrip('\r')
                row =line.split(',')
            # for Data in train_reader:
                train_dir = int(row[dir_col])
                if train_dir is not direction:
                    continue
                days=str(row[days_col])
                if str(after[_WEEKDAY]) not in days:
                    continue

                if str(row[departure_col]) == '--' or str(row[arrival_col]) == '--':
                    continue

                #if we're going south
                departure_time=time_from_str(str(row[departure_col]))
                if time.mktime(departure_time) < time.mktime(after):
                    continue
                arrival_time=time_from_str(str(row[arrival_col]))
                duration = _resolve_duration(departure_time,arrival_time)
                trips_list.append([departure_time,arrival_time,duration])
                if len(trips_list) > count-1:
                    break

        return trips_list
    def acquire(self):
        logging.info("Getting Caltrain: {} from the internet...".format(self.start))

        try:
            # r = requests.get(
            #     "https://maps.googleapis.com/maps/api/distancematrix/json?units={}&departure_time=now&origins={},{}&destinations={},{}&mode={}&transit_mode={}&transit_routing_preference={}&key={}".format(
            #         self.units,
            #         self.home_lat,
            #         self.home_lon,
            #         self.dest_lat,
            #         self.dest_lon,
            #         self.mode,
            #         self.mode_pref,
            #         self.route_pref,
            #         self.key
            #     ),
            # )
            if self.start.lower() == 'sf':
                direction = 0
            else:
                direction = 1
            after = time.localtime(time.mktime(get_pdt()) + self.walking_time*60)
            next_trips = self.next_trips(a=self.start,b=self.end,direction=direction,after=after)
            
            return caltrain_tuple(
                departure_time=next_trips[0][0],
                arrival_time=next_trips[0][1],
                duration=next_trips[0][2],
                )
            return r.status_code, r.text
        except Exception as e:
            logging.exception(e)

        return (None, None)

    def get(self):
        caltrain_data= self.load()
        print(caltrain_data)
        if caltrain_data is None:
            return (0,0,0)
        else:
            return caltrain_data