import datetime


def compare_datetime(origin: datetime, from_dt: datetime=None, to_dt: datetime=None):
    from_succ = True
    to_succ = True
    if from_dt is not None:
        if origin >= from_dt:
            from_succ = True
        else:
            from_succ = False
    if to_dt is not None:
        if origin <= to_dt:
            to_succ = True
        else:
            to_succ = False
    
    return from_succ & to_succ

def day_of_year_to_date(year: str, day_num: str):
    # Initializing start date 
    strt_date = datetime.date(int(year), 1, 1) 
    
    # converting to date 
    res_date = strt_date + datetime.timedelta(days=int(day_num) - 1) 
    res = res_date.strftime('%Y-%m-%d') 
    
    return res