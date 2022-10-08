# Alchemy Bot: Iker Sánchez & Roger Guinart

Bot de Telegram programat en Python com a projecte per a 2n de DAM, mòdul M13.
Aquest bot utilitza una base de dades guardada a remotemysql.com

El nostre bot és un joc: a partir de quatre elements bàsics (foc, aigua, terra, aire), es troben combinacions que creen nous elements. Per exemple, combinar aigua i aire crea un núvol. 
En aquesta versió hi ha 82 elements. Majoritàriament, només hi ha una combinació per cada element.

Hi ha dos .zips: un té les imatges dels elements i l'altre no. El .zip amb imatges és de gairebé 13 MB, però el que no en té no arriba als 7KB. Aquest projecte l'hem fet per al mòdul M13 de 2n de DAM, i només podem entregar fitxers per sota de 2MB, d'aquí l'existència de dos fitxers .zip.
El programa pot funcionar sense les imatges, simplement no n'envia cap.

Per utilitzar el bot a Telegram, hi ha cinc comandes disponibles:

/start (o /createUser) crea l'usuari i dóna la benvinguda al joc. Benvinguts!
/help Escriu aquesta llista de comandes
/combine (o /combination) <element> <element> combina dos elements i comprova si el resultat és invàlid o si l'usuari ja l'ha desbloquejat.
/elementList (o /listElements) llista els elements desbloquejats per l'usuari
/describe (o /description) <element> escriu una petita descripció d'un element desbloquejat.
/deleteAccount <userID> esborra el progrés de l'usuari. **<userID> ha de ser l'ID del propi usuari, sinó la comanda no funcionarà.**