import csv
import requests
import json
from pyproj import Transformer
import time

def emitRequest(url):
  # retry if "Too many request (429)"
  while True:
    r = requests.get(url)
    if r.status_code == 200:
      return r
    elif r.status_code == 429:
      time.sleep(1)
    else:
      raise Exception(r.status_code, url)
      

epsgTransformer = Transformer.from_crs('epsg:2326', 'epsg:4326')

routeList = {}
stopList = {}

r = requests.get('https://opendata.mtr.com.hk/data/light_rail_routes_and_stops.csv')
reader = csv.reader(r.text.split("\n") )
headers = next(reader,None)
routes = [route for route in reader if len(route) == 7]
for [route, bound, stopCode, stopId, chn, eng, seq] in routes:
  if route+"_"+bound not in routeList:
    routeList[route+"_"+bound] = {
      "co": "lr",
      "route_id": "",
      "route": route,
      "bound": "O" if bound == "1" else "I",
      "service_type": "1",
      "orig_tc": None,
      "orig_en": None,
      "orig_sc": None,
      "dest_tc": None,
      "dest_en": None,
      "dest_sc": None,
      "stops": [],
      "fare": []
    }
  if seq == "1.00":
    routeList[route+"_"+bound]["orig_tc"] = chn
    routeList[route+"_"+bound]["orig_en"] = eng
    routeList[route+"_"+bound]["orig_sc"] = chn
  routeList[route+"_"+bound]["dest_tc"] = chn
  routeList[route+"_"+bound]["dest_en"] = eng
  routeList[route+"_"+bound]["dest_sc"] = chn
  routeList[route+"_"+bound]["stops"].append("LR"+stopId)
  if "LR"+stopId not in stopList:
    r = requests.get('https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=輕鐵－'+chn, headers={'Accept': 'application/json'})
    lat, lng = epsgTransformer.transform( r.json()[0]['y'], r.json()[0]['x'] )
    stopList["LR"+stopId] = {
      "stop": "LR"+stopId,
      "name_en": eng,
      "name_tc": chn,
      "name_sc": chn,
      "lat": lat,
      "long": lng,
      "routes": []
    }

    
#loop stoplist to get contained routes
for key, stopMod in stopList.items():
  tmpContainRoute = []
  for routeMod in routeList:
    if stopMod['stop'] in routeMod['stops']:
      tmpSeq = routeMod['stops'].index(stopMod['stop'])
      tmpRoute = {}
      tmpRoute['ID'] = ('%s%s%s%s%s'%(routeMod['co'], routeMod['route_id'],  routeMod['route'], routeMod['bound'], routeMod.get('service_type', '1')))
      tmpRoute['i'] = tmpSeq
      tmpContainRoute.append(tmpRoute)
  stopMod['routes'] = tmpContainRoute
    
    

with open('routeList.lr.json', 'w') as f:
  f.write(json.dumps([route for route in routeList.values() if len(route['stops']) > 0], ensure_ascii=False))
with open('stopList.lr.json', 'w') as f:
  f.write(json.dumps(stopList, ensure_ascii=False))

 
