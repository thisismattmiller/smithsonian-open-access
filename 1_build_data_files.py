import glob
import bz2

with open('all_data.ndjson','w') as out:
  for div in glob.glob('./OpenAccess-master/metadata/objects/*'):
    print('Working on: ',div)
    for file in glob.glob(f'{div}/*'):
      with bz2.open(file, "rb") as f:
        out.write(f.read().decode())
