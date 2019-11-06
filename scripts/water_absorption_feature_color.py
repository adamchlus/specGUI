from os.path import expanduser
home = expanduser("~")
import pandas as pd 


water = pd.read_csv("%s/Dropbox/projects/specGUI/data/water_absorption.csv" % home,index_col =0)
f = interpolate.interp1d(water.index.values, water['abs'])
water = pd.Series(f(range(350,2501)),range(350,2501))
water = water**.25
blue =  (water-water.min())/(water.max()-water.min())


blue.to_csv("%s/Dropbox/projects/specGUI/data/water_absorption_blues.csv" % home)