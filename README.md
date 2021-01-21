# Discord-voice-channel-creator

A discord bot that will create a temporary voice channel

## Feature

1. Create a temporary channel
2. "@"role/"@"people to only allow them to speak in that voice channel

## Command

### Voice Channel

vc create ["@"role/"@"people/text]

### info

vc change_log [version_number]

vc help

---

## Hosting

As this bot is open source, you can host and edit this bot by yourself. I added some owner command to let you easier to edit and launch the bot.

### Environment variable

OWNER={owner id} (to use owner command)

TOKEN={your bot token} (to launch the bot)

### Owner command

#### Extension

vc load {extension}

vc unload {extension}

vc reload {extension}

#### Other

vc stats
vc resetDB
