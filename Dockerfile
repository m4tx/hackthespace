FROM docker.io/library/rust:1.87 AS builder
WORKDIR /usr/src/hackthespace
COPY . .
RUN cargo install --path . --locked

FROM docker.io/library/debian:12-slim
COPY --from=builder /usr/local/cargo/bin/hackthespace /usr/local/bin/hackthespace
RUN mkdir /app

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends tini=0.19.* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["hackthespace", "-l", "0.0.0.0:8000"]
EXPOSE 8000
