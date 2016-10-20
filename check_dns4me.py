#!/usr/bin/env python

###
### checkdns4me.py
###
### utility script which checks if the dns4me api version has changed and triggers a download script
### designed to run as a daemon
### may suit other similar purposes
###
### Provided as-is where-is.  Use at your own risk + please don't ask me for support :)
###
### Copyright 2016 Dan Capper <dan@hopfulthinking.com>
###
### Licensed under the Apache License, Version 2.0 (the "License");
### you may not use this file except in compliance with the License.
### You may obtain a copy of the License at
###
###    http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing, software
### distributed under the License is distributed on an "AS IS" BASIS,
### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
### See the License for the specific language governing permissions and
### limitations under the License.
###

from urllib import urlopen
from time import sleep
from subprocess import call
import syslog

### Set these as you require ###

watchurl = "https://dns4me.net/api/v2/get_hosts_file_version/0abcdef1-1000-1000-1000-101010101010"
# obtain version api url from https://dns4me.net/user/hosts_file
# with a bit of imagination, this script could look for any url content to change...

sleep = 60                                                      # how long between checks?
debug = False                                                   # set true for extra syslog
onchange = "/usr/bin/perl /usr/local/bin/unbound-dns4me.pl"     # call if changed
postchange = "/bin/systemctl restart unbound"                   # call after change

### Don't edit below this line ###

urllines = ''
oldurllines = ''
while True:
    if debug: syslog.syslog(syslog.LOG_INFO, 'Opening url: [%s]' % watchurl)
    try:
        urlfile = urlopen(watchurl)
        urllines = urlfile.readlines()
        if urllines != oldurllines:
            oldurllines = urllines
            syslog.syslog(syslog.LOG_INFO, 'version has changed or first run - call [{0}]'.format(onchange))
            call(explode(onchange, ' '))
            syslog.syslog(syslog.LOG_INFO, 'post change - call [{0}]'.format(postchange))
            call(explode(postchange, ' '))
        elif debug: syslog.syslog(syslog.LOG_INFO, 'no change detected')
    except IOError: syslog.syslog(syslog.LOG_WARNING, 'Unable to open URL [{0}]'.format(watchurl))
    if debug: syslog.syslog(syslog.LOG_INFO, 'sleep for {0}s'.format(sleep))
    sleep(sleep)
