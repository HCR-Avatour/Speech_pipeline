FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
       python3.11 \
       python3-pip \
       git \
       curl \
       sudo

RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
RUN apt-get install ffmpeg -y

# Create the working directory
WORKDIR /

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /home/appuser/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN python3 -m pip install --upgrade pip
RUN --mount=type=cache,target=/home/appuser/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD python3 pipeline_server.py
