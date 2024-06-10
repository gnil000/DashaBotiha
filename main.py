# import asyncio
import configparser
import requests
from loguru import logger
from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot, Message
config = configparser.ConfigParser()
config.read("config.ini")

print(config["VK"]["token"])

bot = Bot(token = config["VK"]["token"])
photo_uploader = PhotoMessageUploader(bot.api)

@bot.on.message()
async def message_handler(message: Message):
    try:
        if len(message.attachments)!=0:
            if message.attachments[0].photo != None:
                p = requests.get(message.attachments[0].photo.sizes[-1].url)
                logger.debug(p.content)
                photo = await photo_uploader.upload(file_source=p.content, peer_id=message.peer_id,)
                await message.answer(attachment=photo)
        else:
            await message.answer(message.text)
    except Exception as ex:
        logger.error(ex)

bot.run_forever()