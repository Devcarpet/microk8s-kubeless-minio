import os
import time


from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import requests

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_API_URL = os.environ.get("MINIO_API_URL")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")

UNSPLASH_URL = 'https://api.unsplash.com'
UNSPLASH_SEARCH = \
    '%s/search/photos?client_id=%s&page=1&query=' % \
    (UNSPLASH_URL, UNSPLASH_ACCESS_KEY)


def upload_image(query):
    url = "%s%s" % (UNSPLASH_SEARCH, query)
    print(url)
    c = (requests.get(url).json()['results'])
    durl = (c[0]['urls']['regular'])

    print(durl)

    new_filename = "%s_%s.jpg" % (query, int(time.time()))

    r = requests.get(durl)
    with open('/tmp/%s'%new_filename, 'wb') as f:
        f.write(r.content)

    print("WROTE %s", MINIO_ACCESS_KEY)

    minioClient = Minio(MINIO_API_URL,
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)
    print("WROTE BEFORE TRY")
    return(new_filename)
    
    try:
        minioClient.make_bucket("devcarpettest")
    except BucketAlreadyOwnedByYou as err:
        print("Already")
        pass
    except BucketAlreadyExists as err:
        print("Already")    
    except ResponseError as err:
        print("FUUUUUUUUCK")

        raise
    else:
        print("Bucket ok")
    try:
        minioClient.fput_object(
            'devcarpettest', new_filename, '/tmp/%s' % new_filename)
        print("uploaded", new_filename)
    except ResponseError as err:
        print(err)

    return(new_filename)
    
def hello(event, context):
    return upload_image("Deer")



if __name__=="__main__":
    import sys
    upload_image(sys.argv[1])

