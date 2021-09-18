import discord
import sys
import getopt
import configparser

from FTP.FTPHandler import FTPHandler

config = configparser.ConfigParser()
bot = discord.Client()
dry_run = False
bot_enabled = False

ftp_handler = None


def run(argv):
    global dry_run, config, ftp_handler, bot_enabled
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
    ftp_handler = FTPHandler(config, dry_run)
    ftp_handler.scan_for_updates()
    if bot_enabled:
        bot.run(config['DISCORD']['botKey'])
    ftp_handler.close()


@bot.event
async def on_ready():
    message = await bot.get_channel(int(config['DISCORD']['channelId'])).send(
        '```Starting...```')

    quit()


if __name__ == "__main__":
    run(sys.argv[1:])
