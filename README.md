# AstroBot 👾

This is my final project for Harvard's CS50x 2020

#### Video Demo: https://youtu.be/CD3tueGtBas

This is a Discord bot built for every space enthusiast and for every space-themed discord servers out there! You can use it to keep track of the upcoming launches and learn more about them, know who is currently in space and learn what is the phase of the moon right now!

I've built this bot as I was interested of learning more about REST APIs and how to use them. Also, I wanted for a long time to learn how to build a discord bot.
So, I combined my enthusiasm for space and all of the things I wanted to learn and I built this bot!

I'm currently using replit for uploading my code so the bot is on the cloud and not my local device.
While Developing this bot I used a lot of googling and saw that a lot of people use JavaScript to build Discord Bots. So, maybe I will try to build one using JavaScript in the future.

This bot is completely written using Python and it is built on some REST APIs to fetch information, which are:

- [NASA APOD API](https://github.com/nasa/apod-api/tree/d392c158aefe1625f902241699b4a5892f8a76f3)
- [Launch Library](https://lldev.thespacedevs.com/2.2.0/swagger)
- [Moon Phases API](https://www.farmsense.net/api/astro-widgets/)
- [ISS Current Location](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)
- [Reverse Geocoding](https://nominatim.org/release-docs/develop/api/Reverse/)

I've spent a lot of time to find a free API to show the current moon phase and I landed on the one that I mentioned in the list above.
But, I'm thinking of building a Moon Phases API myself in the near future, it sounds like a fun project for me.

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
