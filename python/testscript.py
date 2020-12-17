import configparser
import json
from collections import Counter
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.request import install_opener, build_opener, HTTPSHandler
import ssl
import base64
import time as t
from datetime import date
from datetime import time
from datetime import datetime
filedate = datetime.now()
#Reading the configuration file
config = configparser.ConfigParser()
config.read("configuration.ini")
#The AQL search to execute
SQLs = {"OffenseCreated": quote("SELECT  \"Offense_ID\" as 'OffenseID', RULENAME(\"Rule_ID\") AS 'RuleName', DATEFORMAT(starttime,'yyyy-MM-dd hh:mm:ss a') AS StartTime, DATEFORMAT(endtime,'yyyy-MM-dd hh:mm:ss a') AS StorageTime, DATEFORMAT(devicetime,'yyyy-MM-dd hh:mm:ss a') AS LogSourceTime, QIDNAME(qid) AS 'EventName' FROM events WHERE qid='28250369' LAST 24 HOURS")}
#Execute AQL search for all clients:
for section_name in config.sections():
    Server_IP = config.get(section_name, "server_ip")
    Auth_token = config.get(section_name, "auth_token")
    header = {'Accept': 'application/json', 'SEC': Auth_token, 'Version': '9'}
    BASE_URL = "https://" + Server_IP + "/api/ariel/searches"
    for key, value in SQLs.items():
        url = BASE_URL + "?query_expression=" + SQLs[key]
#Execution of the AQL query by using the API  ARIEL MODULE
        request = Request(url, headers=header, method="POST")
#The validation of the certification.
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        install_opener(build_opener(HTTPSHandler(
            context=context, check_hostname=False)))
#Extract the search id of the AQL query
        response = urlopen(request)
        data = response.read().decode("utf-8")
        response_json = json.loads(data)
        search_id = response_json['search_id']
        t.sleep(600)
#Exploit the search id to get the results
        url1 = BASE_URL + "/" + search_id + "/" + "results"
#Wait for stroking the results of the search_id
        results_request = Request(url1, headers=header, method="GET")
        # cafile=certifi.where()
        results_response = urlopen(results_request)
        results_data = results_response.read()
        results_json = json.loads(results_data.decode('utf-8'))
#Store the results in json file
        with open('logs/' + section_name + "-" + key + "-" + filedate.strftime("%d%m%Y%H%M") + ".json", 'a+') as outfile:
            json.dump(results_json, outfile)
