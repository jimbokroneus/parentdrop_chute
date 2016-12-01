import time
from collections import defaultdict
import json
from pprint import pprint
import os
import urllib2
import logging

try:
    import urlparse
except ImportError:
    #py3k
    from urllib import parse as urlparse

#function that checks if the json rule is in the key value store
def check(kvstore, key):
 if key in kvstore:
  return 1
 else:
  return 0

#function to execute shell scripts based on json contents
def execute_json(json_rule_id, json_timestamp, json_enabled, json_start_time, json_end_time, json_days):
 #add intimation to the log
 logging.info('Execution function called') 

 #create parameter 1 for shell script
 for i in xrange(len(json_days)):
  p1="time: "+str(json_start_time[i])+" 0 "+str(json_end_time[i])+" 0 "+str(json_days[i])
  #add confirmation to the log
  logging.info('parameter 1 - start hour, start min, end hour, end min, days - created')

  #check if contents of json are in k,v store
  flag=check(kvstore, json_rule_id)
  if flag == 0:
   logging.warning('Illegal Value')
  else:
   logging.info('Rule present in the KV Store')
   if json_enabled == "true" :
    logging.info('Rule enabled - add rule to the blacklist')
    bashCommand = "/bin/bash /usr/local/bin/parser/script_add.sh \""+p1+"\""
    os.system(bashCommand)
    for i in kvstore[json_rule_id]:
     p2=str(i.strip("\n"))
     bashCommand = "/bin/bash /usr/local/bin/parser/script_add.sh \""+p2+"\""
     os.system(bashCommand)
   else:
    logging.info('Rule disabled - remove rule from the blacklist')
    bashCommand = "/bin/bash /usr/local/bin/parser/script_remove.sh \""+p1+"\""
    os.system(bashCommand)
    for i in kvstore[json_rule_id]:
     p2=str(i.strip("\n"))
     bashCommand = "/bin/bash /usr/local/bin/parser/script_remove.sh \""+p2+"\""
     os.system(bashCommand)
  
  #restart dansguardian
  logging.info('Restarting dansguardian for it to effect')
  bashCommand = "/bin/bash /usr/local/bin/parser/script_restart.sh"
  os.system(bashCommand)
    
 
#function to parse the json contents
def parse_json(data):
 #add intimation to the log
 logging.info('Parsing function called')
 
 #variable declaration
 json_start_time = []
 json_end_time = []
 json_days = []
 json_enabled = "false"
 json_rule_id = ""
 json_timestamp = ""

 #strip required values from json
 if "rule" in data:
  json_rule_id=str(data["rule"])
 else:
  logging.warning('JSON contains no field named rule')
 if "updated_at" in data:
  json_timestamp=str(data["updated_at"])
 else:
  logging.warning('JSON contains no field named updated_at')
 if "enabled" in data:
  json_enabled=str(data["enabled"])
 else:
  logging.warning('JSON contains no field named enabled')
 if "schedule" in data:
  for uniq_id in data["schedule"]:
   json_start_time.append(int(data["schedule"][uniq_id]["lower"]))
   json_end_time.append(int(data["schedule"][uniq_id]["upper"]))
   json_days.append(int(data["schedule"][uniq_id]["day"]))
 else:
  logging.warning('JSON contains no field named schedule')

 #add confirmation to the log
 logging.info('JSON Parsed')

 #convert the day schedule to the required format
 json_days_temp = []
 for day in json_days:
  day=(day+5)%7
  json_days_temp.append(day)

 json_days = json_days_temp
 
 #add confirmation to the log
 logging.info('Days format converted')
 logging.info('Execution function to be called')

 #execute shell scripts
 execute_json(json_rule_id, json_timestamp, json_enabled, json_start_time, json_end_time, json_days)

#global variables
kvstore = defaultdict(list) # kv store for rule id - function pairing

#main utility
if __name__ == '__main__':
 #initialize logging
 logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

 #initialization phase
 USER_ID = 'Ox8rSCFHZJeplEOyfbvQDTl7zVi1' #to do --> obtain from REST API
 ROUTER_ID = '-KVx_DhXOEY2tEj5RLfb' #to do --> obtain from REST API
 URL = 'https://paradrop-3ab90.firebaseio.com/users/'+USER_ID+'/routers/'+ROUTER_ID+'/rules.json' #check
 logging.info('Connection parameters initialized')
 
 polling_interval = 60.0 #poll the firebase backend periodically
 running=1
 
 #store hard-coded values of IDs, rules from a file to a k,v store. Note: all entries in a file are unique
 myfile = open('/usr/local/bin/parser/BlockSiteList.txt', 'r')
 try:
  for line in myfile:
   rule_id, rule = line.split(" ")
   kvstore[rule_id.strip()].append(str(rule))
 finally:
  myfile.close()
 
 logging.info('BlockSiteList loaded onto KV Store')
 
 while running==1:
  start= time.clock()

  #pull json from the server 
  json_data = json.load(urllib2.urlopen(str(URL)))

  #read/parse json data
  for data in json_data:
   logging.info('Calling parsing function')
   parse_json(json_data[data])

  work_duration = time.clock() - start
  time.sleep(polling_interval - work_duration)
