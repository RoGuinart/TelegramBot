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
    
#Diccionari
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
	"cloud+water": "rain",
	"earth+rain": "plant",
    "earth+earth":"land",
    "brick+brick":"wall",
    "wall+wall":"house",
    "earth+water":"mud",
    "mud+fire":"brick",
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
    "rock+life":"soil",
    "soil+plow":"field",
    "animal+water":"fish",
    "farm+animal":"livestock",
    "livestock+farm": "cow",
    "animal+livestock":"horse",
    "cow+fish":"manatee",
    "animal+air":"bird",
    "bird+bird":"egg",
    "egg+farm":"chicken",
    "chicken+egg":"philosophy",
    "philosophy+philosophy":"idea",
    "fish+egg":"roe",
    "fish+horse":"seahorse",
    "horse+bird":"pegasus",
    "fish+bird":"flyingfish",
    "horse+water":"hippo",
    "cow+water":"milk",
    "fire+cow":"steak",
    "steak+heat":"jerky",
    "fire+bird":"phoenix",
    "fire+egg":"omelette",
    "bird+water":"duck",
    "duck+metal":"airplane",
    "seahorse+philosofy":"small",
    "small+bird":"hummingbird",
    "bird+metal":"airplane",
    "ocean+fish":"shark",
    "sea+fish":"starfish"
}

#Comprovar la combinació
def checkCombination(update, context):
    global started
    if started == True:
        if len(context.args) != 2:
            update.message.reply_text("Enter two elements:\n/combination <element> <element>")
        e1 = context.args[0].lower()
        e2 = context.args[1].lower()

        if ord(e1[0]) > ord(e2[0]):
            aux = e1
            e1 = e2
            e2 = aux
        
        newElement = combination(e1, e2)
        if newElement == 0:
            update.message.reply_text("Wrong combination")
        else:
            update.message.reply_text(f"New element found:\n{e1} + {e2} = {newElement}")

            context.bot.send_photo(update.message.chat_id, photo=open('Elementos/{}.jpg'.format(newElement),'rb'))
    else:
        update.message.reply_text("FMA Bot not activated")

#Fer la combinacio
def combination(e1, e2):
    comb = f"{e1}+{e2}"
    if comb in elements:
        return elements[comb]
    else:
        return 0

#Començar el bot
def start(update, context):
    global started
    ''' START '''
	# Enviar un mensaje a un ID determinado.
    context.bot.send_message(update.message.chat_id, "FMA Bot = Activado", parse_mode=ParseMode.HTML)
    started = True

	# Podemos llamar a otros comandos, sin que se haya activado en el chat (/help).




#Comprovar si existeix l'element
def checkElement(element):
    for value  in elements.values():
        if value == element:
            return 0
