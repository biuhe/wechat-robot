# import requests
#
# a = {
#     "HeWeather6": [
#         {
#             "basic": {
#                 "cid": "CN101280109",
#                 "location": "天河",
#                 "parent_city": "广州",
#                 "admin_area": "广东",
#                 "cnty": "中国",
#                 "lat": "23.1355896",
#                 "lon": "113.3353653",
#                 "tz": "+8.00"
#             },
#             "update": {
#                 "loc": "2019-05-16 23:03",
#                 "utc": "2019-05-16 15:03"
#             },
#             "status": "ok",
#             "now": {
#                 "cloud": "97",
#                 "cond_code": "104",
#                 "cond_txt": "阴",
#                 "fl": "32",
#                 "hum": "72",
#                 "pcpn": "0.0",
#                 "pres": "1002",
#                 "tmp": "29",
#                 "vis": "16",
#                 "wind_deg": "204",
#                 "wind_dir": "西南风",
#                 "wind_sc": "2",
#                 "wind_spd": "9"
#             }
#         }
#     ]
# }
#
# # print(a['HeWeather6'][0].get('now')['fl'])
#
#
#
#
#
#

msg = '/今天/天气怎么样'
print(len(msg.split('/')))
