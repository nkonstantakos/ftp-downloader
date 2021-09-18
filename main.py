import asyncio
import io

import discord
import sys
import getopt
import configparser
import ftplib

from tqdm import tqdm


config = configparser.ConfigParser()
bot = discord.Client()
download_list = ['']
local_path = "DAVE - 1x07 - What Wood You Wear.mkv"
remote_path = "/media/66bc/nktorrents/private/testData/DAVE/Season 01/"
ftp = None
pbar = None
message = None
output = None
completed = False
dry_run = False
bot_enabled = False


def run(argv):
    properties_location = ''
    try:
        opts, args = getopt.getopt(argv, "b:p:d:c:n", ["bot=", "properties=", "dry-run=", "chunks=", "num-files="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-p", "--properties"):
            properties_location = arg
        elif opt in ("-c", "--chunks"):
            chunks = arg
        elif opt in ("-n", "--num-files"):
            num_files = arg
        elif opt in ("-d", "--dry-run"):
            dry_run = arg

    global config, ftp
    config.read(properties_location)
    ftp = ftplib.FTP(config['FTP']['url'])
    ftp.login(config['FTP']['username'], config['FTP']['password'])
    if bot_enabled:
        bot.run(config['DISCORD']['botKey'])


def file_write(data):
    file = open(local_path, 'ab')
    file.write(data)
    global pbar
    pbar.update(len(data))
    file.close()

@bot.event
async def on_ready():
    ftp.cwd(remote_path)
    files = ftp.nlst()
    for fname in files:
        print(fname)
    ftp.sendcmd("TYPE i")
    size = ftp.size(local_path)
    global pbar
    global output
    output = io.StringIO()
    pbar = tqdm(total=size, ascii=True, file=output, unit_divisor=1000)
    #pbar = tqdm(total=10, ascii=True, file=output, unit_divisor=1000, )
    global message
    message = await bot.get_channel(int(config['DISCORD']['channelId'])).send(
        '```{0} ```'.format(output.getvalue()))

    download()

    quit()


def download():
    ftp.retrbinary("RETR " + local_path, file_write)
    global completed
    completed = True


def print_single_status():
    global completed, output, message, pbar
    output.truncate(0)
    current = output.getvalue().replace('\r', '').lstrip()
    current = current.replace('\x00', '')
    print(current)


async def print_status():
    global completed
    global output
    global message
    global pbar
    output.truncate(0)
    pbar.update(1)
    for i in range(10):
        current = output.getvalue().replace('\r', '').lstrip()
        current = current.replace('\x00', '')
        await message.edit(content='```{0} ```'.format(current))
        print(output.getvalue())
        output.truncate(0)
        print(pbar.update(1))
        await asyncio.sleep(2)


if __name__ == "__main__":
    run(sys.argv[1:])
