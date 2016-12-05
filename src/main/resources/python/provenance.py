#!/usr/bin/env python

import sys
import os
import datetime

from cat_utils import terminate, Session, IjpOptionParser
from icat_defs import facilityName

import requests

# Hard-wired values that this script expects to exist in ICAT
# - may need to be changed
#
DATASET_TYPE="TestDatasetType"
APPLICATION="ProvenanceTest"
APPLICATION_VERSION="1"

usage = "usage: %prog dataset_id options"
parser = IjpOptionParser(usage)

parser.add_option("--out-dataset-name", dest="datasetName",
                 help="Name for generated dataset")

(options, args) = parser.parse_args()

jobName = os.path.basename(sys.argv[0])

if not options.sessionId:
    terminate(jobName + " must specify an ICAT session ID", 1)

if not options.icatUrl:
    terminate(jobName + " must specify an ICAT url", 1)

if not options.idsUrl:
    terminate(jobName + " must specify an IDS url", 1)

if not options.datasetIds:
    terminate(jobName + " must supply a dataset ID", 1)

# Check that it's only a single ID, not a list

if len(options.datasetIds.split(',')) > 1:
    terminate(jobName + ': expects a single datasetId, not a list: ' + options.datasetIds)

datasetId = int(options.datasetIds)

if not options.datasetName:
    datasetName = "OutputDataset1"
else:
    datasetName = options.datasetName

session = Session(facilityName, options.icatUrl, options.idsUrl, options.sessionId)

# Find the input dataset

input_dataset = session.get("Dataset INCLUDE Investigation", datasetId)
investigation = input_dataset.investigation

# Create an output dataset

dataset = session.factory.create("dataset")
dataset.investigation = investigation
dataset.name = datasetName
dataset.type = session.getDatasetType(DATASET_TYPE)
dataset.startDate = dataset.endDate = datetime.datetime.today()

# Create the dataset in ICAT - return code 2 if it already exists
try:
    dataset.id = session.create(dataset)
    print "Dataset id:", dataset.id, "created with name", dataset.name
except WebFault as e:
    icatException = e.fault.detail.IcatException
    if icatException.type == "OBJECT_ALREADY_EXISTS":
        terminate(icatException.message, 2)
    else:
        terminate(icatException.type + ": " + icatException.message, 1)

try:
    dataset.complete = True
    session.update(dataset)
except Exception as e:
    session.deleteDataset(dataset)
    terminate(e, 1)
    
# Store the provenance in ICAT, and supply the ijpUrl and ijpJobId
# so that it can be linked to and viewed from the job in the IJP

application = session.getApplication(APPLICATION, APPLICATION_VERSION)
arguments = "--datasetIds="+str(datasetId)+" --out-dataset-name="+datasetName
provId = session.storeProvenance(application,arguments,ids=[input_dataset],ods=[dataset], ijpUrl=options.ijpUrl, ijpJobId=options.ijpJobId);

print "Provenance record id = ", provId, " created in ICAT", " for job ", options.ijpJobId
