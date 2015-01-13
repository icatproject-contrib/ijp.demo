A set of sample jobtypes and scripts (bash, python) to demonstrate the ICAT Job Portal.

Run setup configure then edit the generated demojobs.properties file.

The jobtype XML files should be installed in an IJP server.
To do this, define ijp.jobtypes.dir in demojobs.properties and run setup install.

The scripts should be installed on each batch server that the IJP server may use to execute the jobs.
To do this, define ijp.scripts.dir in demojobs.properties and run setup install.

