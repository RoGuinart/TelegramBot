# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from multiprocessing import context
from multiprocessing.sharedctypes import Value
from optparse import Values
import random
from telegram import (ParseMode)
from telegram.ext import (Updater, CommandHandler)
from PIL import Image






# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
combination=""
started = False
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

elements = {
	"fire": "fire",
	"water": "water",
	"earth": "earth",
	"air": "air",
	"earth+fire": "lava",
    "fire+water": "steam",
	"heat+water": "steam",
	"air+fire": "smoke",
	"air+water":"cloud",
    "earth+water":"mud",
    "mud+fire":"brick",
	"cloud+water": "rain",
	"earth+rain": "plant",
    "earth+earth":"land",
    "brick+brick":"wall",
    "wall+wall":"house",
    "house+house":"village",
    "village+village":"city",
    "city+city":"country",
    "country+country":"continent",
    "river+water":"lake",
    "river+river":"sea",
    "sea+sea":"ocean",
    "river+wall":"dam",
    "continent+ocean":"planet",
    "planet+fire":"sun",
    "sun+water":"rainbow",
    "water+rain":"river",
    "planet+ocean":"primordialsoup",
    "planet+sea":"primordialsoup",
    "primordialsoup+life":"bacteria",
    "primordialsoup+energy":"life",
    "fire+fire":"energy",
    "energy+earth":"earthquake",
    "bacteria+water":"plankton",
    "air+air":"pressure",
    "pressure+pressure":"wind",
    "wind+wind":"tornado",
    "energy+air":"heat",
    "barn+house":"farm",
    "sea+tornado":"hurricane",
    "sea+air":"waves",
    "lava+water":"obsidian",
    "pressure+earth":"rock",
    "fire+rock":"metal",
    "metal+earth":"plow",
    "plow+land":"field",
    "field+house":"barn",
    "city+smoke":"smog",
    "heat+air":"warmth",
    "energy+sun":"solarcell",
    "earth+plow":"field",
    "plane+planet":"solarsystem",
    "solarsystem+solarsystem":"galaxy",
    "galaxy+galaxy":"galaxycluster",
    "galaxycluster+galaxycluster":"universe",
    "pressure+heat":"plasma",
    "land+life":"animal",
    "land+life":"soil",
    "soil+plow":"field",
    "animal+water":"fish",
    "farm+animal":"livestock",
    "livestock+farm":"cow",
    "livestock+farm":"horse",
    "cow+fish":"manatee",
    "animal+air":"bird",
    "bird+bird":"egg",
    "egg+farm":"chicken",
    "chicken+egg":"philosphy",
    "philosphy+philosphy":"idea",
    "fish+egg":"roe",
    
}


def checkCombination(update, context):
    global started
    if started == True:
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

            context.bot.send_photo(update.message.chat_id, photo=open('Elementos/{}.jpg'.format(newElement),'rb'))
    else:
        update.message.reply_text("FMA Bot no está activado")


def combination(e1, e2):
    comb = f"{e1}+{e2}"
    if comb in elements:
        return elements[comb]
    else:
        return 0


def start(update, context):
    global started
    ''' START '''
	# Enviar un mensaje a un ID determinado.
    context.bot.send_message(update.message.chat_id, "FMA Bot = Activado", parse_mode=ParseMode.HTML)
    started = True

	# Podemos llamar a otros comandos, sin que se haya activado en el chat (/help).





def checkElement(element):
    for value  in elements.values():
        if value == element:
            return 0
        
