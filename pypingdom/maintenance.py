# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import time


class Maintenance(object):

    def __init__(self, client, json=False, obj=False):
        self.client = client
        self._id = False
        if json:
            self.from_json(json)
        elif obj:
            self.from_obj(obj)
        else:
            raise Exception("Missing definition: use json or obj parameter")

    def __repr__(self):
        checks = []
        for check in self.checks:
            if check:
                checks.append(check.name)
            else:
                checks.append("<deleted check>")
        return """
        pingdom.Maintenance <{0}>
         name: {1}
         from: {2}
         to: {3}
         checks: {4}
        """.format(self._id,
                   self.name,
                   self.start,
                   self.stop,
                   ", ".join(checks))

    def to_json(self):
        check_ids = [str(check._id) for check in self.checks if check]
        data = {
            # "__csrf_magic": "",
            # "id": "",
            "description": self.name,
            "from": int(time.mktime(self.start.timetuple())),
            "to": int(time.mktime(self.stop.timetuple())),
            "uptimeids": "{0}".format(",".join(check_ids))
        }
        return data

    def from_json(self, obj):
        self._id = int(obj['id'])
        self.name = obj["description"]
        self.start = datetime.datetime.fromtimestamp(obj['from'])
        self.stop = datetime.datetime.fromtimestamp(obj['to'])
        self.checks = [self.client.get_check(_id=int(x)) for x in obj['checks']['uptime']]

    def from_obj(self, obj):
        self.name = obj["name"]
        self.start = obj['start']
        self.stop = obj['stop']
        self.checks = obj['checks']
