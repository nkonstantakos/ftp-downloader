import discord
import sys
import getopt
import configparser

from discord.ext import tasks

from DataSync.DataSyncHandler import DataSyncHandler
from DataSync.Model.SyncFile import SyncFile

config = configparser.ConfigParser()
bot = discord.Client()
dry_run = False
bot_enabled = False
sync_handler: DataSyncHandler = None

bot_commands = [
    discord.ApplicationCommand(
        name="sync",
        description="Manually triggers a file sync."
    ),
]


async def run(argv):
    global dry_run, config, sync_handler, bot_enabled
    properties_location = 'properties.ini'
    try:
        opts, args = getopt.getopt(argv, "b:p:d:c:n", ["bot=", "properties=", "dry-run=", "chunks=", "num-files="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-b", "--bot"):
            bot_enabled = arg == 'True'
        elif opt in ("-p", "--properties"):
            properties_location = arg
        elif opt in ("-c", "--chunks"):
            chunks = arg
        elif opt in ("-n", "--num-files"):
            num_files = arg
        elif opt in ("-d", "--dry-run"):
            dry_run = arg == 'True'

    config.read(properties_location)
    sync_handler = DataSyncHandler(config, dry_run)
    if bot_enabled:
        await bot.login(config['DISCORD']['botKey'])
        await bot.register_application_commands(bot_commands)
        await bot.connect()


@tasks.loop(seconds=60.0)
async def sync_task():
    global sync_handler
    await sync_handler.sync_data(print_pending)


async def print_pending(new_files: list[SyncFile]):
    message_content = "```New files detected: "
    for file in new_files:
        message_content = message_content + "\n" + file.file_name
    message_content = message_content + "```"
    message = await bot.get_channel(int(config['DISCORD']['channelId'])).send(message_content)



@bot.event
async def on_ready():
    sync_task.start()
    message = await bot.get_channel(int(config['DISCORD']['channelId'])).send(
        '```Starting...```')


@bot.event
async def on_slash_command(interaction: discord.Interaction):
    command_name = interaction.data['name']
    if command_name == "sync":
        await interaction.response.send_message("Triggering a file sync...")
        await sync_handler.sync_data(print_pending)


if __name__ == "__main__":
    loop = bot.loop
    loop.run_until_complete(run(sys.argv[1:]))
