import json
from haversine import haversine, Unit

routeList = {}
stopList = {}
stopMap = {}

#def getRouteObj ( route, co, stops, bound, orig, dest, seq, fares, faresHoliday, freq, jt, nlbId, gtfsId, serviceType = '1'):
def getRouteObj ( co, route, bound, serviceType, stops, orig, dest):
  return {
    'co': co,
    'route': route,
    'bound': bound,
    'service_type': serviceType,
    'stops': stops,
    'orig': orig,
    'dest': dest,
    #'fares': fares,
    #'faresHoliday': faresHoliday,
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
  for _route in _routeList:
    routeID = ('%s%s%s%s'%(_route['co'], _route['route'], _route['bound'], _route.get('service_type', '1')))
    orig = {'en': _route['orig_en'].replace('/', '／'),
            'tc': _route['orig_tc'].replace('/', '／'),
            'sc': _route['orig_sc'].replace('/', '／')
            }
            
    dest = {'en': _route['dest_en'].replace('/', '／'),
            'tc': _route['dest_tc'].replace('/', '／'),
            'sc': _route['dest_sc'].replace('/', '／')
            }
    routeList[routeID] = getRouteObj(
            co = _route['co'],
            route = _route['route'],
            bound = _route['bound'],
            serviceType = _route.get('service_type', '1'),
            stops = _route['stops'],
            orig = orig,
            dest = dest
          #fares = _route.get('fares', None),
          #faresHoliday = _route.get('faresHoliday', None),
          #freq = _route.get('freq', None),
          #jt = _route.get('jt', None),
          #nlbId = _route.get('id', None),
          #gtfsId = _route.get('gtfsId', None),
          #seq = len(_route['stops'])
    )
    
  
  
importRouteListJson('kmb')
#importRouteListJson('ctb')
importRouteListJson('nwfb')

db = {
  'routeList': routeList,
  'stopList': stopList
  #'stopMap': stopMap,
  #'holidays': holidays
}

with open( 'db.json', 'w' ) as f:
  f.write(json.dumps(db, ensure_ascii=False, separators=(',', ':')))
