# 2. Use Case: dl-convert-ul
Download, convert and upload with separated python scripts

## 2-1. dl-convert-ul local mode
### 2-1-1. Enter the dl-convert-ul example folder
```
$ cd dl-convert-ul
```

### 2-1-2. Set the environment variables
```
$ export AWS_ACCESS_KEY_ID=<aws-key>
$ export AWS_SECRET_ACCESS_KEY=<aws-secret>
$ export YOUTUBE_DESTINATION_BUCKET=<your-bucket>
$ export YOUTUBE_MAX_HEIGHT=<max-height>
```

### 2-1-3. Download a playlist or a movie
```
$ python youtube-dl.py https://www.youtube.com/watch?v=PAujbeIvbfY
```

## 2-2. dl-convert-ul docker mode
### 2-2-1. Enter the dl-convert-ul example folder
```
$ cd dl-convert-ul
```

### 2-2-2. Build docker image

```
$ docker build -f ./Dockerfile -t komushi/youtube-dl:dl-convert-ul-array .
```

### 2-2-3. Run

```
$ docker run -i -t -e AWS_ACCESS_KEY_ID=<aws-key> -e AWS_SECRET_ACCESS_KEY=<aws-secret> -e YOUTUBE_DESTINATION_BUCKET=<your-bucket> -e YOUTUBE_MAX_HEIGHT=<max-height> komushi/youtube-dl:dl-convert-ul-array <youtube-url>
```

### 2-2-4. Optionally push to a docker image repositiory

```
$ docker push komushi/youtube-dl
```