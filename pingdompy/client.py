# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .api import Api
from .check import Check
from .maintenance import Maintenance


class Client(object):
    """Interact with API."""

    def __init__(self, apikey, api_version='3.1'):
       
        """
        Initializer.

        :param apikey: Pingdom api key
        """
        self.api = Api(apikey, api_version)
        # cache checks
        self.checks = {}
        self.maintenances = {}
        for item in self.api.send('get', "checks", params={"include_tags": True})['checks']:
            self.checks[item["name"]] = Check(self.api, json=item)

    def get_check(self, name=None, _id=None):
        if name:
            return self.checks.get(name, None)
        elif _id:
            for _name, check in self.checks.items():
                if check._id == _id:
                    return check
        else:
            raise Exception("Missing name or _id")

    def get_checks(self, filters=None):
        if filters is None:
            return [c for c in self.checks.values()]

        return [c for c in self.checks.values() if len(set(u + filters.get("status", c.status)
                for u in filters.get("tags", [])).intersection(set([x['name'] + c.status for x in c.tags])))]

    # def create_check(self, obj):
    #     c = Check(self.api, obj=obj)
    #     data = c.to_json()
    #     response = self.api.send(method='post', resource='checks', data=data)
    #     c._id = int(response["check"]["id"])
    #     c.from_json(self.api.send('get', "checks", response["check"]["id"])['check'])
    #     self.checks[c.name] = c
    #     return c

    # def delete_check(self, check):
    #     if not check._id:
    #         raise Exception("CheckNotFound %s" % check.name)
    #     self.api.send(method='delete', resource='checks', resource_id=check._id)
    #     self.checks.pop(check.name, None)

    # def update_check(self, check, changes):
    #     # ensure definition is updated
    #     check.fetch()
    #     # cache current definition to detect idempotence when modify is called
    #     cached_definition = check.to_json()
    #     check.from_obj(changes)
    #     data = check.to_json()
    #     if data == cached_definition:
    #         return False
    #     # GET /checks (get_checks) returns 'verify_certificate' regardless
    #     if check.type == 'http':
    #         # The http-type API will only accept a parameter called 'encryption' though.
    #         data['encryption'] = changes['encryption'] if 'encryption' in changes else data['verify_certificate']
    #     del data['verify_certificate']  # 'verify_certificate' is not a valid parameter
    #     del data["type"]  # type can't be changed
    #     self.api.send(method='put', resource='checks', resource_id=check._id, data=data)
    #     check.from_json(self.api.send('get', "checks", check._id)['check'])
    #     return check
     
    def get_maintenance(self, window_id):
        value = str(window_id)
        response = self.api.send(method = 'get', resource = 'maintenance', resource_id = value)
        return response

    def create_maintenance(self, obj):
         window = Maintenance(self.api, obj=obj)
         value = window.to_json()
         response = self.api.send(method = 'post', resource = 'maintenance', data = value)
         window._id = response["maintenance"]["id"]
         return window

    # def servertime(self):
    #     return self.api.send(method='get', resource='servertime')['servertime']

    # def get_summary_average(self, checkid, start=None, end=None, probes=None, include_uptime=None, by_country=None,
    #                         by_probe=None):
    #     params = {}
    #     if start is not None:
    #         params['from'] = start
    #     if end is not None:
    #         params['to'] = end
    #     if probes is not None:
    #         params['probes'] = probes
    #     if include_uptime is not None:
    #         params['includeuptime'] = include_uptime
    #     if by_country is not None:
    #         params['bycountry'] = by_country
    #     if by_probe is not None:
    #         params['byprobe'] = by_probe
    #     return self.api.send('get', resource="summary.average", resource_id=checkid, params=params)

    # def get_summary_outage(self, checkid, start=None, end=None, order="asc"):
    #     params = {}
    #     if start is not None:
    #         params['from'] = start
    #     if end is not None:
    #         params['to'] = end
    #     if order is not None:
    #         params['order'] = order
    #     return self.api.send('get', resource="summary.outage", resource_id=checkid, params=params)