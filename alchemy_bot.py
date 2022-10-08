# -*- coding: utf-8 -*-
'''
	FMAlchemyBot
'''
from multiprocessing import context
from telegram.ext import (Updater, CommandHandler)

# Database
from sqlite3 import connect
import pymysql.cursors

# Per comprovar si existeix la imatge de l'element
from os.path import exists

# Error logs
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)



def checkCombination(update, context):
	'''
		Comprova si la combinació de l'usuari és possible.
		Si ho és, desbloqueja l'element resultant, si no s'havia desbloquejat abans.
	'''
	connection = pymysql.connect(host='remotemysql.com',
									user='tz4WJ4N0x7',
									password='Tp3GJnuEIf',
									database='tz4WJ4N0x7',
									cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	if(not userExists(cursor, update.message.chat.username)): # User does not exist
		update.message.reply_text("Error: l'usuari no existeix. Fes servir /start per crear un nou usuari.")
		closeConnection(connection, cursor)
		return

	
	if(len(context.args) != 2):
		update.message.reply_text("Entra dos elements:\n/combination <element> <element>")
		closeConnection(connection, cursor)
		return

	try:
		e1ID = selectOne(cursor, f"SELECT ElementID FROM Elements WHERE ElementName = '{context.args[0].lower()}'")
		e2ID = selectOne(cursor, f"SELECT ElementID FROM Elements WHERE ElementName = '{context.args[1].lower()}'")


		#Si l'element no existeix
		if(e1ID == None):
			update.message.reply_text(f"Error: l'element {context.args[0]} és invàlid.")
			closeConnection(connection, cursor)
			return
		if(e2ID == None):
			update.message.reply_text(f"Error: l'element {context.args[1]} és invàlid.")
			closeConnection(connection, cursor)
			return

		#Si l'element no s'ha desbloquejat
		if  (not checkUnlockedElement(update.message.chat.username, e1ID, cursor)):
			update.message.reply_text(f"Error: l'element {context.args[0]} no està disponible.")
			closeConnection(connection, cursor)
			return
		elif(not checkUnlockedElement(update.message.chat.username, e2ID, cursor)):
			update.message.reply_text(f"Error: l'element {context.args[1]} no està disponible.")
			closeConnection(connection, cursor)
			return

		
		resultID = selectOne(cursor, f"SELECT ResultingElement FROM Combinations WHERE Element1ID = {e1ID} AND Element2ID = {e2ID}")
		if resultID == None:
			resultID = selectOne(cursor, f"SELECT ResultingElement FROM Combinations WHERE Element1ID = {e2ID} AND Element2ID ={e1ID}")
			if resultID == None:
				update.message.reply_text(f"Combinació invàlida.")
				closeConnection(connection, cursor)
				return

		result = selectOne(cursor, f"SELECT ElementName FROM Elements WHERE ElementID = {resultID}")
		if(unlockElement(cursor, update.message.chat.username, resultID)):
			update.message.reply_text(f"Nou element descobert! {context.args[0]} + {context.args[1]} = {result}")
			if(exists(f'img/{context.args[0]}.jpg')):
				context.bot.send_photo(update.message.chat_id, photo=open(f'img/{result}.jpg','rb'))
		else:
			update.message.reply_text(f"{context.args[0]} + {context.args[1]} = {result}\nJa havies desbloquejat l'element anteriorment!")
	except:
		update.message.reply_text(f"Error desconegut.\nTorna-ho a intentar.")

	connection.commit()
	closeConnection(connection, cursor)


def unlockElement(cursor, user, elementID):
	'''
		Si l'usuari user no ha desbloquejat l'element elementID, s'afegeix a la seva llista d'elements desbloquejats.
	'''
	if(checkUnlockedElement(user, elementID, cursor)): #Si l'usuari ja ha desbloquejat l'element
		return False
	else: #Si l'usuari no té l'element
		userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{user}'")
		sqlQuery(cursor, f"INSERT INTO UnlockedElements(UserID, ElementID) VALUES('{userID}', {elementID})")
		return True

def checkUnlockedElement(user, elementID, cursor):
	'''
		Comprova si l'usuari user ha desbloquejat l'element elementID.
	'''
	userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{user}'")
	isUnlocked = selectOne(cursor, f"SELECT ElementID FROM UnlockedElements WHERE UserID = '{userID}' AND ElementID = {elementID}")
	return isUnlocked == None

def unlockedElementsList(update, context):
	'''
		Llista els elements desbloquejats per l'usuari que ha escrit la comanda
	'''
	connection = pymysql.connect(host='remotemysql.com',
									user='tz4WJ4N0x7',
									password='Tp3GJnuEIf',
									database='tz4WJ4N0x7',
									cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()

	if(not userExists(cursor, update.message.chat.username)): # User does not exist
		update.message.reply_text("Error: l'usuari no existeix. Fes servir /start per crear un nou usuari.")
		return


	userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{update.message.chat.username}'")
	totalElements = selectOne(cursor, "SELECT COUNT(*) FROM Elements")
	unlockedElems = selectOne(cursor, f"SELECT COUNT(*) FROM UnlockedElements WHERE UserID = '{userID}'")
	percentatge = round(unlockedElems / totalElements * 100, 2)

	update.message.reply_text(f"Has desbloquejat {unlockedElems} de {totalElements} elements. ({percentatge}%):")


	list = selectAll(cursor, f"SELECT E.ElementName FROM Elements E JOIN UnlockedElements UE ON E.ElementID = UE.ElementID WHERE UE.UserID = '{userID}'")
	
	string = ""
	i=0 #Compta els elements per missatge (max 25)
	j=1 #Enumera els elements quan s'ensenyen. No és l'ID dels elements.
	for dict in list:
		for element in dict.values(): 
			if(i == 25): #Com a molt, s'enviaran 25 elements en un sol missatge.
				update.message.reply_text(f"{string}")
				i = 0
				string = ""
			string+= f"{j}. {element}\n"
			i+=1
			j+=1

	update.message.reply_text(f"{string}")


def elementDescription(update, context):
	'''
		Envia la descripció de l'element que l'usuari especifica, sempre que aquest element estigui desbloquejat.
	'''

	if(len(context.args) != 1):
		update.message.reply_text("Escriu un element:\n/description <element>")
		return
	
	connection = pymysql.connect(host='remotemysql.com',
								 user='tz4WJ4N0x7',
								 password='Tp3GJnuEIf',
								 database='tz4WJ4N0x7',
								 cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()

	description=selectOne(cursor, f"SELECT Description FROM Elements WHERE ElementName='{context.args[0]}'")
	if(description == None):
		update.message.reply_text("Element invàlid.")
	else:
		userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{update.message.chat.username}'")
		if(selectOne(cursor, f"SELECT * FROM UnlockedElements WHERE UserID = '{userID}' AND ElementID=(SELECT ElementID FROM Elements WHERE ElementName='{context.args[0]}')") != None):
			update.message.reply_text(description)
			
			if(exists(f'img/{context.args[0]}.jpg')):
				context.bot.send_photo(update.message.chat_id, photo=open(f'img/{context.args[0]}.jpg','rb'))
		else:
			update.message.reply_text("Element no disponible.")

	closeConnection(connection, cursor)

	
	

def start(update, context):
	''' 
		START: Comprova si existeix l'usuari a la BBDD. Si no existeix, el crea. 
		També li dóna la benvinguda, depenent de si és nou o no, i a més d'això actualitza el seu nom.
		Quan es crea un usuari nou, automàticament desbloqueja els quatre elements bàsics. 
	 '''

	
	connection = pymysql.connect(host='remotemysql.com',
								 user='tz4WJ4N0x7',
								 password='Tp3GJnuEIf',
								 database='tz4WJ4N0x7',
								 cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()

	userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{update.message.chat.username}'")
	if userID == None: #Si l'usuari no existeix
		createUser(cursor, update)
		
		username = selectOne(cursor, f"SELECT UsernameFull FROM Users WHERE UsernameAt = '{update.message.chat.username}'")
		update.message.reply_text(f"Benvingut/da, {username}!\nEscriu /help per veure una llista de comandes.")
		print(f"User {username} created")
		
	else: #Si l'usuari ja existeix
		if username != getName(update):
			username = getName(update)
			sqlQuery(cursor, f"UPDATE Users SET UsernameFull='{username}' WHERE UsernameAt = '{update.message.chat.username}');")
			connection.commit()
		update.message.reply_text(f"Benvingut/da de nou, {username}!")
	
	connection.commit()
	closeConnection(connection, cursor)
	

def getName(update):
	'''
		Obté el nom de l'usuari. Comprova si hi ha cognom i dóna bon format. Per exemple, evita retornar "Roger " o "IkerSanchez"; seria "Roger" i "Iker Sanchez"
	'''
	first_name = update.message.chat.first_name if update.message.chat.first_name != None else ""
	last_name = update.message.chat.last_name if update.message.chat.last_name != None else ""

	if(first_name != "" and last_name != ""): # És a dir, si tots dos existeixen
		first_name += " "

	return first_name+last_name

def userExists(cursor, username):
	'''
		Comprova si l'usuari existeix
	'''
	result = selectOne(cursor, f"SELECT * FROM Users WHERE UsernameAt = '{username}'")

	return result != None


def createUser(cursor, update):
	'''
		Crea un compte nou i l'hi afegeix els quatre elements bàsics.
	'''

	if(selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{update.message.chat.username}'") == None):
		sqlQuery(cursor, f"INSERT INTO Users(UsernameAt, UsernameFull) VALUES('{update.message.chat.username}', '{getName(update)}')")

		#Desbloqueja els quatre elements bàsics
		i=1
		while (i<=4):
			unlockElement(cursor, update.message.chat.username, i)
			i+=1
			
	else:
		print(f"User {update.message.chat.username} already exists")
	


def deleteAccount(update, context):
	'''
		Esborra un compte de les taules Users i UnlockedElements. Si es vol tornar a crear, s'ha de cridar a createUser(update)
	'''
	
	connection = pymysql.connect(host='remotemysql.com',
								 user='tz4WJ4N0x7',
								 password='Tp3GJnuEIf',
								 database='tz4WJ4N0x7',
								 cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()

	if(len(context.args) == 1):
		if(context.args[0] == update.message.chat.username):
			userID = selectOne(cursor, f"SELECT UserID FROM Users WHERE UsernameAt = '{update.message.chat.username}'")
			sqlQuery(cursor, f"DELETE FROM Users WHERE UserID = '{userID}'")
			sqlQuery(cursor, f"DELETE FROM UnlockedElements WHERE UserID = '{userID}'")
			update.message.reply_text("Compte esborrat correctament.")
		else:
			update.message.reply_text(f"Estàs segur que vols borrat el teu progrés?\nEscriu /deleteAccount {update.message.chat.username} per confirmar.")
	else:
		update.message.reply_text(f"Estàs segur que vols borrat el teu progrés?\nEscriu /deleteAccount {update.message.chat.username} per confirmar.")
	
	connection.commit()
	closeConnection(connection, cursor)




def selectOne(cursor, query):
	'''
		Executa SELECT i retorna un sol resultat.
	'''

	cursor.execute(query)
	data = cursor.fetchone()
	if data == None:
		return None

	for key, value in data.items(): #lole
		return value
	return None

def selectAll(cursor, query):
	'''
		Executa SELECT i rotorna tots els resultats 
	'''
	cursor.execute(query)
	return cursor.fetchall()
		

def sqlQuery(cursor, query):
	'''
		Executa una comanda a la base de dades. NO FA COMMIT
	'''
	cursor.execute(query) #No commit here!

def closeConnection(connection, cursor):
	'''
		Tanca la connexió amb la base de dades.
	'''
	cursor.close()
	connection.close()





def help(update, context):
	'''
		Ensenya un missatge amb totes les comandes disponibles
	'''
	msg = "/start || Crea un compte i et dóna la benvinguda."
	msg += "\n/combination <element>  <element> || Combina dos elements i comprova si n'has desbloquejat un de nou."
	msg += "\n/listElements || Llista els elements que has desbloquejat"
	msg += "\n/describe <element> || Descriu un element"
	msg += "\n/deleteAccount <yourID> || Escborra tot el teu progrés"
	update.message.reply_text(msg)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
	TOKEN="5711933178:AAEKfTXFbV_WJ9JQIVGJAYX_EepnReYLAnM" # @FMAlchemyBot
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher
	
	# /comandes
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('createUser',	start))
	dp.add_handler(CommandHandler('combine',	checkCombination))
	dp.add_handler(CommandHandler('combination',	checkCombination))
	dp.add_handler(CommandHandler('describe',	elementDescription))
	dp.add_handler(CommandHandler('description',	elementDescription))
	dp.add_handler(CommandHandler('listElements',	unlockedElementsList))
	dp.add_handler(CommandHandler('elementList',	unlockedElementsList))
	dp.add_handler(CommandHandler('deleteAccount',	deleteAccount))
	dp.add_handler(CommandHandler('help',	help))

	dp.add_error_handler(error_callback)
	updater.start_polling()
    # Deixa el bot esperant comandes
	print("FMAlchemyBot bootup successful")
	updater.idle()

if __name__ == '__main__':
	print(('FMAlchemyBot Starting...'))
	main()