# -*- coding: utf-8 -*-
#!/usr/bin/env pythonn

import sys
import requests
import json
import base64
import datetime
import time
import httplib

#localtime JST
now = datetime.datetime.now()
#localtime uinixtime
now_unix = int(time.mktime(now.timetuple()))

class Eloqua_Request:
    """Eloqua Login:
        you put in the below informations
        1.sitename: Eloqua instance name
        2.username: Eloqua username
        3.password: Eloqua password
     
    """
    def __init__(self, sitename, username, password, api_ver=2.0, mode=None):
        loginurl = 'https://login.eloqua.com/id'
        # Reference: http://docs.oracle.com/cloud/latest/marketingcs_gs/OMCAC/Authentication_Basic.html
        auth = sitename + '\\' + username + ':' + password
        authkey = base64.b64encode(auth)
        headers = {'content-type': 'application/json', 'authorization': 'basic ' + authkey}
        req = requests.get(loginurl, headers=headers)
        #print json.dumps(req.json(), indent = 4)
        
        # when http status error, raise error message.
        req.raise_for_status()

        if req.status_code == 200:
            if req.json() == "Not authenticated.":
                raise Exception("Error Login Infomations.")
            else:
                self.sitename = sitename
                self.username = username
                self.password = password
                self.loginurl = loginurl
                self.headers = headers
                self.urls_base = req.json()["urls"]["base"]
                self.urls_apis_rest = self.urls_base + "/API/{mode}/{version}/" .format(mode="REST", version=api_ver)
                self.urls_apis_bulk = self.urls_base + "/API/{mode}/{version}/" .format(mode="BULK", version=api_ver)


    def get_assets_info(self, object_type, asset_id=0, depth="minimal", count=10):
        object_type_list = ["contact_field", "list", "segment", "email", "landingpage", "campaign"]
        if object_type not in object_type_list:
            print "Object Type List: " + object_type_list
            raise Exception("Error object_type. Choose object_type from the above list.")

        url_partial_pre = self.urls_apis_rest + "assets/"
        q = {"depth": depth, "count": str(count)}
        if asset_id == 0:
            if object_type == "contact_field":
                url = url_partial_pre + "contact/fields"
            elif object_type == "list":
                url = url_partial_pre + "contact/lists"
            elif object_type == "segment":
                url = url_partial_pre + "contact/segments"
            elif object_type == "email":
                url = url_partial_pre + "emails"
            elif object_type == "landingpage":
                url = url_partial_pre + "landingPages"
            elif object_type == "campaign":
                url = url_partial_pre + "campaigns"
        else:
            if object_type == "contact_field":
                url = url_partial_pre + "contact/field/" + str(asset_id)
            elif object_type == "list":
                url = url_partial_pre + "contact/list/" + str(asset_id)
            elif object_type == "segment":
                url = url_partial_pre + "contact/segment/" + str(asset_id)
            elif object_type == "email":
                url = url_partial_pre + "email/" + str(asset_id)
            elif object_type == "landingpage":
                url = url_partial_pre + "landingPage/" + str(asset_id)
            elif object_type == "campaign":
                url = url_partial_pre + "campaign/" + str(asset_id)

        req = requests.get(url, headers=self.headers, params=q)
        
        if req.status_code == 200:
            print "Methond: GET => " + req.url
            print req.headers
            return json.dumps(req.json(), sort_keys=True, indent=4, ensure_ascii=False)

        else:
            return "Not Exist asset_id"

    def get_activity(self, email, activity_type, startDate=1451606400, endDate=now_unix, count=10, depth="minimal"):
        """Contact Activity
        you can know contact activity from emailaddress.
        you need a ID to retrieve activity information.
        after search for contacts based on condition, deliver a ID into Activity URI.
        you have to connect to api_version=1.0 not 2.0 to get acitivity information (REST API).
        default term you can retrieve is from 2016-01-01 to now.
        time setting is unixtime.
        """
        if email == "":
            raise Exception("Error! Confirm your email.")
        else:
            url = self.urls_apis_rest + "data/contacts"
            q = {"search": email, "depth": depth}
            req = requests.get(url, headers=self.headers, params=q)
            if req.status_code == 200:
                if req.json()["total"] == 0:
                    return "Not Exist email"
                else:
                    print "Methond: GET => " + req.url
                    #return json.dumps(req.json(), indent=4)
                    contact_id = req.json()["elements"][0]["id"]
                    print "Your Contact ID: => " + contact_id
            else:
                return req.status_code
            
            activity_type_list = ["emailOpen", "emailSend", "emailClickThrough", "emailSubscribe", "emailUnsubscribe", "formSubmit", "webVisit", "campaignMembership"]
            if activity_type not in activity_type_list:
                print "Activity Type List: " + activity_type_list
                raise Exception("Error activity_type. Choose activity_type from the above list.") 
            else:
                get_url = self.urls_base + "/API/REST/1.0/data/activities/contact/" + contact_id
                q = {"type": activity_type, "startDate": str(startDate), "endDate": str(endDate), "count": str(count)} 
                req_activity = requests.get(get_url, headers=self.headers, params=q, stream=True)
                if req_activity.status_code == 200:
                    #print req_activity.read()
                    print "Methond: GET => " + req_activity.url
                    print req_activity.headers
                    return json.dumps(req_activity.json(), sort_keys=True, indent=4, ensure_ascii=False)
                else:
                    return req_activity.status_code


    def get_cdo_id(self, cdo_name=None, depth="minimal"):
        """
        get a cdo_id from cdo_name

        :param cdo_name:
        :param depth:
        :return: cdo_id
        """
        if cdo_name == None:
            raise Exception("Error! Enter the CDO Name.")
        else:
            url = self.urls_apis_rest + "assets/customObjects"
            name = "name=" + cdo_name
            q = {"search": name, "depth": depth}
            req = requests.get(url, headers=self.headers, params=q)
            if req.status_code == 200:
                print "Methond: GET => " + req.url
                print req.headers
                results = json.dumps(req.json(), sort_keys=True, indent=4, ensure_ascii=False)
                cdo_id = req.json()["elements"][0]["id"]
                print results
                return cdo_id
            else:
                return req.status_code

    def get_cdo_data(self, cdo_id=0, count=10, depth="minimal"):
        """
        retrieve cdo_data using a get_cdo_id method

        :param cdo_id:
        :param count:
        :param depth:
        :return: cdo_contact_data
        """
        if cdo_id == 0:
            raise Exception("Error! Enter the correct CDO ID.")
        else:
            url = self.urls_apis_rest + "data/customObject/" + str(cdo_id) + "/instances"
            q = {"count": str(count), "depth": depth}
            req = requests.get(url, headers=self.headers, params=q)
            if req.status_code == 200:
                print "Methond: GET => " + req.url
                print req.headers
                return json.dumps(req.json(), sort_keys=True, indent=4, ensure_ascii=False)
            else:
                return req.status_code
