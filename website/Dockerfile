FROM python:3.10
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    bzip2 \
    libx11-xcb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz -O /tmp/geckodriver.tar.gz; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "./app.py"]
