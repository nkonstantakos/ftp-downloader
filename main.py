import discord
import sys
import getopt
import configparser

from DataSync.DataSyncHandler import DataSyncHandler

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


@bot.event
async def on_ready():
    message = await bot.get_channel(int(config['DISCORD']['channelId'])).send(
        '```Starting...```')


@bot.event
async def on_slash_command(interaction: discord.Interaction):
    command_name = interaction.data['name']
    if command_name == "sync":
        await interaction.response.send_message("Triggering a file sync...")
        sync_handler.sync_data()


if __name__ == "__main__":
    loop = bot.loop
    loop.run_until_complete(run(sys.argv[1:]))
