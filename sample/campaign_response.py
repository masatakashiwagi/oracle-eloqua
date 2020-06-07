# -*- coding: utf-8 -*-
#!/usr/bin/env pythonn

import json
import datetime
import sys
# library append path
sys.path.append('../src')

from eloqua_request import Eloqua_Request

###
sitename = 'xxxxxxxxx'
username = 'xxxxxxxxx'
password = 'xxxxxxxxx'
###

client = Eloqua_Request(sitename, username, password, mode="REST")

asset_id = 1574
campaign_response = client.get_assets_info(object_type="campaign", asset_id=asset_id, depth="complete")
campaign_res = json.loads(campaign_response)

print campaign_response
name = campaign_res["name"]
currentStatus = campaign_res["currentStatus"]
createdAt = datetime.datetime.fromtimestamp(int(campaign_res["createdAt"]))
startAt = datetime.datetime.fromtimestamp(int(campaign_res["startAt"]))
endAt = datetime.datetime.fromtimestamp(int(campaign_res["endAt"]))
cam_res_endAt = datetime.datetime.fromtimestamp(int(campaign_res["endAt"]) + int(31536000))

print "campaign name: " + unicode(name).encode('utf-8')
print "status: " + str(currentStatus)
print "campaign created date: " + str(createdAt)
print "campaign started date: " + str(startAt)
print "campaign ended date: " + str(endAt)
print "campaign response ended date: " + str(cam_res_endAt)
