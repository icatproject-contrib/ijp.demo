#!/usr/bin/env python

# Test batch job arguments
# Essentially, just reports whatever it finds on the command line
# usage: test_args options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl>
# optional options: --datasetIds=<id1,...> --datafileIds=<id1,...>

import sys
import os
import logging

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import IjpOptionParser

logging.basicConfig(level=logging.CRITICAL)

usage = "usage: %prog options"

parser = IjpOptionParser(usage)

# Options specific to this script
# Job Type specs can choose to use these, but can't invent their own
# (parse_args() will throw an error for unknown options)

parser.add_option("--option-one", dest="optionOne",
                 help="script-specific option 1")
parser.add_option("--option-two", dest="optionTwo",
                 help="script-specific option 2")

(options, args) = parser.parse_args()

jobName = os.path.basename(sys.argv[0])
print jobName, "starting..."

rest = args  

if options.sessionId:
    print "ICAT sessionId provided"
else:
    print "No ICAT sessionId provided"

# Report icat/ids URLs if present

if options.icatUrl:
    print "ICAT url =", options.icatUrl
else:
    print "ICAT url not supplied"

if options.idsUrl:
    print "IDS url =", options.idsUrl
else:
    print "IDS url not supplied"

if options.datasetIds:
    print "datasetIds = ", options.datasetIds
else:
    print "datasetIds not supplied"

if options.datafileIds:
    print "datafileIds = ", options.datafileIds
else:
    print "datafileIds not supplied"

if options.optionOne:
    print "Option 1 = ", options.optionOne

if options.optionTwo:
    print "Option 2 = ", options.optionTwo

print "Other command-line arguments (if any): ", args

print jobName, "completed."