def element(update, context):
    if started == True:
        if len(context.args) != 1:
            update.message.reply_text("Entra un element:\n/element <element>")
            return
        if checkElement(context.args[0]) == 0:
            if context.args[0]=='fire':
                update.message.reply_text("Fire is one of the four classical elements along with Earth, Water and Air in ancient Greek philosophy and science.\nFire is considered to be both hot and dry and, according to Plato, is associated with the tetrahedron.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/fire.jpg','rb'))
            elif context.args[0]=='water':
                update.message.reply_text("Water is one of the classical elements in ancient Greek philosophy along with Air, Earth and Fire, in the Asian Indian system Panchamahabhuta, and in the Chinese cosmological and physiological system Wu Xing.\nIn contemporary esoteric traditions, it is commonly associated with the qualities of emotion and intuition.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/water.jpg','rb'))
            elif context.args[0]=='earth':
                update.message.reply_text("Earth is one of the classical elements in ancient Greek philosophy along with Air, Earth and Fire.\nIt was commonly associated with qualities of heaviness, matter and the terrestrial world. Due to the hero cults, and chthonic underworld deities, the element of earth is also associated with the sensual aspects of both life and death in later occultism.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/earth.jpg','rb'))
            elif context.args[0]=='air':
                update.message.reply_text("Air is one of the four classical elements along with Water, Earth and Fire in ancient Greek philosophy and in Western alchemy.\nAccording to Plato, it is associated with the octahedron; air is considered to be both hot and wet. ")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/air.jpg','rb'))
            elif context.args[0]=='lava':
                update.message.reply_text("Lava is molten or partially molten rock that has been expelled from the interior of a terrestrial planet or a moon onto its surface.\nLava may be erupted at a volcano or through a fracture in the crust, on land or underwater, usually at temperatures from 800 to 1,200 °C")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/lava.jpg','rb'))
            elif context.args[0]=='steam':
                update.message.reply_text("Steam is water in the gas phase.\nThis may occur due to evaporation or due to boiling, where heat is applied until water reaches the enthalpy of vaporization.\nSteam that is saturated or superheated is invisible.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/steam.jpg','rb'))
            elif context.args[0]=='smoke':
                update.message.reply_text("Smoke is a collection of airborne particulates and/or gases emitted when a material undergoes combustion, together with the quantity of air that is entrained or otherwise mixed into the mass.\nIt is commonly an unwanted by-product of fires")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/smoke.jpg','rb'))
            elif context.args[0]=='cloud':
                update.message.reply_text("Cloud is an aerosol consisting of liquid droplets, frozen crystals, or other particles suspended in the atmosphere of a planetary body or similar space.\nWater or various other chemicals may compose the droplets and crystals.\nOn Earth, clouds are formed as a result of saturation of the air when it is cooled to its dew point, or when it gains sufficient moisture from an adjacent source to raise the dew point to the ambient temperature.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/cloud.jpg','rb'))
            elif context.args[0]=='rain':
                update.message.reply_text("Rain is water droplets that have condensed from atmospheric water vapor and then fall under gravity. Rain is a major component of the water cycle and is responsible for depositing most of the fresh water on the Earth.\nIt provides water for hydroelectric power plants, crop irrigation, and suitable conditions for many types of ecosystems.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/rain.jpg','rb'))
            elif context.args[0]=='plant':
                update.message.reply_text("Plant is an element combination of earth and water element.\nThe water combined with the soil of earth makes the plant grow strong and develop strong roots. When it fully grows it starts doing the photosynthesis and as a consequence the air element renovates itself, making it almost infinite.")
                context.bot.send_photo(update.message.chat_id, photo=open('Elementos/plant.jpg','rb'))
            
            
        else:
            update.message.reply_text("The element selected does not exist")
    else:
        update.message.reply_text("FMA Bot no está activado")
                
    
    
def help(update, context):
    global started
    if started == True:
        m1 = "/combination <element>  <element> | Combines two elements and checks if you've gotten a new one. Replies with your result."
        m2 = "/element <element> | Brew explication of the element with an image that represents it."

        update.message.reply_text(f"{m1}\n{m2}")
    else:
        update.message.reply_text("FMA Bot no está activado")

def main():
    #TOKEN="5672783109:AAHPI7aGzq1cYIbFHZzA9x2FeaLkyl0Yl3s"
    TOKEN="5491139231:AAFnIXg9PioSi3d8j-csypLiH-X-RgsvTXQ"
    updater=Updater(TOKEN, use_context=True)
    
    dp=updater.dispatcher
    # Eventos que activarán nuestro bot.
	# /comandos
    dp.add_handler(CommandHandler('start',	start))
    dp.add_handler(CommandHandler('element',	element))
    dp.add_handler(CommandHandler('combination',	checkCombination))
    dp.add_handler(CommandHandler('help',	help))
    dp.add_error_handler(error_callback)
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()

if __name__ == '__main__':
	print(('Starting...'))
	main()