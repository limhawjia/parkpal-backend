# ParkPal Backend

This repository contains the backend required to support ParkPal, a mobile application that provides users with real-time parking information in Singapore. It consists of multiple services -- a web api, a data pulling service and a database.

These services can be easily deployed to any server running Docker using Docker swarm and Docker compose after some configuration. 

## Web api

The web api provides endpoints for users to query information about collated parking information in Singapore.

## Data pulling service

The data pulling service consists of a few scripts to pull and normalize carpark information from various providers in Singapore. Upon startup, the Docker container is configured to first retrieve the meta-data of the carparks. Subsequently, cron jobs will be run to pull data about lot availability regularly.

## Current support

The backend is currently only able to provide information about public carparks in Singapore from three providers -- URA, LTA and HDB.

The web api currently provides a single end point for users to query nearby carparks based on their current location and a search radius.

## Quickstart

The various services can be deployed easily to a server that runs Docker. Simply copy the folders `docker`, `main`, `scripts` along with `requirements.txt`, `docker-compose.yml` and `docker-compose.staging.yml` into your server. This can be done manually or through a deployment pipeline. Afterwards, you can choose to use `docker-compose` or `docker swarm` to automatically spin up the respective containers for the various services. 

Note that if you choose to use `docker swarm`, you would have to build the respective Docker images first and use `docker-compose.staging.yml` as it does not support build contexts in the compose file. More information can be found on Docker's [official documentation](https://docs.docker.com/).

As our services rely on certain third party applications and apis, there a few secrets that have to be injected into the Docker containers through environment variables. Make sure that you have these environment variables set in your server:

* `URA_API_ACCESS_KEY` - can be obtained through URA's [map site](https://www.ura.gov.sg/maps/api/)
* `LTA_API_ACCESS_KEY` - can be obtained through LTA's [DataMall](https://www.mytransport.sg/content/mytransport/home/dataMall.html)
* `GOOGLE_GEOCODING_API_KEY` - your own api key for Google's geocoding services

Here are optional variables that can be set based on your preferences:

* `CRON_FREQUENCY` - the frequency at which to update lot availability (in minutes 0 - 59)
* `QUERY_LIMIT` - the maximum number of carparks to be stored from each provider.

## Technologies

* Python
* Flask
* Docker

## Testing

We are currently in the midst of creating more extensive tests.

## FAQs
To be updated
