pingdompy
=========


Python library for interacting with Pingdom services (REST API and maintenance windows).


Features
--------


* Check management: create, delete, update, list
* Maintenance windows: create, delete, list


Requirements
------------


* Pingdom account
* requests (0.10.8 or newer)


Installation
------------

The git repo will need to be cloned to your local system and installed using the following: 

```
    >>> git clone https://github.com/UKCloud/pingdompy.git
    >>> pip3 install -e /path/to/clone/pingdompy
```

Usage
-----

The *client* object will allow you to interact with the API.

```
    >>> import pingdompy
    >>> client = pingdompy.Client(apikey="your api key")
```

Checks
------

**List all checks:**

The Pingdom Api can be called to recieve a comprehensive list of all checks visible to the api key specified:

```
    >>> checks = client.get_checks()
        print(checks)

    [{
        "type": "http",
        "id": 100,
        "name": "mycheck",
        "lasterrortime": 1297446423,
        "lasttesttime": 1300977363,
        "lastresponsetime": 355,
        "status": "up",
        "resolution": 0,
        "hostname": "string",
        "created": 0,
        "tags": [{"name": "apache", "type": "a", "count": 2}],
        "probe_filters": ["region: EU"],
        "ipv6": true
    }]
```

List checks with *production* and *frontend* tags:

```
    >>> client.get_checks(tags=[production,frontend])
```

**List specific check:**

Pingdom can also be called to pull a more detailed list of a specific check when an ID is passed in:

```
    >>> check = client.get_check(checkid)
    print(check)

    {
        "type": {},
        "sendnotificationwhendown": 6,
        "notifyagainevery": 5,
        "notifywhenbackup": true,
        "responsetime_threshold": 30000,
        "custom_message": "Important check is down!",
        "integrationids": [],
        "id": 100,
        "name": "mycheck",
        "lasterrortime": 1297446423,
        "lasttesttime": 1300977363,
        "lastresponsetime": 355,
        "status": "up",
        "resolution": 0,
        "hostname": "string",
        "created": 0,
        "tags": [],
        "probe_filters": [],
        "ipv6": true,
        "verify_certificate": true,
        "ssl_down_days_before": 0
    }
```

**Create a check:**

```
    >>> changes = {
            "name": "Check Check"
            "host": "www.google.com",
            "tags": [{"name": "pingdompy-test"},
            "resolution": "60"
            "type": "http"
        }
    >>> client.create_check(check_definition)
```

Refer to [this page](https://docs.pingdom.com/api/#tag/Checks/paths/~1checks/post) for the list of options that could also be implemented.

**Integrations: (not yet implemented)**

To enable/disable an integration plugins (like webhooks) use the field *integrationids* (array with integer ids to set or "null" tring to remove it)

**Alert policies: (not yet implemented)**

To bind an alerting policy use the field *alert_policy* (numeric id to set it or string "null" to disable alerts)


**Update a check:**

```
    >>> client.update_check(check, {"paused": True})
```

By passing in the checks' id as "check" and a json formatted array of changes, you can update a check. This will return the updated checks' details for verification and a message confirming the update occured.


**Delete a check:**

```
    >>> client.delete_check(check)
```

By passing in the check's id as "check", this will delete the specified check and return a message confirming it's deletion. Only supports a singular deletion at a time. **This cannot be undone**


Maintenance windows
-------------------

**Create a 1 hour maintenance window for production websites:**

```
    >>> start = datetime.datetime.now() + datetime.timedelta(minutes=int(start_time))
    >>> end = start + datetime.timedelta(minutes=int(duration_time))

    >>> window = client.create_maintenance({"name": maint_name, \
        "start": start, "stop": end, "uptime_ids": uptime_ids})
```

This will create a maintenance window for the specified check id. Multiple id's may be specified using a comma delimited string. E.G: "123456,654321". The times are in minutes and the start time is required in the format of how many minutes until the maintenance will begin from current time.


**List a maintenance window's information**

```
    client.get_maintenance(window_id)
```

This will list and return the details for the specified maintenance window id. Only supports a singular id at a time.


**Delete future maintenance windows:**

```
    client.delete_maintenance(window_id)
```

By passing in the maintenance window's id, this will delete the specified window and return a message confirming it's deletion. Only maintenance windows in the future are able to be deleted. Only supports a singular deletion at a time.