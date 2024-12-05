from core.general import *
from lib import repeater as rp
import lib.mlb

# ouob

# info(lib.mlb.main())

info(rp.repeat(read_from_file('headers.yaml')).text)
