# 1. Use Case: all-in-one
Download and upload with all-in-one python logic

## 1-1. all-in-one local mode
### 1-1-1. Enter the all-in-one example folder
```
$ cd all-in-one
```

### 1-1-2. Set the environment variables
```
$ export AWS_ACCESS_KEY_ID=<aws-key>
$ export AWS_SECRET_ACCESS_KEY=<aws-secret>
$ export YOUTUBE_DESTINATION_BUCKET=<your-bucket>
$ export YOUTUBE_MAX_HEIGHT=<max-height>
```

### 1-1-3. Download a playlist or a movie
```
$ python youtube-dl-all-in-one.py https://www.youtube.com/watch?v=PAujbeIvbfY
```

## 1-2. all-in-one docker mode
### 1-2-1. Enter the all-in-one example folder
```
$ cd all-in-one
```

### 1-2-2. Build docker image

```
$ docker build -t "komushi/youtube-dl:all-in-one" .
```

### 1-2-3. Run

```
$ docker run -i -t -e AWS_ACCESS_KEY_ID=<aws-key> -e AWS_SECRET_ACCESS_KEY=<aws-secret> -e YOUTUBE_DESTINATION_BUCKET=<your-bucket> -e YOUTUBE_MAX_HEIGHT=<max-height> komushi/youtube-dl:all-in-one <youtube-url>
```

### 1-2-4. Optionally push to a docker image repositiory

```
$ docker push komushi/youtube-dl
```
