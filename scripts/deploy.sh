#!/bin/bash

scp -i ./credentials -o StrictHostKeyChecking=no -pr "$(pwd)" "$HOST_NAME":~/
ssh -i ./credentials -o StrictHostKeyChecking=no "$HOST_NAME" cd ParkPalBackend && docker-compose build
ssh -i ./credentials -o StrictHostKeyChecking=no "$HOST_NAME" docker container stop "$(docker container ls -aq)"
ssh -i ./credentials -o StrictHostKeyChecking=no "$HOST_NAME" docker swarm init || true
ssh -i ./credentials -o StrictHostKeyChecking=no "$HOST_NAME" docker stack deploy --compose-file ./ParkPalBackend/docker-compose.staging.yml ParkPal
