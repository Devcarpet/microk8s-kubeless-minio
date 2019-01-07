```
kubeless function  deploy up \ 
  --runtime python3.6 --from-file up.py \ 
  --dependencies requirements.txt --handler up.hello \ 
  --env MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY \ 
  --env MINIO_SECRET_KEY=$MINIO_SECRET_KEY \ 
  --env MINIO_API_URL=$MINIO_API_URL \  
  --env UNSPLASH_ACCESS_KEY=$UNSPLASH_ACCESS_KEY
```
