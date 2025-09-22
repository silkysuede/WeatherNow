import re
import json
import asyncio
import aiohttp
import datetime
from typing import Union, Any, Dict, List
from dataclasses import dataclass

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

@dataclass(frozen=False, kw_only=False, slots=True, repr=False, eq=False, match_args=False)
class _Alert:
    active: bool = None
    start: datetime.datetime = None
    end: datetime.datetime = None 
    status: "list[str]" = None
    message_type: "list[str]" = None
    event: "list[str]" = None
    code: "list[str]" = None
    area: "list[str]" = None
    point: "list[str]" = None
    region: "list[str]" = None
    region_type: str = None
    zone: "list[str]" = None
    urgency: "list[str]" = None
    severity: "list[str]" = None
    certainty: "list[str]" = None
    limit: int = None
    cursor: str = None


class WeatherWrapper:
    
    def __init__(self, base_url : str):
        self.base_url = base_url

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, url : str) -> None:
        self._base_url = url
        
    @property
    def request_url(self) -> str:
        return self._request_url
    
    @request_url.setter
    def request_url(self, url : str)-> None:
        self._request_url = self.base_url + url

    async def _async_request_get(self, session : aiohttp.ClientSession, url : str, data=None) -> list:
        '''
            Asynchronous GET request.
        '''
        
        session_get = session.request(method='GET', url=url, params=data)
        async with session_get as response:
            text = await response.text()
            return [response.raw_headers, response.status, text]
        
    async def _async_request_post(self, session : aiohttp.ClientSession, url : str, data) -> JSONType | str:
        '''
            Asynchronous POST request.
        '''
        
        session_post = session.request(method='POST', url=url, data=data)
        async with session_post as response:
            ret = None
            try:
                ret = await response.json()
            except Exception:
                ret = await response.text()
            return ret

    async def _async_session(self, request, urls : str | list, arg_dict_list:list[dict]=None) -> list | JSONType | str:
        '''
            Create an async session for making API requests. Can handle one or many URLs as arguments.\n
            If using many URLs, args can be passed as well.\n
            Returns a list of responses.
        '''
        
        if urls and request:
            tasks = []
            async with aiohttp.ClientSession() as session:
                if isinstance(urls, str):
                    urls = [urls]
                if isinstance(urls, (list, tuple)):
                    for i in range(len(urls)):
                        tasks.append(
                            asyncio.ensure_future(request(session, urls[i], arg_dict_list[i] if arg_dict_list else None))
                        )
                else:
                    raise TypeError("'urls' must be of type 'str' or 'list'.")

                responses = await asyncio.gather(*tasks)

                return responses
        else:
            return None

    def get_alerts(
        self,
        active : bool=None,
        start : datetime.datetime=None,
        end : datetime.datetime=None, 
        status : "list[str]"=None,
        message_type : "list[str]"=None,
        event : "list[str]"=None,
        code : "list[str]"=None,
        area : "list[str]"=None,
        point : "list[str]"=None,
        region : "list[str]"=None,
        region_type : str=None,
        zone : "list[str]"=None,
        urgency : "list[str]"=None,
        severity : "list[str]"=None,
        certainty : "list[str]"=None,
        limit : int=None,
        cursor : str=None
    ):
        new_alert = WeatherAlert(
            self.base_url,
            active,
            start,
            end, 
            status,
            message_type,
            event,
            code,
            area,
            point,
            region,
            region_type,
            zone,
            urgency,
            severity,
            certainty,
            limit,
            cursor
        )
        return new_alert.parse_alerts(new_alert.format_alerts(new_alert.get_alerts()))

    def get_glossary(self):
        glossary = WeatherGlossary(self.base_url)
        return glossary.parse_glossary(glossary.format_glossary(glossary.get_glossary()))

