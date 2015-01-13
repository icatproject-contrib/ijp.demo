#!/usr/bin/env python

# Create a datafile
# usage: create_datafile <datasetId> options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl> --filename=<filename> --contents=<string>

import sys
import os
import logging
import tempfile

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import terminate, Session, IjpOptionParser

from icat_defs import facilityName, formatName, formatVersion

logging.basicConfig(level=logging.CRITICAL)

    # IjpOptionParser predefines 'standard' IJP options:
    #   --sessionId  - the ICAT session ID
    #   --icatUrl     - URL for the ICAT service
    #   --idsUrl      - URL for the IDS service
    #   --datasetIds  - comma-separated list of dataset IDs
    #   --datafileIds - comma-separated list of datafile IDs
    # The IJP will pass these options to job scripts if the job type
    # specifies that the job will expect them.  The option dest names
    # match their names, e.g.:
    #
    #   usage = "usage: %prog options"
    #   parser = IjpOptions(usage)
    #   (options,args) = parser.parse_args()
    #   if options.datasetIds:
    #       datasetIdsList = options.datasetIds.split(',')
    #       ...

usage = "usage: %prog dataset_id options"
parser = IjpOptionParser(usage)

# Options specific to this script:

parser.add_option("--filename", dest="filename",
                  help="write contents to FILE", metavar="FILE")
parser.add_option("--contents", dest="fileContents",
                  help="contents to put into the file")

(options, args) = parser.parse_args()

jobName = os.path.basename(sys.argv[0])
print jobName, "starting..."

# Old code, when datasetId was passed 'bare'
# if len(args) < 1: terminate(jobName + " must have a datasetId argument", 1)
    
# datasetId = args[0]

# Not that we'll do anything with any extra args; could treat them as more file-contents perhaps?

rest = args[1:]    

if not options.sessionId:
    terminate(jobName + " must specify an ICAT session ID", 1)

# Report icat/ids URLs if present

if options.icatUrl:
    print "ICAT url =", options.icatUrl
else:
    print "ICAT url not supplied"

if options.idsUrl:
    print "IDS url =", options.idsUrl
else:
    print "IDS url not supplied"

sessionId = options.sessionId

if not options.datasetIds:
    terminate(jobName + " must supply a dataset ID", 1)

# Check that it's only a single ID, not a list

if len(options.datasetIds.split(',')) > 1:
    terminate(jobName + ': expects a single datasetId, not a list: ' + options.datasetIds)

datasetId = options.datasetIds

if not options.filename:
    terminate(jobName + " must specify a filename", 1)

if not options.fileContents:
    terminate(jobName + " must supply file contents", 1)
   
datasetId = int(datasetId)

session = Session(facilityName, options.icatUrl, options.idsUrl, sessionId)

# Create temporary file containing fileContents

newFile = tempfile.NamedTemporaryFile(delete=False)
newFile.write(options.fileContents)
newFile.close()

datafileFormat = session.getDatafileFormat(formatName, formatVersion)

dataset = session.get("Dataset INCLUDE Investigation, DatasetType", datasetId)

try:
    dfid = session.writeDatafile(newFile.name, dataset, options.filename, datafileFormat)
    print "Written file", options.filename, "in dataset", dataset.name, "file id =", dfid

    dataset.complete = True
    session.update(dataset)
    os.unlink(newFile.name)
                    
except Exception as e:
    print "Exception raised during datafile creation:", e
    # How do you delete a file? Following does not exist:
    # session.deleteDatafile(dfid)
    os.unlink(newFile.name)
    terminate(e, 1)

print jobName, "completed."
