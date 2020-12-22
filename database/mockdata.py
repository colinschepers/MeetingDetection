import sqlalchemy as db
from datetime import datetime
from database.models import User, Event


data = """
39.984611,116.318026,0,493,39744.1204861111,2008-10-23,02:53:30
39.984563,116.317517,0,496,39744.1206018519,2008-10-23,02:53:40
39.984606,116.317065,0,505,39744.1207175926,2008-10-23,02:53:50
39.984586,116.316716,0,515,39744.1208333333,2008-10-23,02:54:00
39.984536,116.316354,0,525,39744.1209490741,2008-10-23,02:54:10
39.984516,116.315963,0,536,39744.1210648148,2008-10-23,02:54:20
39.984574,116.315611,0,546,39744.1211805556,2008-10-23,02:54:30
39.984538,116.315148,0,556,39744.1212962963,2008-10-23,02:54:40
39.984532,116.314808,0,564,39744.1214120373,2008-10-23,02:54:50
39.984696,116.312921,0,144,39744.1222222222,2008-10-23,02:56:00
"""


def create_mockdata():
    user = User()
    db.session.add(user)
    db.session.flush()

    for line in data.split('\n'):
        split = line.split(',')
        lat, lon = float(split[0]), float(split[1])
        timestamp = datetime.strptime(split[-1], "%Y-%m-%d %H:%M:%S").timestamp()
        event = Event(user_id=user.id, lat=lat, lon=lon, timestamp=timestamp)
        db.session.add(event)

    db.session.commit()