#Foto del element i una breu descripcio       
def element(update, context):
    if started == True:
        if len(context.args) != 1:
            update.message.reply_text("Enter an element:\n/element <element>")
            return
        if checkElement(context.args[0]) == 0:
            if context.args[0]=='fire':
                update.message.reply_text("Fire is one of the four classical elements along with Earth, Water and Air in ancient Greek philosophy and science.\nFire is considered to be both hot and dry and, according to Plato, is associated with the tetrahedron.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='water':
                update.message.reply_text("Water is one of the classical elements in ancient Greek philosophy along with Air, Earth and Fire, in the Asian Indian system Panchamahabhuta, and in the Chinese cosmological and physiological system Wu Xing.\nIn contemporary esoteric traditions, it is commonly associated with the qualities of emotion and intuition.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='earth':
                update.message.reply_text("Earth is one of the classical elements in ancient Greek philosophy along with Air, Earth and Fire.\nIt was commonly associated with qualities of heaviness, matter and the terrestrial world. Due to the hero cults, and chthonic underworld deities, the element of earth is also associated with the sensual aspects of both life and death in later occultism.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='air':
                update.message.reply_text("Air is one of the four classical elements along with Water, Earth and Fire in ancient Greek philosophy and in Western alchemy.\nAccording to Plato, it is associated with the octahedron; air is considered to be both hot and wet. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='lava':
                update.message.reply_text("Lava is molten or partially molten rock that has been expelled from the interior of a terrestrial planet or a moon onto its surface.\nLava may be erupted at a volcano or through a fracture in the crust, on land or underwater, usually at temperatures from 800 to 1,200 °C")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='steam':
                update.message.reply_text("Steam is water in the gas phase.\nThis may occur due to evaporation or due to boiling, where heat is applied until water reaches the enthalpy of vaporization.\nSteam that is saturated or superheated is invisible.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='smoke':
                update.message.reply_text("Smoke is a collection of airborne particulates and/or gases emitted when a material undergoes combustion, together with the quantity of air that is entrained or otherwise mixed into the mass.\nIt is commonly an unwanted by-product of fires")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='cloud':
                update.message.reply_text("Cloud is an aerosol consisting of liquid droplets, frozen crystals, or other particles suspended in the atmosphere of a planetary body or similar space.\nWater or various other chemicals may compose the droplets and crystals.\nOn Earth, clouds are formed as a result of saturation of the air when it is cooled to its dew point, or when it gains sufficient moisture from an adjacent source to raise the dew point to the ambient temperature.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='rain':
                update.message.reply_text("Rain is water droplets that have condensed from atmospheric water vapor and then fall under gravity. Rain is a major component of the water cycle and is responsible for depositing most of the fresh water on the Earth.\nIt provides water for hydroelectric power plants, crop irrigation, and suitable conditions for many types of ecosystems.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='plant':
                update.message.reply_text("Plant is an element combination of earth and rain element.\nThe water combined with the soil of earth makes the plant grow strong and develop strong roots. When it fully grows it starts doing the photosynthesis and as a consequence the air element renovates itself, making it almost infinite. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))                
            
            
            elif context.args[0]=='land':
                update.message.reply_text("Land is an element combination of earth element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='wall':
                update.message.reply_text("Wall is an element combination of brick with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='house':
                update.message.reply_text("House is an element combination of wall element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='mud':
                update.message.reply_text("Mud is an element combination of earth and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='brick':
                update.message.reply_text("Brick is an element combination of mud and fire element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='village':
                update.message.reply_text("Village is an element combination of house element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='city':
                update.message.reply_text("City is an element combination of village element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='country':
                update.message.reply_text("Country is an element combination of city element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='continent':
                update.message.reply_text("Continent is an element combination of country element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='lake':
                update.message.reply_text("Lake is an element combination of river and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='heat':
                update.message.reply_text("Heat is an element combination of energy and air element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='sea':
                update.message.reply_text("Sea is an element combination of river element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='ocean':
                update.message.reply_text("Ocean is an element combination of earth and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='dam':
                update.message.reply_text("Dam is an element combination of river element with wall element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='planet':
                update.message.reply_text("Planet is an element combination of continent and ocean element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='sun':
                update.message.reply_text("Sun is an element combination of planet and fire element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='rainbow':
                update.message.reply_text("Rainbow is an element combination of sun and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='river':
                update.message.reply_text("River is an element combination of water and rain element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='primordialsoup':
                update.message.reply_text("Primordialsoup is an element combination of planet and ocean element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='bacteria':
                update.message.reply_text("Bacteria is an element combination of primordialsoup and life element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='life':
                update.message.reply_text("Life is an element combination of primordialsoup and energy element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='energy':
                update.message.reply_text("Energy is an element combination of fire element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='earthquake':
                update.message.reply_text("Earthquake is an element combination of earth and energy element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='plankton':
                update.message.reply_text("Plankton is an element combination of bacteria and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='pressure':
                update.message.reply_text("Pressure is an element combination of air element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='wind':
                update.message.reply_text("Wind is an element combination of pressure element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='tornado':
                update.message.reply_text("Tornado is an element combination of wind element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='farm':
                update.message.reply_text("Farm is an element combination of barn and house element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='hurricane':
                update.message.reply_text("Hurricane is an element combination of sea and tornado element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='waves':
                update.message.reply_text("Waves is an element combination of sea and air element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='obsidian':
                update.message.reply_text("Obsidian is an element combination of lava and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='rock':
                update.message.reply_text("Rock is an element combination of earth and pressure element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='metal':
                update.message.reply_text("Metal is an element combination of fire and rock element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='plow':
                update.message.reply_text("Plow is an element combination of metal and earth element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='field':
                update.message.reply_text("Field is an element combination of plow and land element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='barn':
                update.message.reply_text("Barn is an element combination of field and house element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='smog':
                update.message.reply_text("Smog is an element combination of city and smoke element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='warmth':
                update.message.reply_text("Warmth is an element combination of heat and air element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='solarcell':
                update.message.reply_text("Solar cell is an element combination of energy and sun element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='solarsystem':
                update.message.reply_text("Solar system is an element combination of planet element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='galaxy':
                update.message.reply_text("Galaxy is an element combination of solarsystem element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='galaxycluster':
                update.message.reply_text("Galaxy cluster is an element combination of galaxy element with itself.\nThe water combined with the soil of ea  rth makes the plant grow strong and develop strong roots. When it fully grows it starts doing the photosynthesis and as a consequence the air element renovates itself, making it almost infinite.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='universe':
                update.message.reply_text("Universe is an element combination of galaxycluster element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='plasma':
                update.message.reply_text("Plasma is an element combination of pressure and heat element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='animal':
                update.message.reply_text("Animal is an element combination of land and life element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='soil':
                update.message.reply_text("Soil is an element combination of rock and life element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='fish':
                update.message.reply_text("Fish is an element combination of animal and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='livestock':
                update.message.reply_text("Livestock is an element combination of farm and animal element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='horse':
                update.message.reply_text("Horse is an element combination of animal and livestock element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='manatee':
                update.message.reply_text("Manatee is an element combination of cow and fish element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='bird':
                update.message.reply_text("Bird is an element combination of animal and air element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='egg':
                update.message.reply_text("Egg is an element combination of bird element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='chicken':
                update.message.reply_text("Chicken is an element combination of egg and farm element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='philosophy':
                update.message.reply_text("Philosophy is an element combination of chicken and egg element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='idea':
                update.message.reply_text("Idea is an element combination of philosophy element with itself. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='roe':
                update.message.reply_text("Roe is an element combination of fish and egg element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='seahorse':
                update.message.reply_text("Seahorse is an element combination of fish and horse element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='pegasus':
                update.message.reply_text("Pegasus is an element combination of horse and bird element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='flyingfish':
                update.message.reply_text("Flyingfish is an element combination of fish and bird element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='hippo':
                update.message.reply_text("Hippo is an element combination of horse and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='milk':
                update.message.reply_text("Milk is an element combination of cow and water element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='steak':
                update.message.reply_text("Steak is an element combination of cow and fir element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='jerky':
                update.message.reply_text("Jerky is an element combination of steak and fire element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='phoenix':
                update.message.reply_text("Phoenix is an element and mythological animal combination of fire and bird element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='omelette':
                update.message.reply_text("Omelette is an element and food combination of fire and egg element. ")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='duck':
                update.message.reply_text("Duck is an animal combination of bird and water element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='airplane':
                update.message.reply_text("Airplane is an element combination of duck and metal element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='small':
                update.message.reply_text("Small is an element and property combination of seahorse and philosophy element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='hummingbird':
                update.message.reply_text("Hummingbird is an element combination of small and bird element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='cow':
                update.message.reply_text("Cow is an element combination of livestock and farm element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='shark':
                update.message.reply_text("Shark is an animal combination of fish and water element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))
            elif context.args[0]=='starfish':
                update.message.reply_text("Starfish is an element combination of earth and water element.")
                context.bot.send_photo(update.message.chat_id, photo=open(f'Elementos/{context.args[0]}.jpg','rb'))         
                
        else:
            update.message.reply_text("The element selected does not exist")
    else:
        update.message.reply_text("FMA Bot not activated")
                
    
#Comanda d'ajuda  
def help(update, context):
    global started
    if started == True:
        m1 = "/combination <element>  <element> | Combines two elements and checks if you've gotten a new one. Replies with your result."
        m2 = "/element <element> | Brew explication of the element with an image that represents it."

        update.message.reply_text(f"{m1}\n{m2}")
    else:
        update.message.reply_text("FMA Bot not activated")
        
#Execcució del bot
def main():
    TOKEN="5711933178:AAEKfTXFbV_WJ9JQIVGJAYX_EepnReYLAnM"
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