import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from .bot import StreamBot
from .vars import Var
from aiohttp import web
from .server import web_server
from .utils.keepalive import ping_server
from Adarsh.bot.clients import initialize_clients

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

ppath = "Adarsh/bot/plugins/*.py"
files = glob.glob(ppath)
StreamBot.start()
loop = asyncio.get_event_loop()


async def start_services():
    print('\n')
    print('━━━━━━━━━━━━━━━━━━━ ɪɴɪᴛᴀʟɪᴢɪɴɢ ᴛʜᴇ ʙᴏᴛ ʙᴀʙʏ ━━━━━━━━━━━━━━━━━━━')
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("━━━━━━━━━━━━━━━━━━━ ᴅᴏɴᴇ ━━━━━━━━━━━━━━━━━━━")
    print()
    print("━━━━━━━━━━━━━━━━━━━ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴄʟɪᴇɴᴛs ʙᴀʙʏ ━━━━━━━━━━━━━━━━━━━")
    await initialize_clients()
    print("------------------------------ ᴅᴏɴᴇ ------------------------------")
    print('\n')
    print('--------------------------- ɪᴍᴘᴏʀᴛɪɴɢ ᴛʜᴇ ᴍᴏᴅᴜʟᴇs ---------------------------')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"Adarsh/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["Adarsh.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    if Var.ON_HEROKU:
        print("━━━━━━━━━━━━━━━━━━━ sᴛᴀʀᴛɪɴɢ ᴋᴇᴇᴘ ᴀʟɪᴠᴇ sᴇʀᴠɪᴄᴇ ━━━━━━━━━━━━━━━━━━━")
        print()
        asyncio.create_task(ping_server())
    print('━━━━━━━━━━━━━━━━━━━ ɪɴɪᴛᴀʟɪᴢɪɴɢ ᴡᴇʙ sᴇʀᴠᴇʀ ━━━━━━━━━━━━━━━━━━━')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    print('━━━━━━━━━━━━━━━━━━━ ᴅᴏɴᴇ ━━━━━━━━━━━━━━━━━━━')
    print('\n')
    print('----------------------- sᴇʀᴠɪᴄᴇ sᴛᴀʀᴛᴇᴅ -----------------------------------------------------------------')
    print('                        ʙᴏᴛ ɴᴀᴍᴇ ➻ {}'.format((await StreamBot.get_me()).first_name))
    print('                        sᴇʀᴠᴇʀ ɪᴘ ➻ {}:{}'.format(bind_address, Var.PORT))
    print('                        ᴏᴡɴᴇʀ ➻ {}'.format((Var.OWNER_USERNAME)))
    if Var.ON_HEROKU:
        print('                        ᴀᴘᴘ ʀᴜɴɴɴɢ ᴏɴ ➻ {}'.format(Var.FQDN))
    print('---------------------------------------------------------------------------------------------------------')
    print('ғᴏʟʟᴏᴡ ᴍᴇ ᴏɴ ɢɪᴛʜᴜʙ ❅ https://github.com/Bikash1225/filestreambot-pro')
    print('---------------------------------------------------------------------------------------------------------')
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('━━━━━━━━━━━━━━━━━━━ ᴍʜᴍᴍ ɢᴏᴏᴅ ʙʏᴇ ʙᴀʙʏ ━━━━━━━━━━━━━━━━━━━')
