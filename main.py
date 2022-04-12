# bot.py
import requests
import discord
import os

TOKEN = os.environ.get('DISCORD_TOKEN')
API_KEY = os.environ.get('API_KEY')


def get_translation(text, target):
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"to": "{}".format(target), "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
    payload = [{"Text": "{}".format(text)}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com",
        "X-RapidAPI-Key": "{}".format(API_KEY)
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    except requests.exceptions.RequestException as e:
        return e
    except (requests.exceptions.InvalidJSONError, TypeError):
        return "Invalid JSON"

    try:
        response.json()[0]["translations"][0]["text"]
    except (KeyError, IndexError, ValueError):
        return "PARSING ERROR"

    return response.json()[0]["translations"][0]["text"]


client = discord.Client()


@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    channel = discord.utils.get(client.get_all_channels(), name='translation-log')
    if reaction.emoji == '🇪':
        target = 'en'
    elif reaction.emoji == '🇨':
        target = 'zh-CN'
    # elif reaction.emoji == '🇯':
    #     target='ja'
    else:
        return
    text = reaction.message.content
    if len(str(text)) == 0 or "https:" in str(text) or "http:" in str(text):
        return
    embed = discord.Embed(title="Translation", description="Translation", color=0xffffff)
    embed.add_field(name="Original Text", value=text, inline=False)
    embed.add_field(name="Translated Test", value=get_translation(text, target=target), inline=False)
    await channel.send(embed=embed)


client.run(TOKEN)
