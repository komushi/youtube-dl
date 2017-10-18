1. Build docker image

```
$ docker build -t "komushi/youtube-dl:alpine3.6" .
```

2. Build docker image

```
docker run --rm komushi/youtube-dl:alpine3.6 https://www.youtube.com/watch?v=PAujbeIvbfY

docker run --rm komushi/youtube-dl:alpine3.6 <youtube-url> <aws-key> <aws-secret>
```

3. Push to docker hub