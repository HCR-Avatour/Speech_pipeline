CONTAINER_NAME := my-container
TAG_NAME := latest

stop:
	@docker stop ${CONTAINER_NAME} || true && docker rm ${CONTAINER_NAME} || true
	
build:
	stop
    @docker build --tag=myimg:${TAG_NAME} .

run:
    @docker run -it --name ${CONTAINER_NAME} myimg:${TAG_NAME}
