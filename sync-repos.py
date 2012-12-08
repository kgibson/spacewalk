#!/usr/bin/python
import os
import sys

sys.path.append('/usr/share/rhn')
try:
   from spacewalk.server import rhnSQL
   from spacewalk.common.rhnConfig import initCFG, CFG
except:
   print "Couldn't load needed libs, Are you sure you are running this on a satellite?"
   sys.exit(1)

initCFG()

db_string = CFG.DEFAULT_DB 
rhnSQL.initDB(db_string)

query = """ select C.id, C.name, C.label, CS.source_url
               from rhnChannel C inner join 
                    rhnChannelContentSource CCS on CCS.channel_id = C.id inner join
                    rhnContentSource CS on CS.id = CCS.source_id"""

h = rhnSQL.prepare(query)
h.execute()
list = h.fetchall_dict()

for row in list:
    sync_command="spacewalk-repo-sync --type=yum  --url='%s' --channel='%s'" % (row['source_url'], row['label'] )
    print sync_command
    os.system(sync_command)
