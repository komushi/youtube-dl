----
## Get in the serverless directory
```
$ cd aws-batch-example/serverless-youtube-dl
```

## Install serverless framework
```
$ npm install serverless -g
$ npm install serverless-step-functions
$ npm install serverless-pseudo-parameters
```

## Install libraries
```
$ pip install -t vendored/ -r requirements.txt
```

## Deploy
```
$ serverless deploy
```

## Run
```
$ curl -X POST https://<restapi_id>.execute-api.<region>.amazonaws.com/dev/youtube-dl -d '{"url":"https://www.youtube.com/playlist?list=PLxeJ9A111coroEJyNYTrR7BR2_pY16_Kv"}'
```