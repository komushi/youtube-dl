## Batch Process Flow by AWS Step Functions
![Step Functions Definition](images/flow.png)


----
## Get in the serverless directory
```
$ cd aws-array-jobs-example/serverless-youtube-dl-array
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

## Prepare the s3 bucket
* [Create an s3 bucket to store converted videos on aws console](https://s3.console.aws.amazon.com/s3/home)
* Modify serverless.yml at provider.environment.YOUTUBE_DESTINATION_BUCKET with the created s3 bucket name

## Prepare the batch compute environment
* [Create a batch compute environment](https:/console.aws.amazon.com/batch/home#/compute-environments)
* Modify serverless.yml at provider.environment.COMPUTE_ENVIRONMENT with the created batch compute environment name

## Deploy
```
$ serverless deploy
```

## Run
```
$ curl -X POST https://<restapi_id>.execute-api.<region>.amazonaws.com/dev/youtube-dl-array -d '{"url":"https://www.youtube.com/playlist?list=PLxeJ9A111coroEJyNYTrR7BR2_pY16_Kv"}'
```

curl -X POST https://g66g87ekpi.execute-api.ap-northeast-1.amazonaws.com/dev/youtube-dl-array -d '{"url":"https://www.youtube.com/playlist?list=PLxeJ9A111coroEJyNYTrR7BR2_pY16_Kv"}'