class WeatherAlert(WeatherWrapper):
    def __init__(
        self,
        base_url : str,
        active : bool=None,
        start : datetime.datetime=None,
        end : datetime.datetime=None, 
        status : "list[str]"=None,
        message_type : "list[str]"=None,
        event : "list[str]"=None,
        code : "list[str]"=None,
        area : "list[str]"=None,
        point : "list[str]"=None,
        region : "list[str]"=None,
        region_type : str=None,
        zone : "list[str]"=None,
        urgency : "list[str]"=None,
        severity : "list[str]"=None,
        certainty : "list[str]"=None,
        limit : int=None,
        cursor : str=None
    ):
        super().__init__(base_url)
        self.alert = _Alert(
            active,
            start,
            end, 
            status,
            message_type,
            event,
            code,
            area,
            point,
            region,
            region_type,
            zone,
            urgency,
            severity,
            certainty,
            limit,
            cursor 
        )

    def get_alerts(self) -> list:
        self.request_url = '/alerts'
        alerts = []
        
        arg_dict_list = [
            {
                'active'       : self.alert.active,
                'start'        : self.alert.start,
                'end'          : self.alert.end,
                'status'       : self.alert.status,
                'message_type' : self.alert.message_type, 
                'event'        : self.alert.event,
                'code'         : self.alert.code,
                'urgency'      : self.alert.urgency,
                'severity'     : self.alert.severity,
                'certainty'    : self.alert.certainty,
                'limit'        : self.alert.limit,
                'cursor'       : self.alert.cursor
            }
        ]
        incompatible = {
            'area'          : self.alert.area,
            'point'         : self.alert.point,
            'region'        : self.alert.region,
            'region_type'   : self.alert.region_type,
            'zone'          : self.alert.zone
        }
        found = {}
        found_count = 0
        
        for k, v in incompatible.items():
            if found_count > 1:
                print(f'{found.keys()[0]} is incompatible with {k}.')
                return alerts
            
            if incompatible[k]:
                found[k] = incompatible[k]
                found_count += 1
                
        for param_name, param_val in found.items():
            arg_dict_list[0][param_name] = param_val
        
        filtered_args = [{}]
        for k,v in arg_dict_list[0].items():
            if v:
                filtered_args[0][k] = v
                
        alerts = asyncio.run(self._async_session(self._async_request_get, self.request_url, arg_dict_list=filtered_args))
        
        return alerts
    
    @staticmethod
    def format_alerts(alerts : list):
        new_alerts = []
        
        for alert in alerts:
            if alert:
                new_alert = {
                    'headers'       : alert[0] if alert[0] else None,
                    'response_code' : alert[1] if alert[1] else None,
                    'response'      : json.loads(alert[2]) if alert[2] else None
                }
                new_alerts.append(new_alert)
                
            else:
                new_alerts.append({})
        return new_alerts
    
    @staticmethod
    def parse_alerts(alerts : "list[dict]"):
        parsed_alerts = []
        for alert in alerts:
            for a in alert['response']['features']:
                parsed = {
                    #'coordinates'   : a['geometry']['coordinates'],
                    'areaDesc'      : a['properties']['areaDesc'],
                    'effective'     : a['properties']['effective'],
                    'onset'         : a['properties']['onset'],
                    'expires'       : a['properties']['expires'],
                    'ends'          : a['properties']['ends'],
                    'severity'      : a['properties']['severity'],
                    'certainty'     : a['properties']['certainty'],
                    'urgency'       : a['properties']['urgency'],
                    'event'         : a['properties']['event'],
                    'sender'        : a['properties']['sender'],
                    'senderName'    : a['properties']['senderName'],
                    'headline'      : a['properties']['headline'],
                    'description'   : a['properties']['description'],
                    'instruction'   : a['properties']['instruction'],
                    'response'      : a['properties']['response'],
                    #'windThreat'    : a['properties']['parameters']['windThreat'],
                    #'maxWindGust'   : a['properties']['parameters']['maxWindGust'],
                    #'hailThreat'    : a['properties']['parameters']['hailThreat'],
                    #'maxHailSize'   : a['properties']['parameters']['maxHailSize']
                }
                parsed_alerts.append(parsed)
        return parsed_alerts

class WeatherGlossary(WeatherWrapper):
    def __init__(self, base_url):
        super().__init__(base_url)
    
    def get_glossary(self):
        self.request_url = '/glossary'
        
        glossary = asyncio.run(self._async_session(self._async_request_get, self.request_url))
        return glossary
    
    @staticmethod
    def format_glossary(glossary : list):
        new_glossary = []
        
        for alert in glossary:
            if alert:
                new_alert = {
                    'headers'       : alert[0] if alert[0] else None,
                    'response_code' : alert[1] if alert[1] else None,
                    'response'      : json.loads(alert[2]) if alert[2] else None
                }
                new_glossary.append(new_alert)
                
            else:
                new_glossary.append({})
        return new_glossary
    
    @staticmethod
    def parse_glossary(alerts : "list[dict]"):
        parsed_alerts = []
        for alert in alerts:
            for g in alert['response']['glossary']:
                parsed_alerts.append(g)
        return parsed_alerts

if __name__ == "__main__":
    wrapper = WeatherWrapper('https://api.weather.gov')
    resps = wrapper.get_alerts(start='2025-09-12T00:00:00Z', end='2025-09-17T00:00:00Z', status=['actual'], message_type=['alert'], area=['KS'], limit=1)
    print(resps)
    