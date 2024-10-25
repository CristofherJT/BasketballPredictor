#Data manipulation library
import pandas as pd
#Lets us create and work with arrays of data
import numpy as np

#Will download nba_api to device
import os
os.system(f"{os.sys.executable} -m pip install nba_api")

import nba_api 

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

