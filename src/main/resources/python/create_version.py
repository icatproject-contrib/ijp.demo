#!/usr/bin/env python

# Create a new version of a dataset
# usage: create_version <datasetId> options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl> --name=<filename> 
# optional: --comment=<string>

# This script requires both vicat and the icat RESTful client to be available
# (At present, this means that vicat.py must be in the same directory)

import sys
import os
import logging
import tempfile

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import terminate, Session, IjpOptionParser

from icat_defs import facilityName, formatName, formatVersion

# vicat uses the REST client, so import that
import icat

from vicat import VICAT

# Location of the ICAT server certificate (for the RESTful client)
ICAT_CERT="/opt/ijp/bin/icat-cert.rfc"

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

parser.add_option("--name", dest="newName",
                  help="name for new version of dataset")
parser.add_option("--comment", dest="versionComment",
                  help="comment giving reason for this version")

(options, args) = parser.parse_args()

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

if not options.newName:
    terminate(jobName + " must specify a new name", 1)

# Comment is optional (for now), though IJP will probably always provide a (possibly empty) value
# if not options.versionComment:
#     terminate(jobName + " must supply a version comment", 1)
   
datasetId = int(datasetId)

# This is the SUDS-based client that is used by most of the jobscript machinery.

session = Session(facilityName, options.icatUrl, options.idsUrl, sessionId)

dataset = session.get("Dataset INCLUDE DatasetType", datasetId)

restIcat = icat.ICAT(options.icatUrl,ICAT_CERT)
restSession = icat.Session(restIcat,sessionId)
# Use the hard-wired facilityName from icat_defs (in turn from ijp.demo configuration)
fids = restSession.search("SELECT f.id FROM Facility f WHERE f.name = '" + facilityName + "'")
if len(fids) == 1:
    facilityId = fids[0]
else:
    raise Exception("Can't find a Facility called " + facilityName)

vicat = VICAT(restSession, facilityId)
newdsid = vicat.createVersion(datasetId,options.newName,options.versionComment)
print "Created new version of dataset", dataset.name, "new name:", options.newName, "new id =", newdsid

print jobName, "completed."
