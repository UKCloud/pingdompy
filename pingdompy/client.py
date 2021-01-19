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

    def get_check(self, checkid, include_teams = False):
        check = self.api.send(method="get", resource="checks", \
        resourceid=checkid, params={"include_teams": include_teams})["check"]
        return check

    def get_checks(self, tags):
        checks = self.api.send(method="get", resource = "checks", \
        data=tags)["checks"]
        return checks

    def create_check(self, obj):
        check = Check(self.api, obj=obj)
        data = check.to_json()
        response = self.api.send(method='post', resource='checks', data=data)
        check._id = int(response["check"]["id"])
        return check

    # def delete_check(self, check):
    #     if not check._id:
    #         raise Exception("CheckNotFound %s" % check.name)
    #     self.api.send(method='delete', resource='checks', resource_id=check._id)

    def update_check(self, check, changes):
        ## Caches current version of check
        if changes:
            cached = self.api.send(method='get', resource="checks", resource_id=check)['check']
            update = self.api.send(method='put', resource='checks', resource_id=check, data=changes)
            ## Gets updated version of the check
            verify = self.api.send(method='get', resource="checks", resource_id=check)['check']
            if cached != verify and update['message'] == "Modification of check was successful!":
                response = [update['message'], verify]
                return response
            elif cached == verify:
                response = "There were no changes made!"
                return response
            else:
                response = "There seems to be an issue with Pingdom!"
                return  response
        else:
            response = "No changes were specified!"
            return response
 
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
