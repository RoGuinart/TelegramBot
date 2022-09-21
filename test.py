# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from multiprocessing import context
import random
from telegram import (ParseMode)
from telegram.ext import (Updater, CommandHandler)

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

elements = {
	"fire": "fire",
	"water": "water",
	"earth": "earth",
	"air": "air",
	"earth+fire": "lava",
	"fire+water": "steam",
	"air+fire": "smoke",
	"air+water":"cloud",
	"cloud+water": "rain",
	"earth+rain": "plant"
}

def checkCombination(update, context):
	if len(context.args) != 2:
		update.message.reply_text("Entra dos elements:\n/combination <element> <element>")
	e1 = context.args[0].lower()
	e2 = context.args[1].lower()

	if ord(e1[0]) > ord(e2[0]):
		aux = e1
		e1 = e2
		e2 = aux
	
	newElement = combination(e1, e2)
	if newElement == 0:
		update.message.reply_text("Combinació incorrecte")
	else:
		update.message.reply_text(f"New element found:\n{e1} + {e2} = {newElement}")


def combination(e1, e2):
	comb = f"{e1}+{e2}"
	if comb in elements:
		return elements[comb]
	else:
		return 0

def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "Roger Bot = Activado", parse_mode=ParseMode.HTML)

	# Podemos llamar a otros comandos, sin que se haya activado en el chat (/help).
	coin(update, context)


def coin(update, context):
	''' ⚪️/⚫️ Moneda 
	Genera un número elatorio entre 1 y 2.
	'''
	cid=update.message.chat_id
	msg="⚫️ Cara" if random.randint(1,2)==1 else "⚪️ Culo"
	# Responde directametne en el canal donde se le ha hablado.
	update.message.reply_text(msg)


def clutch(update, context):
	'''
	ALL HAIL THE ALMIGHTY CLUTCH
	'''
	songs = ["6o1pPE6l0Vo", "E9DaAONU024", "Yzz8J9CZn00", "6snEKE4abHk", "SRUm1iA_k08", "zPjkQKfmVI8", "qijzVzBc9WA", "MxwI6n8_nyI", "hAh2fUo9W3M", "F1DJFNSideQ"
	"yuphcpY5a5A", "X8cmbmwFAl8", "1XnmDLnffu4", "3Qm-WhZTIx4", "Qr8__1K6x6s", "G_cm96e-yIo", "HZVVHcN1TbI"]

	i = random.randint(0,len(songs)-1)
	song = "https://www.youtube.com/watch?v=" + songs[i]
	update.message.reply_text(song)

def bondia(update, context):
	msg = f"Bon dia {update.message.chat.username}!"
	update.message.reply_text(msg)

def help(update, context):
	m1 = "/combination <element>  <element> | Combines two elements and checks if you've gotten a new one. Replies with your result."
	m2 = "/clutch | Sends a random Clutch song from our Weathermaker archive"
	m3 = "/dia | Buenos días in the morning"
	m4 = "/coin | Toss a coin, get Cara or Culo"
	update.message.reply_text(f"{m1}\n{m2}\n{m3}\n{m4}")

def main():
	TOKEN="5672783109:AAHPI7aGzq1cYIbFHZzA9x2FeaLkyl0Yl3s"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('coin',	coin))
	dp.add_handler(CommandHandler('clutch',	clutch))
	dp.add_handler(CommandHandler('dia',	bondia))
	dp.add_handler(CommandHandler('combination',	checkCombination))
	dp.add_handler(CommandHandler('help',	help))

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('GuinartBot Starting...'))
	main()