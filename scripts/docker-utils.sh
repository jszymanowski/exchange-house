#!/usr/bin/env bash

remove_docker_container() {
  local container_name="$1"

  if [ -z "$container_name" ]; then
    printf "Error: Container name is required\n" >&2
    return 1
  fi

  printf "\nRemoving existing container: %s\n" "$container_name"

  # Check if the container exists before stopping and removing it
  if docker ps -aq --filter "name=$container_name" | grep -q .; then
    docker stop "$container_name" >/dev/null 2>&1
    docker rm "$container_name" >/dev/null 2>&1
  else
    printf "Container %s does not exist or is already removed\n" "$container_name"
  fi
}

build_docker_image() {
  local image_name="$1"

  printf "\nBuilding image\n"
  docker build -t "$image_name" .
}

build_docker_container() {
  local image_name="$1"
  local container_name="$2"
  local host_port="$3"
  local container_port="$4"

  printf "\nBuilding container\n"
  if [ -f .env ]; then
    docker run -d --env-file .env -p "$host_port":"$container_port" --name "$container_name" "$image_name"
  else
    echo "Warning: .env file not found. Running container without environment variables."
    docker run -d -p "$host_port":"$container_port" --name "$container_name" "$image_name"
  fi
}

display_docker_container_info() {
  local image_name="$1"
  local container_name="$2"
  local host_port="$3"

  printf "\nBuilt:\n"
  echo "  - view at: http://localhost:$host_port"
  echo "  - view logs: docker logs $container_name"
  echo "  - open shell console: docker exec -it $container_name sh"
  echo "  - open shell console, instead of running container: docker run --rm -it $image_name sh"
  echo "  - stop container: docker stop $container_name"
  echo "  - remove container: docker rm $container_name"
  echo "  - remove image: docker rmi $image_name"
  echo "  - view running containers: docker ps"

  # Verify container is running
  if ! docker ps --filter "name=$container_name" --format '{{.Names}}' | grep -q "$container_name"; then
    printf "\nWARNING: Container %s is not running. Check logs with: docker logs %s\n" "$container_name" "$container_name"
  fi
}
