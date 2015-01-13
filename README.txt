A set of sample jobtypes and scripts (bash, python).

Run setup configure then edit the generated ijp.batch.scripts.properties file.

The jobtype XML files should be installed in an IJP server.
To do this, define ijp.jobtypes.dir in ijp.batch.scripts.properties and run setup install.

The scripts should be installed on each batch server that the IJP server may use to execute the jobs.
To do this, define ijp.scripts.dir in ijp.batch.scripts.properties and run setup install.

