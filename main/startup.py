from main.cron.hdb import hdb_metadata
from main.cron.ura import ura_metadata
from main.cron.lta import lta_metadata

hdb_metadata.start()
ura_metadata.start()
lta_metadata.start()
