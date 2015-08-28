#! /usr/bin/python
#
# Test / inspect IDS getLink()
# BR, 2015-08-24
#
from __future__ import print_function
import sys
import os
import logging
import icat
import icat.config
import argparse

logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

# First, parse the arguments as supplied by the IJP

parser = argparse.ArgumentParser(description="Get link(s) for the supplied datafile(s) and show the contents.")
parser.add_argument('--icatUrl', dest='icatUrl', help='ICAT url (https://host:port)')
parser.add_argument('--idsUrl', dest='idsUrl', help='IDS url (https://host:port)')
parser.add_argument('--sessionId', dest='sessionId', help='ICAT session ID')
parser.add_argument('--datafileIds', dest='datafileIds', help='List of ICAT datafile IDs')

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

datafileIds = args.datafileIds.split(",")

for datafileId in datafileIds:
    path = client.ids.getLink(datafileId)
    if os.path.exists(path):
        pathStat = "exists"
    else:
        pathStat = "does not exist"
    print("Path for datafileId:", datafileId, pathStat, "path:", path)
    #
    # Show the file contents
    # NOTE: not a good idea on real/large datafiles!
    # But nice to know whether the link really does point to something
    #
    if os.path.exists(path):
        print("File contents:")
        with open(path,'r') as fin:
            print(fin.read())
        print("(End of file contents)")
