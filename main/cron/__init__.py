import os
import sys

if os.environ.get('QUERY_LIMIT', '') == '':
    MetadataQueryLimit = sys.maxsize
    print(f"QUERY_LIMIT not set, defaulting to max size: {MetadataQueryLimit}")
else:
    MetadataQueryLimit = int(os.environ['QUERY_LIMIT'])
