1. Build docker image

```
$ docker build -t "komushi/youtube-dl:alpine3.6" .
```

2. Push to docker hub
```
$ docker push komushi/youtube-dl
```

3. Run

```
docker run --rm komushi/youtube-dl:alpine3.6 https://www.youtube.com/watch?v=PAujbeIvbfY

docker run --rm komushi/youtube-dl:alpine3.6 <youtube-url> <aws-key> <aws-secret>
```
