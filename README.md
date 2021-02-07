# Discord-voice-channel-creator

[![Discord Bots](https://top.gg/api/widget/status/791601658651213824.svg)](https://top.gg/bot/791601658651213824)

A discord bot that will create a temporary voice channel

## Commands

commands| description
---|---
`vc create [?speakers] [?name]` | create a voice channel that everyone can hear
`vc private [speaker/listener] [?name]`| create a private voice and text channel, no other user can enter your channel except admin
`vc text [?speaker] [?name]`| create a common voice channel with a text channel
`vc change_log [?version]` | get recent change log
`vc permission` | get required permission
`vc help` | get command description

## Arguments

arg | Options
---|---
`?` | optional argument
`speaker` | - @user<br>- @role <br> Default speaker: @everyone
`name` | -channel name <br> Default: created by voice channel creator
`version` | -version number

## Example

command | result
---|---
vc create @gta casio heist | Channel name: gta casio heist <br> Speaker: you and user who have @gta role <br> Listener: everyone
vc create @Jason11ookJJ | Channel  name: Jason11ookJJ <br> Speaker: you and Jason11ookJJ <br> Listener: everyone
vc private @Jason11ookJJ |  Channel name: Jason11ookJJ <br> Speaker: you and Jason11ookJJ <br> Listener: you and Jason11ookJJ

---

## Hosting

As this bot is open source, you can host and edit this bot by yourself. I added some owner command to let you easier to edit and launch the bot.

Environment variable | data
---|---
OWNER | owner id
TOKEN | your bot token

command | use
--- | ---
`vc load [extension]` | load extension
`vc unload [extension]` | unload extension
`vc reload [extension]` | reload extension
`vc stats` | get bot stats
`vc resetdb` | reset database
`vc error` | get bot error
`vc check_error [error_id]` | make error will not show up

## Debug
command | uses
---|---
`vc delete_all` | delete all channel in the category 
