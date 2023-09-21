import datetime
import os
import time

import discord
import requests
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="$", help_command=None, intents=intents)

timenow = datetime.datetime.utcnow()


def embed_footer(ctx, embed):
    """
    embeds a footer to every message.
    """
    embed.set_footer(
        text=f"Requested by {ctx.message.author.name}",
        icon_url=ctx.author.avatar,
    )


def countdown_for(launch):
    """
    calculates the countdown for launch
    """
    launch_net = launch["net"]
    now = datetime.datetime.now()
    launch_time = datetime.datetime.strptime(launch_net, "%Y-%m-%dT%H:%M:%SZ")
    diff = relativedelta(launch_time, now)

    return diff


moon_phases = {
    "New Moon": {
        "Image": "app/moon-phases/new-moon.jpg",
        "Emoji": "🌑",
        "Description": (
            "This is the invisible phase of the Moon, with the illuminated"
            " side of the Moon facing the Sun and the night side facing Earth."
            " In this phase, the Moon is in the same part of the sky as the"
            " Sun and rises and sets with the Sun. Not only is the illuminated"
            " side facing away from the Earth, it's also up during the day!"
            " Remember, in this phase, the Moon doesn't usually pass directly"
            " between Earth and the Sun, due to the inclination of the Moon's"
            " orbit. It only passes near the Sun from our perspective on"
            " Earth."
        ),
    },
    "Waxing Crescent": {
        "Image": "app/moon-phases/waxing-crescent.jpg",
        "Emoji": "🌒",
        "Description": (
            "This silver sliver of a Moon occurs when the illuminated half of"
            " the Moon faces mostly away from Earth, with only a tiny portion"
            " visible to us from our planet. It grows daily as the Moon's"
            " orbit carries the Moon's dayside farther into view. Every day,"
            " the Moon rises a little bit later."
        ),
    },
    "First Quarter": {
        "Image": "app/moon-phases/first-quarter.jpg",
        "Emoji": "🌓",
        "Description": (
            "The Moon is now a quarter of the way through its monthly journey"
            " and you see half of its illuminated side. People may casually"
            " call this a half moon, but remember, that's not really what"
            " you're witnessing in the sky. You're seeing just a slice of the"
            " entire Moon ― half of the illuminated half. A first quarter moon"
            " rises around noon and sets around midnight. It's high in the sky"
            " in the evening and makes for excellent viewing."
        ),
    },
    "Waxing Gibbous": {
        "Image": "app/moon-phases/waning-gibbous.jpg",
        "Emoji": "🌔",
        "Description": (
            "Most of the Moon's dayside has come into view, and the Moon"
            " appears brighter in the sky."
        ),
    },
    "Full Moon": {
        "Image": "app/moon-phases/full-moon.jpg",
        "Emoji": "🌕",
        "Description": (
            "This is as close as we come to seeing the Sun's illumination of"
            " the entire day side of the Moon (so, technically, this would be"
            " the real half moon). The Moon is opposite the Sun, as viewed"
            " from Earth, revealing the Moon's dayside. A full moon rises"
            " around sunset and sets around sunrise. The Moon will appear full"
            " for a couple of days before it moves into Waning Gibbous."
        ),
    },
    "Waning Gibbous": {
        "Image": "app/moon-phases/waning-gibbous.jpg",
        "Emoji": "🌖",
        "Description": (
            "As the Moon begins its journey back toward the Sun, the opposite"
            " side of the Moon now reflects the Moon's light. The lighted side"
            " appears to shrink, but the Moon's orbit is simply carrying it"
            " out of view from our perspective. The Moon rises later and later"
            " each night."
        ),
    },
    "Last Quarter": {
        "Image": "app/moon-phases/last-quarter.jpg",
        "Emoji": "🌗",
        "Description": (
            "The Moon looks like it's half illuminated from the perspective of"
            " Earth, but really you're seeing half of the half of the Moon"
            " that's illuminated by the Sun ― or a quarter. A last quarter"
            " moon, also known as a third quarter moon, rises around midnight"
            " and sets around noon."
        ),
    },
    "Waning Crescent": {
        "Image": "app/moon-phases/waning-crescent.jpg",
        "Emoji": "🌘",
        "Description": (
            "The Moon is nearly back to the point in its orbit where its"
            " dayside directly faces the Sun, and all that we see from our"
            " perspective is a thin curve."
        ),
    },
}


@client.event
async def on_ready():
    """
    When the Bot starts running.
    """
    print(f"We have logged in as {client.user}")


