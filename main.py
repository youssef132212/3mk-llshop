import discord
from discord.ext import commands
from collections import defaultdict

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Data storage
shops = defaultdict(lambda: {
    "name": None,
    "owner": None,
    "partners": set(),
    "mentions": 0,
    "warnings": 0,
    "type": None,
    "status": "inactive",
})

def check_shop_exists(shop_name):
    return shop_name in shops

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def shop(ctx, name: str):
    if check_shop_exists(name):
        await ctx.send(f"Shop `{name}` already exists.")
    else:
        shops[name]["name"] = name
        shops[name]["owner"] = ctx.author.name
        shops[name]["status"] = "active"
        await ctx.send(f"Shop `{name}` created successfully.")

@bot.command()
async def shop_info(ctx, name: str):
    if check_shop_exists(name):
        shop = shops[name]
        info = (f"**Shop Info:**\n"
                f"Name: {shop['name']}\n"
                f"Owner: {shop['owner']}\n"
                f"Partners: {', '.join(shop['partners']) if shop['partners'] else 'None'}\n"
                f"Mentions: {shop['mentions']}\n"
                f"Warnings: {shop['warnings']}\n"
                f"Type: {shop['type'] if shop['type'] else 'Not Set'}\n"
                f"Status: {shop['status']}")
        await ctx.send(info)
    else:
        await ctx.send(f"Shop `{name}` does not exist.")

@bot.command()
async def delete(ctx, name: str):
    if check_shop_exists(name):
        del shops[name]
        await ctx.send(f"Shop `{name}` has been deleted.")
    else:
        await ctx.send(f"Shop `{name}` does not exist.")

@bot.command()
async def add_partner(ctx, shop_name: str, partner_name: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["partners"].add(partner_name)
        await ctx.send(f"Partner `{partner_name}` added to shop `{shop_name}`.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def remove_partner(ctx, shop_name: str, partner_name: str):
    if check_shop_exists(shop_name):
        if partner_name in shops[shop_name]["partners"]:
            shops[shop_name]["partners"].remove(partner_name)
            await ctx.send(f"Partner `{partner_name}` removed from shop `{shop_name}`.")
        else:
            await ctx.send(f"Partner `{partner_name}` is not part of shop `{shop_name}`.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def r_mentions(ctx, shop_name: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["mentions"] = 0
        await ctx.send(f"Mentions for shop `{shop_name}` have been reset.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def add_mentions(ctx, shop_name: str, count: int):
    if check_shop_exists(shop_name):
        shops[shop_name]["mentions"] += count
        await ctx.send(f"Added {count} mentions to shop `{shop_name}`. Total mentions: {shops[shop_name]['mentions']}.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def warn_shop(ctx, shop_name: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["warnings"] += 1
        await ctx.send(f"Shop `{shop_name}` has been warned. Total warnings: {shops[shop_name]['warnings']}.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def unwarn_shop(ctx, shop_name: str):
    if check_shop_exists(shop_name):
        if shops[shop_name]["warnings"] > 0:
            shops[shop_name]["warnings"] -= 1
            await ctx.send(f"Warning removed from shop `{shop_name}`. Remaining warnings: {shops[shop_name]['warnings']}.")
        else:
            await ctx.send(f"Shop `{shop_name}` has no warnings to remove.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def change_name(ctx, shop_name: str, new_name: str):
    if check_shop_exists(shop_name):
        shops[new_name] = shops.pop(shop_name)
        shops[new_name]["name"] = new_name
        await ctx.send(f"Shop name changed from `{shop_name}` to `{new_name}`.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def owner(ctx, shop_name: str, new_owner: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["owner"] = new_owner
        await ctx.send(f"Ownership of shop `{shop_name}` has been transferred to `{new_owner}`.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def change_type(ctx, shop_name: str, shop_type: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["type"] = shop_type
        await ctx.send(f"Shop `{shop_name}` type changed to `{shop_type}`.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def active(ctx, shop_name: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["status"] = "active"
        await ctx.send(f"Shop `{shop_name}` is now active.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

@bot.command()
async def disable(ctx, shop_name: str):
    if check_shop_exists(shop_name):
        shops[shop_name]["status"] = "inactive"
        await ctx.send(f"Shop `{shop_name}` is now inactive.")
    else:
        await ctx.send(f"Shop `{shop_name}` does not exist.")

# Add remaining commands following a similar structure...

import os

# Replace 'YOUR_TOKEN_HERE' with this line:
bot.run(os.getenv('MTMyMjAwNTQ4ODM2MzExMDQ0MA.G8Qy-n.dlzFDVBU44f0Vljb8QOWWoBJKcngT4OqdNB0DM'))
