#! /usr/bin/python
#
# Demo of use of getPreparedData etc.
# BR, 2016-08-05
#
from __future__ import print_function
import sys
import os
import logging
import icat
import icat.config
import argparse
import time

logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

def getDataset(datasetId,compressFlag=False,zipFlag=False,wait=False,reportMiss=False):
    """
    Get the specified dataset. If wait is True, will wait
    until the data is prepared; otherwise the call will fail
    for unprepared data (but the IDS will attempt to restore the data
    in the background). Report on cache misses if reportMiss is True.
    """
    sleepTime = 0.1 # 1/10 sec
    datasetResult = client.search("SELECT ds FROM Dataset ds WHERE ds.id = %d" % (datasetId))
    # if data is already in the cache, this will work immediately
    prepId = client.prepareData(datasetResult,compressFlag,zipFlag)
    miss = False
    if wait:
        while not client.isDataPrepared(prepId):
            if reportMiss and not miss:
                print("Dataset",datasetId,"not in local cache; waiting to prepare...")
                miss = True
                time.sleep(sleepTime)
    if reportMiss and miss:
        print("... prepared.")
    return client.getPreparedData(prepId)

# First, parse the arguments as supplied by the IJP

parser = argparse.ArgumentParser(description="Get link(s) for the supplied datafile(s) and show the contents.")
parser.add_argument('--icatUrl', dest='icatUrl', help='ICAT url (https://host:port)')
parser.add_argument('--idsUrl', dest='idsUrl', help='IDS url (https://host:port)')
parser.add_argument('--sessionId', dest='sessionId', help='ICAT session ID')
parser.add_argument('--datasetIds', dest='datasetIds', help='List of ICAT dataset IDs')

args = parser.parse_args()

# Now, construct the args expected by python-icat

pycatArgs = ['--url=%s/ICATService/ICAT?wsdl' % (args.icatUrl,),
    '--idsurl=%s/ids' % (args.idsUrl,)]

# IJP jobs work within a pre-existing session,
# so we have to set needlogin=False
# (otherwise python-icat's Config will expect auth/username/password)

conf = icat.config.Config(needlogin=False, ids="optional").getconfig(pycatArgs)

client = icat.Client(conf.url, **conf.client_kwargs)

# Set the sessionId directly from that supplied by the IJP
# Note that python-icat should NOT log out on closure
# so set autoLogout=False

client.sessionId = args.sessionId
client.autoLogout=False

# Simple test of a session property

print("User:", client.getUserName())

# Now, what does getLink() return?

datasetIds = args.datasetIds.split(",")

for datasetId in datasetIds:
    print("Getting dataset " + datasetId)
    dataset = getDataset(int(datasetId),compressFlag=False,zipFlag=True,wait=True,reportMiss=True)
    # dataset should now be a (handle on a) zip file
    # We're not really interested in the result here!
    print("dataset info:",dataset.info(),"url",dataset.url)

