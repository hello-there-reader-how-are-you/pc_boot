import requests
import random
from random import choice
import time
from discord.ext import commands
from discord import Intents
import RPi.GPIO as GPIO

from my_secrets import *

PC_RELAY_PIN = 14
REBOOT_RELAY_PIN = 15

current_state = 0
delay = 3.4
reset_delay = 4.5

GPIO.setmode(GPIO.BCM)
GPIO.setup(PC_RELAY_PIN, GPIO.OUT)
GPIO.setup(REBOOT_RELAY_PIN, GPIO.OUT)


GPIO.output(PC_RELAY_PIN, GPIO.HIGH)
GPIO.output(REBOOT_RELAY_PIN, GPIO.HIGH)

def toggle(pin, delay):
    global current_state
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pin, GPIO.HIGH)
    current_state = not current_state

# Create the Discord bot
intents = Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Notify the user when the bot has started up
@bot.event
async def on_ready():
    print("pc_bot back in action")
    channel = bot.get_channel(DEFAULT_CHANNEL)
    await channel.send("PC to boot!")

@bot.command()
async def list(ctx):
    await ctx.send('notes: prefix is !, "list" command lists possible commands')
    await ctx.send('cmd list: list = (lists cmds), pc_state, pc_on, pc_off, pc_set_state, pc_restart, pc_toggle, pc_50/50= (50%% chance of turing off pc)')


@bot.command(name='pc_on')
async def on(ctx):
    if not current_state:
        # Turn on the PC relay
        await ctx.send('pc is now on')
        toggle(PC_RELAY_PIN, delay)
    else:
        await ctx.send('pc is already on')

@bot.command(name='pc_off')
async def off(ctx):
    if current_state:
        # Turn on the PC relay
        await ctx.send('pc is now off')
        toggle(PC_RELAY_PIN, delay)
    else:
        await ctx.send('pc is already off')

@bot.command(name='pc_set_state')
async def pc_set_state(ctx, new_state: str):
    global current_state
    # Redefine the state of the PC relay based on user input
    if new_state.lower() == 'on':
        current_state = 1
        await ctx.send('PC state redefined to ON!')
    elif new_state.lower() == 'off':
        current_state = 0
        await ctx.send('PC state redefined to OFF!')
    else:
        await ctx.send('Invalid state. Please use "on" or "off".')



@bot.command(name='pc_restart')
async def restart(ctx):
    await ctx.send('Rebooting begin')
    toggle(REBOOT_RELAY_PIN, reset_delay)
    await ctx.send('Rebooting end')

@bot.command(name='pc_reboot')
async def restart(ctx):
    await ctx.send('Rebooting begin')
    toggle(REBOOT_RELAY_PIN, reset_delay)
    await ctx.send('Rebooting end')


@bot.command(name='pc_state')
async def pc_state(ctx):
    # Get the current state of the PC relay
    await ctx.send(f'PC is {"ON" if current_state else "OFF"}.')



@bot.command(name='pc_50/50')
async def fif_fif(ctx):
    # Check if the PC is already off, if yes, do nothing
    if not current_state:
        await ctx.send('PC is already OFF. Skipping 50/50.')
    # 50% chance of turning the PC off
    elif choice([True, False]):
        await off(ctx)
        await ctx.send('Losing Power...')
    else:
        await ctx.send('PC survives the 50/50!')


@bot.command(name='pc_toggle')
async def on(ctx):
    toggle(PC_RELAY_PIN, delay)
    await ctx.send('PC has been toggled')

# Start the bot
bot.run(str(TOKEN))