from __future__ import print_function
from bs4 import BeautifulSoup
import urllib2
from threading import Thread
import time
import sys
import datetime
from datetime import date
from datetime import timedelta
import getopt
import os

def getAva(rooms, roomName, start, end):
  for i in range(start, end):
    url = 'https://ca.evanced.info/ucsd/lib/roomrequest.asp?command=getResultWin&vm=d&res=&SelectedDate={}&room={}&pointer=&rowchange=&entitytype=0&LangType=0&mm=1&timestamp=1426185127174'.format(date, rooms[i])
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    arr = soup.find_all("td",{"class":"list_light"})
    # result = []
    index = 1
    while index < len(arr):
      time = arr[index].span.contents[0].encode('ascii','ignore')
      # print(time)
      if time in output.keys():
        output[time].append(roomName[i])
      else:
        output[time] = [roomName[i]]
      index += 3
  sys.stderr.write(".")
    # output[roomName[i]] = result

def resolveOpt(argv):
  options, remainder = getopt.getopt(argv[1:], 'hs:e:d:')
  start, end, days, help = None, None, None, 0
  for opt, arg in options:
    if opt == '-s':
      start = arg
    elif opt == '-e':
      end = arg
    elif opt == '-d':
      days = arg
    elif opt == '-h':
      help = 1
    else:
      print("invalid options neglected")
  return((start, end, days, help))

def printGeisel(output, start, end):
  for interval in formatedInterval(start, end):
    print("{:>18} : {}".format(interval, output.get(interval, [])))

def getDate(days):
  if days == None:
    day = 0
  elif days == 't':
    day = 1
  else:
    day = 2
  return (date.today() + timedelta(days=day)).strftime("%m/%d/%Y")

def process(intervalArr, hour):
  for i in range(len(intervalArr)):
    if decodeHour(intervalArr[i].split("-")[0]) < hour:
      intervalArr[i] = ""

def decodeHour(stringTime):
  time, part = stringTime.split()
  base = 0 if part == "AM" else 12
  hour = int(time.split(":")[0])%12
  return (hour+base)

def formatedInterval(start , end):
  start = 8 if start == None else int(start)
  end = 23 if end == None else int(end)
  array = []
  while start < end:
    pre = start % 12
    if pre == 0: pre += 12
    preZ = "AM" if start < 12 else "PM"
    pos = (start+1) % 12
    if pos == 0: pos += 12
    posZ = "AM" if (start+1) < 12 else "PM"
    array.append("{}:00 {}-{}:30 {}".format(pre, preZ, pre, preZ))
    array.append("{}:30 {}-{}:00 {}".format(pre, preZ, pos, posZ))
    start += 1
  return array

def main():
  print("Searching")
  interval = len(rooms)/numThread
  i = 0
  thread = None
  while i < numThread:
    thread = Thread(target = getAva, args = (rooms, roomName, i*interval, (i+1)*interval))
    thread.start()
    i += 1
  thread.join()
  thread = Thread(target = getAva, args = (rooms, roomName, i*interval, len(rooms)))
  thread.start()
  thread.join()
  print("")
  printGeisel(output, start, end)

if __name__ == "__main__":
  hour = datetime.datetime.now().time().hour
  rooms = [4, 5, 56, 57] + list(range(81, 87)) + list(range(58, 64)) + list(range(94, 100))
  roomName = [518, 519, 521, 522] + list(range(618, 621)) + list(range(622, 628)) + list(range(629, 632)) + list(range(718, 721)) + list(range(722, 725))
  output = {}
  numThread = 7
  (start, end, days, help) = resolveOpt(sys.argv)
  if help == 1:
    print("###===###===###===###===###===###===###===###===###===###===###===###===###===###===###===###===###")
    print("#                                                                                                 #")
    print("#  Dear Darling Mandy,                                                                            #")
    print("#                                                                                                 #")
    print("#    Welcome to geisel reserve lookup system, available options are listed as follows:            #")
    print("#      -s to indicate start hour, e.g 9                                                           #")
    print("#      -e to indicate end hour, e.g. 15                                                           #")
    print("#        notice that the start and end hour should range from 8 to 23                             #")
    print("#      -d to indicate day, today would be default if no -d option included                        #")
    print("#        otherwise '-d t' to indicate tomorrow, '-d tt' to indicate the day after tomorrow        #")
    print("#    Thus '$geisel -s 11 -e 15 -d t' would check available room from 11AM to 3PM for tomorrow     #")
    print("#                                                                                                 #")
    print("#                                       Enjoy!                                                    #")
    print("#                                                                                                 #")
    print("#                                                                              Love,              #")
    print("#                                                                                J                #") 
    print("#                                                                                                 #")
    print("###===###===###===###===###===###===###===###===###===###===###===###===###===###===###===###===###")
  else:
    date = getDate(days)
    main()
    print("........")
    yes = raw_input("Reserve Now?   y/n\n")
    if yes == 'y':
      os.system("open https://ca.evanced.info/ucsd/lib/roomrequest.asp?mm=1")
    else:
      print("Land of Sincere, Ocean of Tender, Valley of Dearth, End of Loss")