import click
import requests
from datetime import datetime, timedelta
from dateutil import tz
from random import randint
import time

cookie = {"session": "53616c7465645f5fff514c2fe2c2ddedeb488339fea876f6aa44575f533923ae8d78c42b39bbbdf5686e01d3c40a8798"}

def get_default_day():
    t = datetime.now(tz=tz.gettz('America/New_York'))
    if t.year == 2020 and t.month == 12:
        if t.hour >= 21:
            return t.day + 1
        else:
            return t.day
    return None

@click.command()
@click.option("--day", help="Day to download input of", default=get_default_day, type=int)
@click.option("--year", default=2020, help="Year to download from")
@click.option("--delay", default=lambda: randint(10, 40), help="Delay after midnight to wait")
def download(day, year, delay):
    print(f"Saw {day!r}, {year!r}, {delay!r}")
    EST = tz.gettz('America/New_York')
    grab_time = datetime(year, 12, day, 0, 0, delay, randint(0, 500000), tzinfo=EST)

    while (delta := (grab_time - datetime.now(tz=EST))) > timedelta(seconds=0):
        if delta > timedelta(days=1):
            print("Need to wait >1 day...")
            time.sleep(3600) # 1 hour
        elif delta > timedelta(hours=1):
            time.sleep(1800) # 1/2 hour
        elif delta > timedelta(minutes=1):
            time.sleep(delta.seconds * 2 // 3)
        elif delta > timedelta(seconds=2):
            time.sleep(delta.seconds / 3)
        elif delta >= timedelta(milliseconds=10):
            time.sleep(delta.microseconds / 1050000) # 5% margin
        # else: pass # busyloop

    response = requests.get(f"https://adventofcode.com/{year}/day/{int(day)}/input", cookies=cookie)

    with open(f"inputs/d{day:02d}.txt", "wb") as f:
        f.write(response.content)

    response.close()

if __name__ == "__main__":
    download()
