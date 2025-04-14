#!/bin/bash

remove_docker_container() {
  local container_name="$1"

  echo "\nRemoving existing container: $container_name"

  # Check if the container exists before stopping and removing it
  if docker ps -aq --filter "name=$container_name" | grep -q .; then
    docker stop "$container_name" >/dev/null 2>&1
    docker rm "$container_name" >/dev/null 2>&1
  fi
}

build_docker_image() {
  local image_name="$1"

  echo "\nBuilding image"
  docker build -t $image_name .
}

build_docker_container() {
  local image_name="$1"
  local container_name="$2"
  local host_port="$3"
  local container_port="$4"

  echo "\nBuilding container"
  docker run -d -p $host_port:$container_port --name $container_name $image_name
}

display_docker_container_info() {
  local image_name="$1"
  local container_name="$2"
  local host_port="$3"

  echo "\nBuilt:"
  echo "  - view at: http://localhost:$host_port"
  echo "  - view logs: docker logs $container_name"
  echo "  - open shell console: docker exec -it $container_name sh"
  echo "  - open shell console, instead of running container: docker run --rm -it $image_name sh"
  echo "  - stop container: docker stop $container_name"
  echo "  - remove container: docker rm $container_name"
  echo "  - remove image: docker rmi $image_name"
  echo "  - view running containers: docker ps"
}
