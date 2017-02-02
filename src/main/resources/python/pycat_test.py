#! /usr/bin/python
#
# Testbed for my python-icat hypotheses
# BR, 2015-08-19
#
from __future__ import print_function
import sys
import logging
import icat
import icat.config
import argparse

logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

# First, parse the arguments as supplied by the IJP

parser = argparse.ArgumentParser(description="Show ICAT and IDS versions.")
parser.add_argument('--icatUrl', dest='icatUrl', help='ICAT url (https://host:port)')
parser.add_argument('--idsUrl', dest='idsUrl', help='IDS url (https://host:port)')
parser.add_argument('--sessionId', dest='sessionId', help='ICAT session ID')
parser.add_argument('--ijpUrl', dest='ijpUrl', help='IJP url')
parser.add_argument('--ijpJobId', dest='ijpJobId', help='IJP job id')

args = parser.parse_args()

print('ICAT url: %s; IDS url: %s' % (args.icatUrl, args.idsUrl))

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

