#!/bin/bash

scp -i ./credentials -o StrictHostKeyChecking=no -pr "$(pwd)" ubuntu@ec2-54-255-145-37.ap-southeast-1.compute.amazonaws.com:~/
ssh -i ./credentials -o StrictHostKeyChecking=no ubuntu@ec2-54-255-145-37.ap-southeast-1.compute.amazonaws.com cd ParkPalBackend && docker-compose build
ssh -i ./credentials -o StrictHostKeyChecking=no ubuntu@ec2-54-255-145-37.ap-southeast-1.compute.amazonaws.com docker container stop $(docker container ls -aq)
ssh -i ./credentials -o StrictHostKeyChecking=no ubuntu@ec2-54-255-145-37.ap-southeast-1.compute.amazonaws.com docker swarm init || true
ssh -i ./credentials -o StrictHostKeyChecking=no ubuntu@ec2-54-255-145-37.ap-southeast-1.compute.amazonaws.com docker stack deploy --compose-file ./ParkPalBackend/docker-compose.staging.yml ParkPal


