#!/usr/bin/env python

# Copy a datafile to another dataset - demo script
# usage: copy_datafile options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl> --datasetIds=<setId> --datafileIds=<fileId>
# Expects one datasetId and one datafileId

import sys
import os
import logging
import tempfile

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import terminate, Session, IjpOptionParser

from icat_defs import facilityName

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

# Options specific to this script: none

try:
    (options, args) = parser.parse_args()
except Exception as e:
    print "Exception raised when parsing command-line options:", e
    terminate(e, 1)

jobName = os.path.basename(sys.argv[0])
print jobName, "starting..."

# Not that we'll do anything with any extra args; could treat them as more file-contents perhaps?

rest = args[1:]    

if not options.sessionId:
    terminate(jobName + " must specify an ICAT session ID", 1)

# Report icat/ids URLs if present

if options.icatUrl:
    print "ICAT url =", options.icatUrl
else:
    terminate(jobName + ": ICAT url not supplied", 1)

if options.idsUrl:
    print "IDS url =", options.idsUrl
else:
    terminate(jobName + ": IDS url not supplied", 1)

sessionId = options.sessionId

if not options.datasetIds:
    terminate(jobName + " must supply a dataset ID", 1)

# Check that it's only a single ID, not a list

if len(options.datasetIds.split(',')) > 1:
    terminate(jobName + ': expects a single datasetId, not a list: ' + options.datasetIds,1)

# Similarly for the datafileIds

if not options.datafileIds:
    terminate(jobName + " must supply a datafile ID", 1)

# Check that it's only a single ID, not a list

if len(options.datafileIds.split(',')) > 1:
    terminate(jobName + ': expects a single datafileId, not a list: ' + options.datafileIds,1)

targetDatasetId = int(options.datasetIds)
# Keep datafileId as str for now
datafileId = options.datafileIds

session = Session(facilityName, options.icatUrl, options.idsUrl, sessionId)

# TODO: check whether the datafile is already in the dataset?

# Get the target dataset

try:
    targetDataset = session.get("Dataset INCLUDE Investigation, DatasetType", targetDatasetId)

except Exception as e:
    print "Error retrieveing target dataset: ", e
    terminate( e, 1)

# Get the (source) datafile

try:
    datafile = session.get("Datafile INCLUDE Dataset, DatafileFormat", datafileId)

except Exception as e:
    print "Error retrieving datafile: ", e
    terminate( e, 1)

# Get properties we will need to create a new copy of the datafile

filename = datafile.name

# Test for each field's existence before trying to use it

fileDesc = ""
if hasattr(datafile,'description'): fileDesc = datafile.description

fileFormat = None
if hasattr(datafile,'datafileFormat'): fileFormat = datafile.datafileFormat

formatName = "(none)"
formatType = "(none)"
if fileFormat:
    formatName = fileFormat.name
    if hasattr(fileFormat,'type'): formatType = fileFormat.type

doi = None
if hasattr(datafile,'doi'): doi = datafile.doi

# TODO: create/mod times are being converted to strings "too early"; ignore them for now

createTime = None
# if hasattr(datafile,'createTime'): createTime = datafile.createTime

modTime = None
# if hasattr(datafile,'modTime'): modTime = datafile.modTime

datasetName = datafile.dataset.name

# Report (some of) what we've found

print "File name: ", filename, "in dataset", datasetName, " format: ", formatName, " (", formatType, ")"
print "Description:", fileDesc, "doi:", doi, "Created:", createTime, "Modified:", modTime

# Get datafile contents into local temp file

try:
    fDesc, fName = tempfile.mkstemp()
    f = os.fdopen(fDesc, "w")
    resp = session.idsClient.getData(sessionId, datafileIds=[datafileId])
    chunk = resp.read(2048)
    while chunk:
        f.write(chunk)
        chunk = resp.read(2048)
    f.close()

except Exception as e:
    print "Exception raised during datafile extraction:", e
    terminate(e, 1)

# Create new copy of datafile in the target dataset

try:
    dfid = session.writeDatafile(fName, targetDataset, filename, fileFormat, fileDesc, doi, createTime, modTime)
    print "Written file", filename, "in dataset", targetDataset.name, "file id =", dfid

    targetDataset.complete = True
    session.update(targetDataset)
    os.unlink(fName)
                    
except Exception as e:
    print "Exception raised during datafile copy:", e
    # How do you delete a file? Following does not exist:
    # session.deleteDatafile(dfid)
    os.unlink(fName)
    terminate(e, 1)

print jobName, "completed."
