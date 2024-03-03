#!/bin/bash

PWD=${PWD}
DOCKER_NETWORK_NAME='mde'
DOCKER_COMPOSE_FILE='docker-compose.yaml'


function createNetwork() {
  cmd="docker network ls | grep ${DOCKER_NETWORK_NAME}"
  eval $cmd
  retVal=$?
  if [ $retVal -ne 0 ]; then
    docker network create -d bridge ${DOCKER_NETWORK_NAME}
  else
    echo "docker network already exists ${DOCKER_NETWORK_NAME}"
  fi
}

function compose_up() {
  createNetwork
  docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans

}

function compose_down() {
  docker-compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans
}

function compose_restart() {
  compose_down && compose_up
}


case "$1" in
  compose_up)
    compose_up
  ;;
  compose_down)
    compose_down
  ;;
  compose_restart)
    compose_restart
  ;;
  *)
    echo $"Usage: $0 {compose_up | compose_down | compose_restart }"
  ;;
esac
