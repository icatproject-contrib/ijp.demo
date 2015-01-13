#!/usr/bin/env python

# Names of ICAT entities used in the job scripts
# Expressions of form ${...} will be replaced from values in ijp.batch.scripts.properties during installation.
# Change these to match your ICAT instance

# Facility Name - used in create_datafile, copy_datafile
facilityName = "${facility.name}"

# Data format and version used in create_datafile
formatName = "${data.format.name}"
formatVersion = "${data.format.version}"
