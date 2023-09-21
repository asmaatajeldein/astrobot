# AstroBot 👾

This is my final project for Harvard's CS50x 2021

#### Video Demo: https://youtu.be/CD3tueGtBas

This is a Discord bot built for every space enthusiast and for every space-themed discord server out there! You can use it to keep track of the upcoming launches and learn more about them, know who is currently in space and learn what is the phase of the moon right now!

This bot is completely written using Python and and a bunch of REST APIs to fetch information:

- [NASA APOD API](https://github.com/nasa/apod-api/tree/d392c158aefe1625f902241699b4a5892f8a76f3)
- [Launch Library](https://lldev.thespacedevs.com/2.2.0/swagger)
- [Moon Phases API](https://www.farmsense.net/api/astro-widgets/)
- [ISS Current Location](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)
- [Reverse Geocoding](https://nominatim.org/release-docs/develop/api/Reverse/)

## Libraries and Packages Needed:

- discord
- os
- dotenv
- requests
- datetime
- time
- python-dateutil

## A List of All the Available Commands and Their Arguments:

`$apod`
views the astronomy picture of the day.

`$apod [yyyy-mm-dd]`
views the astronomy picture of the specified day.

`$launches`
gets information about 10 of the upcoming launches.

`$nextlaunch` or `$nl`
fetches information about the next rocket launch.

`$nextlaunch [offset]` or `$nl [offset]`
fetches information about the specified rocket launch.

`$astronauts`
gets the current people in space.

`$iss`
gets the current location of the international space station.

`$moon`
gets information about the moon.

## Files

- `requirements.txt` a list of the packages and libraries required for this bot
- `app/main.py` this is where the main code for the bot is
- `app/moon-phases` this folder contains pictures of every phase of the moon

## Possible Features to Add

This is a list of things i want to add to my bot in the future

- Add a command to show information about the planets of the solar system
- Add a command to view launches of SpaceX only
- Add a command to give a list of the latest space related news
- Add a command to keep track of the weather on Mars