@client.command()
async def apod(ctx, *args):
    """gets the astronomy picture of the day or any specified day."""

    # NASA API GET request
    # if there's no arguments
    if not args:
        response = requests.get(
            f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
        )

        # set the day to today
        day = datetime.datetime.now().date()

        read_more = "https://apod.nasa.gov/apod/astropix.html"

    # if there's a date argument
    elif len(args[0]) == 10:
        try:
            response = requests.get(
                f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={args[0]}"
            )

            # set the day to the day used to query
            day = datetime.datetime.strptime(args[0], "%Y-%m-%d").date()

            day_str = day.strftime("%y%m%d")

            read_more = f"https://apod.nasa.gov/apod/ap{day_str}.html"
        except Exception:
            await ctx.channel.send("Invalid command argument.")
            return

    else:
        await ctx.channel.send("Invalid command argument.")
        return

    response_json = response.json()

    # variables for the message
    if response_json["media_type"] == "image":
        hdurl = response_json["hdurl"]
    title = response_json["title"]
    explanation = response_json["explanation"]

    explanation_length = len(explanation)

    if explanation_length > 1024:
        explanation = (
            explanation[:901]
            + "..."
            + f"[Click Here to Read More]({read_more})"
        )

    embed = discord.Embed(
        title=f"🌌 **Astronomy Picture of the Day of {day}**",
        colour=0x2C3BA3,
        timestamp=timenow,
    )
    embed.add_field(name=f"**{title}**", value=f"{explanation}", inline=False)

    # if the url returned is a picture link
    if response_json["media_type"] == "image":
        url = response_json["url"]
        hdurl = response_json["hdurl"]
        embed.add_field(
            name="**Hi-Res Image**", value=f"[Click Here]({hdurl})"
        )
        embed.set_image(url=url)

    # if the url returned is a youtube link
    if response_json["media_type"] == "video":
        url = response_json["url"]
        embed.add_field(name="**Video Link**", value=f"[Click Here]({url})")

    embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


@client.command()
async def launches(ctx):
    """gets the upcoming 10 rocket launches."""

    url = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/"
    response = requests.get(url)
    response_json = response.json()

    launches = response_json["results"]

    x = 0
    results = []
    embed = 0
    for launch in launches:
        diff = countdown_for(launch)

        if (
            diff.seconds <= 0
            and diff.minutes <= 0
            and diff.hours <= 0
            and diff.days <= 0
        ):
            continue

        else:
            item = {}
            x = x + 1
            item["order"] = x
            item["launch_name"] = launch["name"]
            item["countdown"] = (
                f"{diff.days} days {diff.hours} hours {diff.minutes} minutes"
                f" {diff.seconds} seconds"
            )
            results.append(item)

        embed = discord.Embed(
            title=f"🚀 **Next {x} Launches**",
            colour=0x2C3BA3,
            timestamp=timenow,
        )

        for result in results:
            order = result["order"]
            launch_name = result["launch_name"]
            countdown = result["countdown"]
            embed.add_field(
                name=f"**{order}) {launch_name}**",
                value=f"**Time Untill Launch:** {countdown}",
                inline=False,
            )

            embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


@client.command(name="nextlaunch", aliases=["nl"])
async def nextlaunch(ctx, *args):
    """gets information about any of the upcoming launches."""

    offset = 0
    url = f"https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?limit=1&offset={offset}"

    if args:
        try:
            offset = int(args[0])

            if offset <= 10:
                url = f"https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?limit=1&offset={offset}"

            elif offset <= 0:
                await ctx.channel.send("Invalid offset.")
                return

            else:
                await ctx.channel.send(
                    "I can't find any launches with that offset."
                )
                return

        except Exception:
            await ctx.channel.send("Invalid command argument")
            return

    response = requests.get(url)
    response_json = response.json()

    result = response_json["results"][0]
    launch_name = result["name"]
    launch_status = result["status"]["name"]
    launch_date = datetime.datetime.strptime(
        result["net"], "%Y-%m-%dT%H:%M:%SZ"
    )
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    if result["mission"] is None:
        mission_name = "No mission name was provided"
        mission_description = "No mission description was provided"
        mission_type = "No mission type was provided"
        mission_orbit = "No mission orbit was provided"
    else:
        mission_name = result["mission"]["name"]
        mission_description = result["mission"]["description"]
        mission_type = result["mission"]["type"]
        mission_orbit = result["mission"]["orbit"]["name"]

    countdown = countdown_for(result)

    rocket_name = result["rocket"]["configuration"]["name"]
    rocket_id = result["rocket"]["configuration"]["id"]
    config_url = (
        f"https://lldev.thespacedevs.com/2.2.0/config/launcher/{rocket_id}/"
    )
    config_response = requests.get(config_url)
    config_response_json = config_response.json()
    manufacturer = config_response_json["manufacturer"]["name"]

    pad_name = result["pad"]["name"]
    pad_location = result["pad"]["location"]["name"]
    location_code = result["pad"]["location"]["country_code"]

    rocket_image = result["image"]

    embed = discord.Embed(
        title=f"🚀 **{launch_name}**",
        description=mission_description,
        colour=0x2C3BA3,
        timestamp=timenow,
    )

    embed.add_field(
        name="**Mission**",
        value=f"""
  **Name:** {mission_name}
  **Type:** {mission_type}
  **Orbit:** {mission_orbit}
  **Status:** {launch_status}
  **Date:** {weekdays[launch_date.weekday()]}, {launch_date.day} {launch_date.strftime('%b')} {launch_date.year} at {launch_date.strftime('%I')}:{launch_date.strftime('%M')} {launch_date.strftime('%p')}
  **Approximate Countdown:** {countdown.days} days {countdown.hours} hours {countdown.minutes} minutes {countdown.seconds} seconds
  """,
        inline=False,
    )

    embed.add_field(
        name="**Rocket**",
        value=f"""
  **Name:** {rocket_name}
  **Manufactured By:** {manufacturer}
  """,
        inline=False,
    )

    embed.add_field(
        name="**Launch Pad**",
        value=f"""
  **Name:** {pad_name}
  **Location:** {pad_location}
  **Country Code:** {location_code}
  """,
        inline=False,
    )

    embed.set_image(url=rocket_image)

    embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


