# ParkPal Backend

This repository contains the backend required to support ParkPal, a mobile application that provides users with real-time parking information in Singapore. It consists of multiple services -- a web api, a data pulling service and a database.

These services can be easily deployed to any server running docker using docker swarm and docker compose after some configuration. 

## Web api

The web api provides endpoints for users to query information about collated parking information in Singapore.

## Data pulling service

The data pulling service consists of a few scripts to pull and normalize carpark information from various providers in Singapore. Upon startup, the docker container is configured to first retrieve the meta-data of the carparks. Subsequently, cron jobs will be run to pull data about lot availability regularly.

## Current support

The backend is currently only able to provide information about public carparks in Singapore from three providers -- URA, LTA and HDB.

The web api currently provides a single end point for users to query nearby carparks based on their current location and a search radius.

## Quickstart
To be updated.

## Technologies

* Python
* Flask
* Docker

## Testing

We are currently in the midst of creating more extensive tests.

## FAQs
To be updated.
