from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client,message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>ᴇɴᴛᴇʀ ɪɴ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ</b>\n"
                "**/connect 𝙶𝚁𝙾𝚄𝙿 𝙸𝙳\n**"
                "**Get your Group id by adding this bot to your group and use  <code>/id</code>**",
                quote=True
            )
            return

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            await message.reply_text("You should be an admin in Given group!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, Make sure I'm present in your group!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ **{title}**\nɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰᴏʀᴍ ʜᴇʀᴇ../",
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode="md"
                    )
            else:
                await message.reply_text(
                    "ʏᴏᴜ'ʀᴇ ᴀʟʀᴇᴀᴅʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴛʜɪꜱ ᴄʜᴀᴛ!",
                    quote=True
                )
        else:
            await message.reply_text("ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ɢʀᴏᴜᴘ", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('ꜱᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ! ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client,message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        await message.reply_text("Run /connections to view or disconnect from groups!", quote=True)

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("Successfully disconnected from this chat", quote=True)
        else:
            await message.reply_text("This chat isn't connected to me!\nDo /connect to connect.", quote=True)



@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client,message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "There are no active connections!! Connect to some groups first.",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " ᴀᴄᴛɪᴠᴇ ɪꜰ ᴀᴄᴛɪᴠᴇ ᴇʟꜱᴇ ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "ᴄᴏɴɴᴇᴄᴛ ɢʀᴏᴜᴘꜱ :-\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ!! ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ꜱᴏᴍᴇ ɢʀᴏᴜᴘꜱ ꜰɪʀꜱᴛ.",
            quote=True
        )
