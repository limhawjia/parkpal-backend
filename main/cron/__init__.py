import os
import sys

MetadataQueryLimit = int(os.environ.get('QUERY_LIMIT', None))

if MetadataQueryLimit is None:
    MetadataQueryLimit = sys.maxsize
    print(f"QUERY_LIMIT not set, defaulting to max size: {MetadataQueryLimit}")
