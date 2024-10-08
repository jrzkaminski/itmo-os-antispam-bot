FROM python:3.9-slim as downloader

ARG HUGGINGFACE_TOKEN

ENV HF_HOME ${HF_HOME}

ENV TELEGRAM_BOT_TOKEN ${TELEGRAM_BOT_TOKEN}

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/jrzkaminski/itmo-os-antispam-bot.git .

RUN pip install --no-cache-dir huggingface_hub
RUN echo "$HUGGINGFACE_TOKEN"
RUN sh -c 'echo "$HUGGINGFACE_TOKEN" > /tmp/token.txt' && \
    HG_TOKEN=$(cat /tmp/token.txt) && \
    huggingface-cli login --token $HG_TOKEN && \
    huggingface-cli download NeuroSpaceX/ruSpamNS_v1 && \
    rm /tmp/token.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=downloader /app ./

RUN apt-get update && apt-get install -y \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/sh", "-c", "python itmo_antispam_bot/rubert_bot.py > server.log 2>&1"]