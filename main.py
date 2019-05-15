import discord
import os
import traceback
import json
import argparse
from shutil import copyfile
from discord.ext import commands

def parse_cmd_arguments():  # travis handler, taken from https://github.com/appu1232/Discord-Selfbot/blob/master/appuselfbot.py
    parser = argparse.ArgumentParser(description="Catbot")
    parser.add_argument("-test", "--test-run",  # test run flag for Travis
                        action="store_true",
                        help="Makes the bot quit before trying to log in")
    return parser
args = parse_cmd_arguments().parse_args()
_test_run = args.test_run
if _test_run:
    try:
        os.path.isfile("config.py")
    except:
        print('config.py is missing')  # only visible in Travis
    print("Quitting: test run")
    exit(0)

# Create config if nonexistent
if not os.path.exists('config.py'):
    try:
        copyfile('config.py.sample', 'config.py')
    except Exception as e:
        print(e)
        print('config.py and config.py.sample are missing from root')

import config

bot = commands.Bot(command_prefix=config.prefix, description="cats")

@bot.event
async def on_ready():
    try:
        bot.guild = bot.get_guild(511229375719669766)
        bot.minecraft_role = discord.utils.get(bot.guild.roles, id=config.minecraft_role)
        bot.mod_dict = json.load(open("mods.json", "r"))
        bot.creator = discord.utils.get(bot.guild.members, id=177939404243992578)
        print("Initialized on {}".format(bot.guild.name))
    except Exception as e:
        pass # Only fails if not in guild, won't be possible after first launch
        print(e)

async def globally_block_dms(ctx):
    if ctx.guild is None:
        raise discord.ext.commands.NoPrivateMessage(' ')
        return False
    return True

# loads extensions
modules = [
    'modules.util',
    'modules.vote'
]

failed_modules = []

for extension in modules:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_modules.append([extension, type(e).__name__, e])
if not failed_modules:
    print('All addons loaded!')
        
@bot.event
async def on_command_error(ctx, e):
    if isinstance(e, commands.errors.CommandNotFound):
        pass # Don't need you
    elif isinstance(e, discord.ext.commands.NoPrivateMessage):
        await ctx.send("You cannot use this command in DMs!")
    elif isinstance(e, commands.errors.MissingRequiredArgument):
        formatted_help = await commands.formatter.HelpFormatter().format_help_for(ctx, ctx.command)
        await ctx.send(f"You're missing required arguments.\n{formatted_help[0]}")
    else:
        if ctx.command:
            await ctx.send("An error occurred while processing the `{}` command.".format(ctx.command.name))
        print(f"Ignoring exception in command {ctx.command} in {ctx.message.channel}")
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        log = "".join(tb)
        print(log)

@bot.event
async def on_error(event, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        return
    print(f"Ignoring exception in {event}")
    tb = traceback.format_exc()
    print("".join(tb))
        
@bot.command()
async def about(ctx):
    await ctx.send("This is a bot written by {}, and can be found at https://github.com/GriffinG1/catbot.".format(bot.creator))

@bot.command()
async def reload(ctx):
    """Reloads an addon."""
    if ctx.author == ctx.guild.owner or ctx.author.id == 177939404243992578:
        errors = ""
        for module in modules:
            try:
                bot.reload_extension(module)
            except Exception as e:
                errors += 'Failed to load module: `{}` due to `{}: {}`\n'.format(module, type(e).__name__, e)
        if not errors:
            await ctx.send(':white_check_mark: Extensions reloaded.')
        else:
            await ctx.send(errors)
    else:
        await ctx.send("You don't have permission to do that!")
            
try:
    bot.run(config.token)
except Exception as e:
    print('config.py is missing values.')
    input('Press the enter key to close.')