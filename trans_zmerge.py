import json
from haversine import haversine, Unit

routeList = []
stopList = {}
stopMap = {}

def getRouteObj ( route, co, stops, bound, orig, dest, seq, fares, faresHoliday, freq, jt, nlbId, gtfsId, serviceType = '1'):
  return {
    'co': co,
    'route': route,
    'bound': bound,
    'service_type': serviceType,
    'stops': stops,
    'orig': orig,
    'dest': dest,
    'fares': fares,
    'faresHoliday': faresHoliday,
    #'freq': freq,
    #'jt': jt,
    #'nlbId': nlbId,
    #'gtfsId': gtfsId,
    #'seq': seq
  }


def importRouteListJson( co ):
  _routeList = json.load(open('routeList.%s.json'%co))
  _stopList = json.load(open('stopList.%s.json'%co))
  for stopId, stop in _stopList.items():
    if stopId not in stopList:
      stopList[stopId] = {
        'stop': stopId,
        'name': {
          'en': stop['name_en'],
          'tc': stop['name_tc'],
          'sc': stop['name_sc']
        },
        'lat': stop['lat'],
        'long': stop['long']
      }
  
  
importRouteListJson('kmb')
  
def standardizeDict(d):
  return {key: value if not isinstance(value, dict) else standardizeDict(value) for key, value in sorted(d.items())}

db = {
  'routeList': routeList,
  'stopList': stopList
  #'stopMap': stopMap,
  #'holidays': holidays
}

with open( 'db.json', 'w' ) as f:
  f.write(json.dumps(db, ensure_ascii=False, separators=(',', ':')))
