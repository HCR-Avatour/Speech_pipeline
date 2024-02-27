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
WORKDIR /work
# Copy the source code into the container.
COPY . .

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /home/appuser/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt



# Expose the port that the application listens on.
EXPOSE 5005
# # Expose the IP address of the server
# ENV SERVER_IP=localhost

# Run the application.
# CMD python3 pipeline_server.py -u
# CMD ["bash", "-c", "python3 pipeline_server.py -u"]
CMD ["bash", "-c"]


# docker compose up --build


# FOR ARM chip (on JETSON) -  WILL NEVER WORK ON ARM (GPT4ALL & Vulkan does not support ARM)
# FROM ubuntu:latest

# SHELL ["/bin/bash", "-c"]
# # RUN cat /etc/os-release && false

# RUN apt-get update \
#     && apt-get upgrade -y \
#     && apt-get install -y \
#        python3.11 \
#        python3-pip \
#        git \
#        curl \
#        sudo \
#        wget \
#        cmake build-essential 

# RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
# RUN apt-get install ffmpeg -y

# # Create the working directory
# WORKDIR /work
# # Copy the source code into the container.
# COPY . .

# RUN wget -qO- https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo tee /etc/apt/trusted.gpg.d/lunarg.asc \
#     && sudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-jammy.list http://packages.lunarg.com/vulkan/lunarg-vulkan-jammy.list \
#     && sudo apt update \
#     && sudo apt install vulkan-sdk

# # Build GPT4ALL on ARM
# RUN git clone --recurse-submodules https://github.com/nomic-ai/gpt4all.git \
#     && cd gpt4all/gpt4all-backend \
#     && cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo \
#     && cmake --build build --parallel \
#     && cd ../../gpt4all-bindings/python \
#     && pip install -e .


# # Download dependencies as a separate step to take advantage of Docker's caching.
# # Leverage a cache mount to /home/appuser/.cache/pip to speed up subsequent builds.
# # Leverage a bind mount to requirements.txt to avoid having to copy them into
# # into this layer.
# RUN python3 -m pip install --upgrade pip
# RUN python3 -m pip install -r requirements.txt



# # Expose the port that the application listens on.
# EXPOSE 5005
# # # Expose the IP address of the server
# # ENV SERVER_IP=localhost

# # Run the application.
# # CMD python3 pipeline_server.py -u
# # CMD ["bash", "-c", "python3 pipeline_server.py -u"]
# CMD ["bash", "-c"]


# # docker compose up --build
