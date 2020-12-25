# Databases-Advanced-Docker


This projcte has been created for fetching bitcoins transactions data and store them to mongodb.

to do this we have created an image for each task.

- Scraper container: scrpaes transactions every 60sec and sends them to redis to be cached.
- Redis container: receives all the transactions every last minute.
- Parser container: gets transactions from redis fillter the top one then insert it to mongodb.
- Mongodb container: this documented database to store our highest transaction.


A Docker container image is a lightweight, standalone, executable package of softwarethat includes everything needed to run an application: 
code,runtime, system tools, system libraries and settings.

by using docker 

> we don't to worry about running another OS on top of yours.
> we will be able to wrap eaxh application into it's container
> easy to pull images and use them 
