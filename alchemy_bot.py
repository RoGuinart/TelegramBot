# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from multiprocessing import context
import random
from select import select
from telegram import (ParseMode)
from telegram.ext import (Updater, CommandHandler)

#Database
from sqlite3 import connect
import pymysql.cursors

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

connection = pymysql.connect(host='remotemysql.com',
                                 user='tz4WJ4N0x7',
                                 password='Tp3GJnuEIf',
                                 database='tz4WJ4N0x7',
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def checkCombination(update, context):
	'''
		Comprova si la combinació de l'usuari és possible.
		Si ho és, desbloqueja l'element resultant, si no s'havia desbloquejat abans.
	'''
	
	if(len(context.args) != 2):
		update.message.reply_text("Entra dos elements:\n/combination <element> <element>")
		return

	try:
		e1ID = selectOne(f"SELECT ElementID FROM Elements WHERE ElementName = '{context.args[0].lower()}'")
		e2ID = selectOne(f"SELECT ElementID FROM Elements WHERE ElementName = '{context.args[1].lower()}'")
		if(not checkUnlockedElement(update.message.chat.username, e1ID)):
			update.message.reply_text(f"Error: l'element {context.args[0]} no existeix o no s'ha desbloquejat.")
			return
		elif (not checkUnlockedElement(update.message.chat.username, e2ID)):
			update.message.reply_text(f"Error: l'element {context.args[1]} no existeix o no s'ha desbloquejat.")
			return


		
		resultID = selectOne(f"SELECT ResultingElement FROM Combinations WHERE Element1ID = {e1ID} AND Element2ID = {e2ID}")
		if resultID == None:
			resultID = selectOne(f"SELECT ResultingElement FROM Combinations WHERE Element1ID = {e2ID} AND Element2ID ={e1ID}")
			if resultID == None:
				update.message.reply_text(f"Combinació invàlida.")
				return


		result = selectOne(f"SELECT ElementName FROM Elements WHERE ElementID = {resultID}")
		if(unlockElement(update.message.chat.username, resultID)):
			update.message.reply_text(f"Nou element descobert! {context.args[0]} + {context.args[1]} = {result}")
		else:
			update.message.reply_text(f"{context.args[0]} + {context.args[1]} = {result}\nJa havies desbloquejat l'element anteriorment!")
	except:
		update.message.reply_text(f"Error: no s'ha pogut establir connexió amb la base de dades.\nTorna a intentar.")


def getElementDescription(elementName):
    description = selectOne(f"SELECT Description FROM Elements WHERE ElementName LIKE '{elementName}'")
    return description





def unlockElement(user, elementID):
	if(checkUnlockedElement(user, elementID)): #Si l'usuari ja ha desbloquejat l'element
		return False
	else: #Si l'usuari no té l'element
		sqlQuery(f"INSERT INTO UnlockedElements(UserID, ElementID) VALUES('{user}', {elementID})")
		connection.commit()
		return True

def checkUnlockedElement(user, elementID):
	isUnlocked = selectOne(f"SELECT ElementID FROM UnlockedElements WHERE UserID = '{user}' AND ElementID = {elementID}")
	if(isUnlocked == None):
		return False
	else:
		return True

def unlockedElementsList(update, context):
	createUser(update) #En el cas (poc comú) en que no existeixi usuari, es crea. Si ja existeix, no fa res.


	totalElements = selectOne("SELECT COUNT(*) FROM Elements")
	unlockedElems = selectOne(f"SELECT COUNT(*) FROM UnlockedElements WHERE UserID = '{update.message.chat.username}'")
	percentatge = round(unlockedElems / totalElements * 100,2)

	update.message.reply_text(f"Has desbloquejat {unlockedElems} de {totalElements} elements. ({percentatge}%):")


	list = selectAll(f"SELECT E.ElementName FROM Elements E JOIN UnlockedElements UE ON E.ElementID = UE.ElementID WHERE UE.UserID = '{update.message.chat.username}'")
	
	string = ""
	i=0 #Compta els elements per missatge (max 25)
	j=1 #Enumera els elements quan s'ensenyen. No és l'ID dels elements.
	for dict in list:
		for element in dict.values(): 
			if(i == 25): #Com a molt, s'enviaran 25 elements en un sol missatge.
				update.message.reply_text(f"{j}. {string}")
				i = 0
				string = ""
			string+= f"{j}. {element}\n"
			i+=1
			j+=1

	update.message.reply_text(f"{string}")

def start(update, context):
	''' 
		START: Comprova si existeix l'usuari a la BBDD. Si no existeix, el crea. 
		També li dóna la benvinguda, depenent de si és nou o no, i a més d'això actualitza el seu nom.
		Quan es crea un usuari nou, automàticament desbloqueja els quatre elements bàsics. 
	 '''

	username = selectOne(f"SELECT Username FROM Users WHERE UserID = '{update.message.chat.username}'")
	if username == None: #Si l'usuari no existeix
		createUser(update)
		
		username = selectOne(f"SELECT Username FROM Users WHERE UserID = '{update.message.chat.username}'")
		update.message.reply_text(f"Benvingut, {username}!")
		
	else: #Si l'usuari ja existeix
		if username != getName(update):
			username = getName(update)
			sqlQuery(f"UPDATE Users SET Username='{username}' WHERE UserID = '{update.message.chat.username}');")
			connection.commit()
		update.message.reply_text(f"Benvingut de nou, {username}!")
	

def getName(update):
	first_name = update.message.chat.first_name if update.message.chat.first_name != None else ""
	last_name = update.message.chat.last_name if update.message.chat.last_name != None else ""

	if(first_name != "" and last_name != ""): # És a dir, si algun no existeix
		first_name += " "

	return first_name+last_name


def createUser(update):
	'''
		Crea un compte nou i l'hi afegeix els quatre elements bàsics.
	'''
	if(selectOne(f"SELECT UserID FROM Users WHERE UserID = '{update.message.chat.username}'") == None):
		sqlQuery(f"INSERT INTO Users(UserID, Username) VALUES('{update.message.chat.username}', '{getName(update)}')")

		#Desbloqueja els quatre elements bàsics
		i=1
		while (i<=4):
			unlockElement(update.message.chat.username, i)
			i+=1
			
		connection.commit()
	else:
		print(f"User {update.message.chat.username} already exists")


def deleteAccount(update, context):
	'''
		Esborra un compte de les taules Users i UnlockedElements. Si es vol tornar a crear, s'ha de cridar a createUser(update)
	'''
	if(len(context.args) == 1):
		if(context.args[0] == update.message.chat.username):
			sqlQuery(f"DELETE FROM Users WHERE UserID = '{update.message.chat.username}'")
			sqlQuery(f"DELETE FROM UnlockedElements WHERE UserID = '{update.message.chat.username}'")
			connection.commit()
			update.message.reply_text("Compte esborrat correctament.")
	else:
		update.message.reply_text(f"Estàs segur que vols borrat el teu progrés?\nEscriu /deleteAccount {update.message.chat.username} per confirmar.")


def selectOne(query):
    
	cursor.execute(query)
	data = cursor.fetchone()
	if data == None:
		return None

	for key, value in data.items(): #lole
		return value
	return None

def selectAll(query):

	cursor.execute(query)
	data = cursor.fetchall()

	if data == None:
		return None
	else:
		return data
		

def sqlQuery(query):
	cursor.execute(query) #No commit here!






def help(update, context):
	msg = "/combination <element>  <element> | Combines two elements and checks if you've gotten a new one. Replies with your result" 
	msg += "\n/listElements | Lists the elements you have unlocked"
	msg += "\n/deleteAccount <yourID> | Resets all your progress"
	update.message.reply_text(msg)

def main():
	TOKEN="5672783109:AAHPI7aGzq1cYIbFHZzA9x2FeaLkyl0Yl3s"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('combination',	checkCombination))
	dp.add_handler(CommandHandler('listElements',	unlockedElementsList))
	dp.add_handler(CommandHandler('deleteAccount',	deleteAccount))
	dp.add_handler(CommandHandler('help',	help))

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('GuinartBot Starting...'))
	main()