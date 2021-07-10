from google.cloud import storage

def list_blobs_by_extension(bucket, extension, prefix=None):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    for blob in blobs:
        if blob.name.endswith(extension):
          yield blob
