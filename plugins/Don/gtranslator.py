from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from plugins.admemes.list import list

@Client.on_message(filters.command(["tr"]))
async def left(client,message):
	if (message.reply_to_message):
		try:
			lgcd = message.text.split("/tr")
			lg_cd = lgcd[1].lower().replace(" ", "")
			tr_text = message.reply_to_message.text
			translator = Translator()
			translation = translator.translate(tr_text,dest = lg_cd)
			hehek = InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "ᴄʟᴏꜱᴇ", callback_data="close_data"
                                 ]]
                            )
			try:
				for i in list:
					if list[i]==translation.src:
						fromt = i
					if list[i] == translation.dest:
						to = i 
				await message.reply_text(f"translated from {fromt.capitalize()} to {to.capitalize()}\n\n```{ᴛʀᴀɴꜱʟᴀᴛɪᴏɴ ᴛᴇxᴛ}```", reply_markup=hehek, quote=True)
			except:
			   	await message.reply_text(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{ᴛʀᴀɴꜱʟᴀᴛɪᴏɴ ᴛᴇxᴛ}```", reply_markup=hehek, quote=True)
			

		except :
			print("error")
	else:
			 ms = await message.reply_text("ᴛʀᴀɴꜱʟᴀᴛɪᴏɴ ᴛᴇxᴛ
