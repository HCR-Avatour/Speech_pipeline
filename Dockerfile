FROM ubuntu:latest 
# dustynv/langchain:samples-r36.2.0

SHELL ["/bin/bash", "-c"]
# RUN cat /etc/os-release && false
ENV DEBIAN_FRONTEND=noninteractive
# RUN echo "Etc/UTC" > /etc/timezone

RUN apt-get update \
    && apt-get upgrade -y 
RUN apt install -y \
       python3 \
       python3-pip 
# RUN python3 --version && false
RUN apt-get install -y \
       git \
       curl \
       sudo \
       wget \
       cmake build-essential 

# RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
RUN apt-get install ffmpeg -y

# Create the working directory
WORKDIR /work
# Copy the source code into the container.
# COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt


# Expose the port that the application listens on.
EXPOSE 5005
# # Expose the IP address of the server
# ENV SERVER_IP=localhost

# Run the application.
# CMD python3 pipeline_server.py -u
CMD ["bash", "-c", "python3 pipeline_server.py -u"]
# CMD ["bash", "-c"]
RUN apt install -y nano

# docker compose up --build
