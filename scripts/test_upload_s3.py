import sys
import os
from api.tasks import s3

file_loc = sys.argv[1]

s3.upload_file(file_loc, os.getenv('BUCKETEER_BUCKET_NAME'), file_loc)