@client.command()
async def astronauts(ctx):
    """gets the current astronauts in space."""

    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    response_json = response.json()

    number = response_json["number"]
    people = response_json["people"]

    embed = discord.Embed(
        title="👨‍🚀 **People Currently in Space**",
        description=(
            f"There are {number} people currently outside of the bounds of"
            " Earth's Atmosphere!"
        ),
        colour=0x2C3BA3,
        timestamp=timenow,
    )

    x = 0

    for person in people:
        x = x + 1
        name = person["name"]
        craft = person["craft"]

        embed.add_field(name=f"**{x}) {name}**", value=f"**Onboard:** {craft}")

    embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


@client.command()
async def moon(ctx):
    """gets information about the moon."""

    date_time = datetime.datetime.now()
    unix_time = int(time.mktime(date_time.timetuple()))

    url = f"https://api.farmsense.net/v1/moonphases/?d={unix_time}"

    response = requests.get(url)
    response_json = response.json()[0]

    name = response_json["Moon"][0]
    phase = response_json["Phase"]
    illumination = round(response_json["Illumination"], 3) * 100
    age = round(response_json["Age"], 2)
    moon_angle = round(response_json["AngularDiameter"], 2)

    emoji = moon_phases[phase]["Emoji"]
    image = moon_phases[phase]["Image"]
    description = moon_phases[phase]["Description"]

    file = discord.File(image, filename="image.jpg")

    embed = discord.Embed(
        title=f"{emoji} **The Moon of {datetime.datetime.now().date()}**",
        colour=0x2C3BA3,
        timestamp=timenow,
    )
    embed.add_field(
        name=f"**{name}**",
        value=(
            f"**Phase:** {phase}\n**Illumination: ** {illumination}%\n**Moon"
            f" Age:** {age}\n**Moon Angle:** {moon_angle}"
        ),
    )
    embed.add_field(
        name="**Phase Description**", value=f"{description}", inline=False
    )

    embed.set_image(url="attachment://image.jpg")
    embed_footer(ctx, embed)

    await ctx.send(file=file, embed=embed)


@client.command()
async def iss(ctx):
    """gets the current location of the international space station."""

    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    response_json = response.json()

    lat = float(response_json["iss_position"]["latitude"])
    lon = float(response_json["iss_position"]["longitude"])

    reverse_geocode_url = f"https://nominatim.openstreetmap.org/reverse?format=geojson&lat={lat}&lon={lon}"

    geocode_response = requests.get(reverse_geocode_url)
    geocode_response_json = geocode_response.json()

    embed = discord.Embed(
        title="🛰 **Current ISS Position**", colour=0x2C3BA3, timestamp=timenow
    )
    embed.add_field(name="**Latitude**", value=lat)
    embed.add_field(name="**Longitude**", value=lon)

    if "error" in geocode_response_json:
        print("Unable to reverse geocode")

    elif "properties" in geocode_response_json:
        display_name = geocode_response_json["properties"][0]["display_name"]
        embed.add_field(name="**Location**", value=display_name)
        """ city = geocode_response_json['city']
    embed.add_field(name='**Country**', value=country)
    embed.add_field(name='**City**', value=city) """

    google_maps = f"https://www.google.com/maps/@{lat},{lon},5z"

    embed.add_field(name="Google Maps", value=google_maps, inline=False)

    embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


@client.command(name="help", aliases=["commands"])
async def help(ctx):
    """gets information about the available commands."""

    embed = discord.Embed(
        title="📃 **Command List**",
        colour=0x2C3BA3,
        description="""A list of all available commands and their arguments, the prefix is ($)

  `$apod`
  view the astronomy picture of the day.

  `$apod [yyyy-mm-dd]`
  view the astronomy picture of the specified day.

  `$launches`
  get information about upcoming launches.

  `$nextlaunch` or `$nl`
  fetch information about the next rocket launch.

  `$nextlaunch [offset]` or `$nl [offset]`
  fetch information about the specified rocket launch.

  `$astronauts`
  get the current people in space.

  `$iss`
  get the current location of the international space station.

  `$moon`
  get information about the moon.
  """,
        timestamp=timenow,
    )

    embed_footer(ctx, embed)

    await ctx.channel.send(embed=embed)


if TOKEN is not None:
    client.run(TOKEN)
else:
    print("Please provide a token in '.env'")
