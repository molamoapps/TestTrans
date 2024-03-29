# -*- coding: utf-8 -*-
# MTR Bus fetching

import csv
import requests
import json

routeList = {}
stopList = {}

r = requests.get('https://opendata.mtr.com.hk/data/mtr_bus_routes.csv')
r.encoding = 'utf-8'
reader = csv.reader(r.text.split("\n") )
headers = next(reader,None)
routes = [route for route in reader if len(route) == 4]
for [route, chn, eng, circular] in routes:
  print ("info", chn.split('至'))
  if route == '':
    continue;
  start = {
    "zh": chn.split('至')[0],
    "en": eng.split(' to ')[0]
  }
  end = {
    "zh": chn.split('至')[1],
    "en": eng.split(' to ')[1]
  }
  for bound in ['I', 'O']:
    routeList[route+"_"+bound] = {
      "co": "mtrbus",
      "route_id": "",
      "route": route,
      "bound": bound,
      "service_type": "1",
      "orig_tc": start['zh'] if bound == 'O' else end['zh'],
      "orig_sc": start['zh'] if bound == 'O' else end['zh'],
      "dest_tc": end["zh"] if bound == 'O' else start['zh'],
      "dest_sc": end["zh"] if bound == 'O' else start['zh'],
      "orig_en": start['en'] if bound == 'O' else end['en'],
      "dest_en": end["en"] if bound == 'O' else start['en'],
      "stops": []
    }

# Parse stops
r = requests.get('https://opendata.mtr.com.hk/data/mtr_bus_stops.csv')
reader = csv.reader(r.text.split("\n") )
headers = next(reader,None)
stops = [stop for stop in reader if len(stop) == 8]
for [route, bound, seq, stationId, lat, lng, name_zh, name_en] in stops:
  routeKey = route+"_"+bound
  if routeKey in routeList:
    routeList[routeKey]['stops'].append(stationId)
  else:
    print ("error", routeKey)
  stopList[stationId] = {
    "stop": stationId,
    "name_en": name_en,
    "name_tc": name_zh,
    "name_sc": name_zh,
    "lat": lat,
    "long": lng,
    "routes": []
  }
  
# flatten the routeList back to array
routeList = [routeList[routeKey] for routeKey, route in routeList.items() if len(route['stops']) > 0]
    
    
#loop stoplist to get contained routes
for key, stopMod in stopList.items():
    tmpContainRoute = []
    for routeMod in routeList:
        if stopMod['stop'] in routeMod['stops']:
            tmpSeq = routeMod['stops'].index(stopMod['stop'])
            tmpRoute = {}
            tmpRoute['ID'] = ('%s%s%s%s'%(routeMod['co'], routeMod['route'], routeMod['bound'], routeMod.get('service_type', '1')))
            tmpRoute['i'] = tmpSeq
            tmpContainRoute.append(tmpRoute)
            #tmpContainRoute.append(routeMod['route'])
    stopMod['routes'] = tmpContainRoute

    
with open('routeList.mtrbus.json', 'w') as f:
  f.write(json.dumps(routeList, ensure_ascii=False))
#   f.write(json.dumps([route for route in routeList.values() if len(route['stops']) > 0], ensure_ascii=False))
with open('stopList.mtrbus.json', 'w') as f:
  f.write(json.dumps(stopList, ensure_ascii=False))
