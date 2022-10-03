from sqlite3 import connect
import pymysql.cursors

'''
    Aquest script actualitza la base de dades, afegint-hi elements nous. 
    Per afegir elements o combinacions noves, simplement escriu-los com a "element1+element2": "resultElement", i l'script ja els crearà a la BBDD amb IDs.
    Per crear un element bàsic, simplement escriu "element":"element". Per exemple, "fire":"fire". No afegirà res a combinacions.
'''

connection = pymysql.connect(host='remotemysql.com',
                                 user='tz4WJ4N0x7',
                                 password='Tp3GJnuEIf',
                                 database='tz4WJ4N0x7',
                                 cursorclass=pymysql.cursors.DictCursor)


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

def main():
    error = False
    try:

        sqlQuery(f"DELETE FROM Elements")
        sqlQuery(f"DELETE FROM Combinations")
        sqlQuery(f"ALTER TABLE Elements AUTO_INCREMENT = 1")
        i=0
        for key in elements:
            i+=1 


            key1 = ""
            key2 = ""
            first = True
            for char in key:
                if(char == '+'):
                    first = False
                else:
                    if(first):
                        key1+=char
                    else:
                        key2+=char

            value = elements.get(key)
            k1 = selectOne(f"SELECT ElementName FROM Elements WHERE ElementName = '{key1}'")
            if(k1 == None):
                sqlQuery(f"INSERT INTO Elements(ElementName) VALUES('{key1}')")


            k2 = selectOne(f"SELECT ElementName FROM Elements WHERE ElementName = '{key2}'")
            if(k2 == None and key2 != ""):
                sqlQuery(f"INSERT INTO Elements(ElementName) VALUES('{key2}')")

            v  = selectOne(f"SELECT ElementName FROM Elements WHERE ElementName = '{value}'")
            if(v  == None):
                sqlQuery(f"INSERT INTO Elements(ElementName) VALUES('{value}')")
                

            if(key2 != ""):
                k1ID = selectOne(f"SELECT ElementID FROM Elements WHERE ElementName = '{key1}'")
                k2ID = selectOne(f"SELECT ElementID FROM Elements WHERE ElementName = '{key2}'")
                vID  = selectOne(f"SELECT ElementID FROM Elements WHERE ElementName = '{value}'")

                sqlQuery(f"INSERT INTO Combinations(Element1ID, Element2ID, ResultingElement) VALUES ({k1ID}, {k2ID}, {vID})")

            print(f"Element {value} added succesfully!")
    except:
        error = True
        
    if(not error):
        connection.commit()
    

def selectOne(query):
    
            cursor.execute(query)
            data = cursor.fetchone()
            if data == None:
                return None

            for key, value in data.items(): #lole
                return value
            return None

def sqlQuery(query):
    cursor.execute(query)
    connection.commit()




if __name__ == "__main__":
    with connection:
        with connection.cursor() as cursor:
            main()
