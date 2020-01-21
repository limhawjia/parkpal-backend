import os

MetadataQueryLimit = int(os.environ.get('QUERY_LIMIT', None) or exit('QUERY_LIMIT environment variable not defined.'))
