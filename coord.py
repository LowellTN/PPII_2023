import numpy as np
import pandas as pd
from pyproj import Proj, Transformer
tranformer = Transformer.from_crs('epsg:3857', 'epsg:4326')


def conv(t):
    return tranformer.transform(t[0], t[1])


db=pd.read_csv('sinoe-(r)-annuaire-des-decheteries-dma.csv')
# print(db.to_string())
# print(db.head(5))
# print(db.columns)
# print(db.index)
# print(db.dtypes)
# print(db[["GPS_Y", "GPS_X"]])
# print(db[db["GPS_X"].isnull()])

db['LATITUDE'] = np.nan
db['LONGITUDE'] = np.nan

for index, row in db.iterrows():
    gpsx = row['GPS_X'] 
    gpsy = row['GPS_Y'] 
    lat, long = conv((gpsx, gpsy))
    db.at[index, 'LATITUDE'] = lat
    db.at[index, 'LONGITUDE'] = long
# print(db)
db.to_csv('out.csv')
print(db['LONGITUDE'].isnull())

