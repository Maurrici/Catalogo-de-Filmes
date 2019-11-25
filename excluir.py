import pymysql
import json

conexao = pymysql.connect(db="filmesbd", user="root", passwd="")

cursor = conexao.cursor()

with open("catalogo.json", "r") as f:
    catalogo = json.load(f)
    f.close()

for new_movie in catalogo:
    cursor.execute("INSERT INTO filmes VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(new_movie["id"],
        new_movie["name"], new_movie["year"], new_movie["genre"], new_movie["duration"], new_movie["resume"],
                                                                        new_movie["director"], new_movie["link"]))
    conexao.commit()

cursor.close()