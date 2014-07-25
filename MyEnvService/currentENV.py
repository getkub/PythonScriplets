#!/usr/bin/python
import time, logging
import csv
import os, sys, socket

####
####
###  DO NOT RUN this script of its OWN. BUT use the Wrapper provided as separate script
####
####

# =======================================================================================
# Script to generate various Environment Parameters from CSV or external methods
# Created     :         getkub@github
program =    sys.argv[0]
version =    "1"
verdate =    "2014-02-22T13:02:00Z"
#      Version    Date      Comment
#       1       2014-03-04 Initial Version
#       2       2014-05-23 Changed logic to merge Array as Omnibus not detecting quotes
# =======================================================================================

# *************************************************************************************
# Variable settings
# *************************************************************************************
program                  =    sys.argv[0]
module_path              =    os.path.dirname(os.path.dirname(os.path.dirname(program)))
LOG_DIR                  =    module_path + '/logs'
CONF_DIR                 =    module_path + '/configs'

# *************************************************************************************
# Script Parameters
# *************************************************************************************
CSV_FILE_IN_ABS         =     CONF_DIR + '/csv/allEnvProperties.csv'
THIS_HOST               =     socket.gethostname() # socket.gethostname()
# *************************************************************************************
# Script Specific checks
# *************************************************************************************

# IF no file, then assume no action to do
if not os.path.isfile(CSV_FILE_IN_ABS):
    print ('File: ' + CSV_FILE_IN_ABS + ' NOT present.')
    sys.exit()
# *************************************************************************************
# Function Definition
# *************************************************************************************

def env_Invalid():
    isEnvironmentValid     =         "False"
    return

# ============================================================================
# CSV loading
# http://stackoverflow.com/questions/186916/configuration-file-with-list-of-key-value-pairs-in-python
# ============================================================================

# ============================================================================
# Below function needs to be customised for your needs
# You can either use the headers in CSV/config file, but it is better to override
#         to get/is methods for better readability
# ============================================================================

def env_ThisHost():
    reader2 = csv.reader(filter(lambda row: row[0]!='#',open(CSV_FILE_IN_ABS, 'rb')))
    COUNT   = 0
    for row in reader2:
        if THIS_HOST == row[0]:
           COUNT = COUNT + 1
           envList = {
            'isEnvironmentValid': 'True',
            'getServiceName'    :  row[0],
            'getServiceIP'      :  row[1],
            'getMgmtIP'         :  row[2],
            'isClustered'       :  row[5]
            }

    if  COUNT == 0 :
        logging.warn('Current Host Not existing in: ' + CSV_FILE_IN_ABS)
        envList = {
            'isEnvironmentValid': 'False'
            }

    return  envList

env_ThisHost()

# ============================================================================
# End of Script
# ============================================================================


