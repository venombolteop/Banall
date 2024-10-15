import logging
import re

import os
import sys
import asyncio
from telethon import TelegramClient, events
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from var import Var
from telethon import Button

from time import sleep
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)



RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

logging.basicConfig(level=logging.INFO)

print("Starting.....")

Ayu = TelegramClient('Ayu', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

SUDO_USERS = []
for x in Var.SUDO:
    SUDO_USERS.append(x)



@Ayu.on(events.NewMessage(pattern="^/help"))
async def help(event):
    # URL to the image you want to send with the help message
    image_url = "https://te.legra.ph/file/310a7fad596b00513692a.jpg"
    
    # Help message text with the available commands
    help_text = """
ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:
    
- `/ping` : ᴄʜᴇᴄᴋ's ʙᴏᴛ's ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ.
- `/banall` : ʙᴀɴ ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
- `/unbanall` : ᴜɴʙᴀɴ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
- `/kickall` : ᴋɪᴄᴋ ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
- `/leave` : ᴍᴀᴋᴇ ᴛʜᴇ ʙᴏᴛ ʟᴇᴀᴠᴇ ᴛʜᴇ ɢʀᴏᴜᴘ [ᴏɴʟʏ sᴜᴅᴏ].
- `/restart` : ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ [ᴏɴʟʏ sᴜᴅᴏ].
"""
    
    # Send the image with the help text as the caption
    await event.reply(file=image_url, message=help_text)




@Ayu.on(events.NewMessage(pattern="^/ping"))
async def ping(e):
    start = datetime.now()
    text = "Pong!"
    event = await e.reply(text, parse_mode=None, link_preview=None)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"ɪ'ᴍ ᴏɴ \n\n ᴘᴏɴɢ !! `{ms}` ms")




@Ayu.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    # Send a picture and start message
    await event.respond(
        "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴀɴ ᴀʟʟ ʙᴏᴛ!\n"
        "ᴛʜɪs ʙᴏᴛ ɪs ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ʙᴀɴ ᴀɴᴅ ᴜɴʙᴀɴ ᴜsᴇʀs ɪɴ ɢʀᴏᴜᴘs.\n\n"
        "ʜɪᴛ `/help` ᴛᴏ ɢᴇᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.",
        buttons=[
            [Button.url("ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url="https://t.me/venomOwners")],
            [Button.url("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/venom_chatz")],
        ],
        file='https://te.legra.ph/file/310a7fad596b00513692a.jpg',  # Replace with your image URL
    )



                        



@Ayu.on(events.NewMessage(pattern="^/kickall"))
async def kickall(event):
    if not event.is_group:
        Reply = f"ɴᴏᴏʙ !! ᴜsᴇ ᴛʜɪs ᴄᴍᴅ ɪɴ ɢʀᴏᴜᴘ."
        await event.reply(Reply)
    else:
        await event.delete()
        Ven = await event.get_chat()

        # Check if the user has admin rights and kick permissions
        participant = await event.client.get_participant(event.chat_id, event.sender_id)
        if not participant.admin_rights or not participant.admin_rights.ban_users:
            return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ʙᴀɴ ʀɪɢʜᴛs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

        Venomop = await event.client.get_me()
        admin = Ven.admin_rights
        creator = Ven.creator

        if not admin and not creator:
            return await event.reply("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴇɴᴛ ʀɪɢʜᴛs !!")
        
        Ayush = await Ayu.send_message(event.chat_id, "ʜᴇʟʟᴏ !! ɪ'ᴍ ᴀʟɪᴠᴇ")
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        all = 0
        kimk = 0

        async for user in event.client.iter_participants(event.chat_id):
            all += 1
            try:
                if user.id not in admins_id:
                    await event.client.kick_participant(event.chat_id, user.id)
                    kimk += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
        
        await Ayush.edit(f"**ᴜsᴇʀs ᴋɪᴄᴋᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ! \n\n ᴋɪᴄᴋᴇᴅ:** `{kimk}` \n **ᴛᴏᴛᴀʟ:** `{all}`")






@Ayu.on(events.NewMessage(pattern="^/banall"))
async def banall(event):
    if not event.is_group:
        Reply = f"ɴᴏᴏʙ !! ᴜsᴇ ᴛʜɪs ᴄᴍᴅ ɪɴ ɢʀᴏᴜᴘ."
        await event.reply(Reply)
    else:
        await event.delete()
        Ven = await event.get_chat()

        # Get the sender's status in the group
        participant = await event.client.get_participant(event.chat_id, event.sender_id)
        
        if not participant.admin_rights or not participant.admin_rights.ban_users:
            return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ʙᴀɴ ʀɪɢʜᴛs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        
        Venomop = await event.client.get_me()
        admin = Ven.admin_rights
        creator = Ven.creator
        
        if not admin and not creator:
            return await event.reply("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴇɴᴛ ʀɪɢʜᴛs !!")
        
        Ayush = await Ayu.send_message(event.chat_id, "ʜᴇʟʟᴏ !! ɪ'ᴍ ᴀʟɪᴠᴇ")
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        all = 0
        bann = 0
        
        async for user in event.client.iter_participants(event.chat_id):
            all += 1
            try:
                if user.id not in admins_id:
                    await event.client(EditBannedRequest(event.chat_id, user.id, RIGHTS))
                    bann += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
        
        await Ayush.edit(f"**ᴜsᴇʀs ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ! \n\n ʙᴀɴɴᴇᴅ ᴜsᴇʀs:** `{bann}` \n **Total Users:** `{all}`")




@Ayu.on(events.NewMessage(pattern="^/unbanall"))
async def unban(event):
    if not event.is_group:
        Reply = f"ɴᴏᴏʙ !! ᴜsᴇ ᴛʜɪs ᴄᴍᴅ ɪɴ ɢʀᴏᴜᴘ."
        await event.reply(Reply)
    else:
        # Check if the user has admin rights and ban/unban permissions
        participant = await event.client.get_participant(event.chat_id, event.sender_id)
        if not participant.admin_rights or not participant.admin_rights.ban_users:
            return await event.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ʙᴀɴ ʀɪɢʜᴛs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

        msg = await event.reply("sᴇᴀʀᴄʜɪɴɢ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ʟɪsᴛs.")
        p = 0
        async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            except FloodWaitError as ex:
                print(f"sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
                sleep(ex.seconds)
            except Exception as ex:
                await msg.edit(str(ex))
            else:
                p += 1
        await msg.edit("{}: {} ᴜɴʙᴀɴɴᴇᴅ".format(event.chat_id, p))







@Ayu.on(events.NewMessage(pattern="^/leave"))
async def _(e):
    if e.sender_id in SUDO_USERS:
        venom = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 7:
            bc = venom[0]
            bc = int(bc)
            text = "ʟᴇᴀᴠɪɴɢ....."
            event = await e.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ")
            except Exception as e:
                await event.edit(str(e))
        else:
            bc = e.chat_id
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ")
            except Exception as e:
                await event.edit(str(e))


@Ayu.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__ʀᴇsᴛᴀʀᴛɪɴɢ__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None)
        try:
            await Ayu.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()

print("\n\n")
print("Your Ban All Bot Deployed Successfully ✅")

Ayu.run_until_disconnected()
