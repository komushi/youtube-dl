FROM python:alpine3.6

ENV EDGE_REPOSITORY=http://dl-cdn.alpinelinux.org/alpine/edge/main

RUN apk update --repository $EDGE_REPOSITORY \
	&& apk add ffmpeg --repository $EDGE_REPOSITORY \
	&& rm -rf /var/cache/apk/*

RUN pip install youtube-dl

RUN pip install boto3

ADD get_url.py /
ADD youtube_dl_array.py /
ADD s3_ul_array.py /


ENTRYPOINT [ "python", "./get_url.py" ]
