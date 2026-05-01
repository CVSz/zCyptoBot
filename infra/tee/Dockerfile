FROM gramineproject/gramine:latest

COPY app /app
WORKDIR /app

ENTRYPOINT ["gramine-sgx", "./app"]
