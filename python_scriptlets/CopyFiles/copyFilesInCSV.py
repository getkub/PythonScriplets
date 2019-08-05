#!/usr/bin/python
import csv, time
import os, shutil
import sys, pwd, grp
import logging

# =======================================================================================
# Script to copy files from Source to Destination based on rules specified by CSV
# Created    	  :         getkub  ( I'm no python coder, hence some methods are crude)
# Version      	:         0.1
# Date        	:         2014-02-22
# v0.1          :         Initial Version 2014-02-22
# =======================================================================================
# *************************************************************************************
# Validations
# *************************************************************************************
if os.geteuid() != 0:
    logging.error('You need to have root privileges to run this script. Exiting.')
    exit(2)

if(len(sys.argv) < 2):
    print "You must set 1 arguments!!"
    print "Usage is : <scriptname> <arg1>"
    exit(2)

# *************************************************************************************
# Variable settings
# *************************************************************************************
program                  =    sys.argv[0]
APP_DIR                  =    os.path.dirname(os.path.dirname(os.path.dirname(program)))
LOG_DIR                  =    APP_DIR + '/logs'
CONF_DIR                 =    APP_DIR + '/configs'

# *************************************************************************************
# Logging Configurations
# *************************************************************************************
TODAY_YYYYMMDD     =    time.strftime("%Y%m%d")
LOG_FILENAME       =    'copyFiles.' + TODAY_YYYYMMDD + '.log'
LOG_ABSFILE        =    LOG_DIR  + '/' + LOG_FILENAME
logging.basicConfig(filename=LOG_ABSFILE, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# *************************************************************************************
# External Configurations
# *************************************************************************************


# *************************************************************************************
# Script Info
# *************************************************************************************
INPUT_PARAMS_LENGTH       =     len(sys.argv)
logging.debug('Number of arguments=' + str(INPUT_PARAMS_LENGTH))
logging.debug('Argument list:' + str(sys.argv))

# *************************************************************************************
# Script Parameters
# *************************************************************************************
CSV_FILE_IN_ABS         =     sys.argv[1] # This should be absolute path
# *************************************************************************************
# Script Specific checks
# *************************************************************************************
logging.debug('Starting Script: ' + program)

# IF no file, then assume no action to do
if not os.path.isfile(CSV_FILE_IN_ABS):
    logging.warn('File: ' + CSV_FILE_IN_ABS + ' NOT present.')
    print('Warn: File ' + CSV_FILE_IN_ABS + ' NOT present.')
    logging.info('Ending Script: ' + program)
    sys.exit()

# ============================================================================
# -- CSV File of below format
# Source,Destination,Owner,Group,Permission,Description
# -- Source is relative to configFiles
# ============================================================================
reader2 = csv.reader(filter(lambda row: row[0]!='#',open(CSV_FILE_IN_ABS, 'rb')))

# Python 2.x has problem with os.chmod as it accepts only in octal mode. Also it needs to be integer
# The only way to do is to convert permission into octal (with base8) and provide as it is to os.chmod
# http://stackoverflow.com/questions/18806772/most-pythonic-way-to-convert-a-string-to-a-octal-number

for row in reader2:
    if  ServerTypeTag in row[0]:
        Source         =         row[0]
        Destination    =         row[1]
        Owner          =         row[2]
        Group          =         row[3]
        Permission     =         row[4]
        Description    =         row[5]

        OCTAL_Permission=int(Permission,8)
        logging.debug('Source=' + Source + ',Destination=' + Destination + ',Owner=' + Owner + ',Group=' + Group + ',Permission=' + str(Permission) )
        try:
            logging.info("Copying file " + Source + ' to ' + Destination)
            shutil.copyfile(Source,Destination)
            uid = pwd.getpwnam(Owner).pw_uid
            gid = grp.getgrnam(Group).gr_gid
            os.chown(Destination, uid, gid)
            os.chmod(Destination, OCTAL_Permission)
        except:
            logging.error("Error Copying file " + Source + ' to ' + Destination)
            print 'Error: (Skipping) Error Copying file ' + Source + ' to ' + Destination
            pass

    else:
        logging.debug('No files to Copy. Filters were: ServerTypeTag=' + ServerTypeTag + ',Source=' + row[0] )


logging.debug('Ending Script: ' + program)

# ============================================================================
# End of Script
# ============================================================================
