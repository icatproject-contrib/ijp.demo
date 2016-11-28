#!/usr/bin/env python

from cat_utils import terminate, Session, IjpOptionParser
#import lsf_utils

import requests

usage = "usage: %prog dataset_id options"
parser = IjpOptionParser(usage)

(options, args) = parser.parse_args()

# at this point, you would do the job

# any outputs would be recorded into a provenance record in ICAT using ijp

# the ID for the provenance record in ICAT is, as shown below, sent to ijp to be recorded
provId = 1;

url = options.ijpUrl + '/ijp/rest/jm/job/provenance/' + options.ijpJobId
payload = {'provenanceId': provId, 'sessionId': options.sessionId}

requests.post(url, data=payload, verify=False)
