# -*- coding: utf-8 -*-
#!/usr/bin/env pythonn

import json
import datetime
from eloqua_request import Eloqua_Request

###
sitename = 'xxxxxxxxx'
username = 'xxxxxxxxx'
password = 'xxxxxxxxx'
###

client = Eloqua_Request(sitename, username, password, mode="REST")
campaign_response = client.get_assets_info(object_type="campaign", asset_id=1574, depth="complete")
campaign_res = json.loads(campaign_response)

print campaign_response
name = campaign_res["name"]
currentStatus = campaign_res["currentStatus"]
createdAt = datetime.datetime.fromtimestamp(int(campaign_res["createdAt"]))
startAt = datetime.datetime.fromtimestamp(int(campaign_res["startAt"]))
endAt = datetime.datetime.fromtimestamp(int(campaign_res["endAt"]))
cam_res_endAt = datetime.datetime.fromtimestamp(int(campaign_res["endAt"]) + int(31536000))

print "キャンペーン名: " + unicode(name).encode('utf-8')
print "ステータス: " + str(currentStatus)
print "キャンペーン作成日: " + str(createdAt)
print "キャンペーン開始日: " + str(startAt)
print "キャンペーン終了日: " + str(endAt)
print "キャンペーンレスポンス終了日: " + str(cam_res_endAt)
