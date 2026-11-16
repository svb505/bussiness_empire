import sqlite3


"""Обычный - серый, Нормальный - синий, дорогие - фиолетовый, премиум - красные, 
"""

def main_base():
    images = ["icons/dom1.png", "icons/dom2.png", "icons/dom3.png", "icons/dom4.png",
              "icons/dom5.png", "icons/dom6.png", "icons/dom7.png", "icons/dom8.png",
              "icons/dom9.png", "icons/dom10.png", "icons/dom11.png", "icons/dom12.png"]
    prices = [25000, 32000, 39000, 42500, 47000, 52000, 55000, 61200, 69500, 74000, 89200, 99000]
    regions = ["Detroit", "Clevand", "Baltimore", "Mexico City", "Montgomery", "Kansas City", "Cape Town",
               "Santo Domingo",
               "Bogota", "Memphis", "Buenos Aires", "Houston"]
    countries = ["Michigan", "Ohio", "Maryland", "Mexico", "Alabama", "Kansas", "South Africa", "Dominican Republic",
                 "Columbia", "Tennessee", "Argentina", "Texas"]
    conn = sqlite3.connect("nedv.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS nedv(
                        price INTEGER,
                        image TEXT,
                        region TEXT,
                        country TEXT
                    )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM nedv")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(prices)):
            cursor.execute(
                "INSERT INTO nedv(price, image, region, country) VALUES (?, ?, ?, ?)",
                (prices[i], images[i], regions[i], countries[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM nedv").fetchall()
    print(all[0])
    conn.close()
def coin_base():
    names = [
        "Шиллинг «Новая Англия»",
        "Дублон Брашера в стиле Лимы 1742 года",
        "Аурей императора Тита",
        "Шекель периода Иудейской войны",
        "2000 юаней",
        "5 центов США",
        "Сестерций императора Адриана",
        "Константиновский рубль",
        "Декадрахма Агридженто",
        "5 центов США «Liberty Head»",
        "Золотая монета 1 000 000 канадских долларов",
        ".Аурей императора Брута 42 год до н.э",
        "20 долларов",
        "Золотой динар Омейядов",
        "«Нью-Йоркский золотой дублон»",
        "Доллар 1794 года «Flowing Hair Dollar»"
    ]
    prices = [
        414000,
        700000,
        956000,
        1105375,
        1298000,
        1322500,
        1648805,
        2160000,
        2640000,
        2918000,
        3737500,
        4070000,
        4174000,
        4780000,
        6000000,
        6029400
    ]

    years = [1652,1742,79,1992,1938,1621,1825,220,1913,2007,42,1912,661,1787,1794,1933]
    images = ["icons/coin1.jpg","icons/coin2.jpg","icons/coin4.jpg","icons/coin5.jpg","icons/coin6.jpg","icons/coin7.jpg",
              "icons/coin8.jpg","icons/coin9.png","icons/coin10.jpg","icons/coin11.jpg","icons/coin12.jpg",
              "icons/coin13.jpg","icons/coin14.jpg",
              "icons/coin15.jpg","icons/coin16.jpg","icons/coin17.jpg"]
    conn = sqlite3.connect("coins.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS coins(
                            name TEXT,
                            year INTEGER,
                            price INTEGER,
                            image TEXT
                        )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM coins")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO coins(name, year, price, image) VALUES (?, ?, ?, ?)",
                (names[i], years[i], prices[i], images[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM coins").fetchall()
    print(all[0])
    conn.close()
def cars_base():
    names = ['Bonda Ciwic old','Dobge Corovan','Cabilace UTC','Bonda Ciwic tipe f','DMW m3 e35','Marcedes VV 140','Cabilace Escalade',
             'Marcedes omg s63','Lambargyny urys','macLaren B1','Konigzeg Gamera',
                'Lambargyny Syan','Bugaty Le Voyeture Noare',
             'Rols-Roice Bout Tale','Marcedes VIZIO']
    prices = [1300,3000,6000,14000,25000,40000,90000,160000,195000,1300000,1900000,2500000,19000000,28000000,35000000]
    images = ["icons/ciwic old.jpg","icons/caravan.jpg","icons/utc.jpg","icons/ciwic.jpg","icons/m3 e35.jpg",
              "icons/W140.jpg","icons/escalade.jpg",
              "icons/amg s63.jpg",
              "icons/urus.jpg","icons/b1.jpg",
              "icons/gem.jpg","icons/syan.jpg","icons/bln.jpg","icons/boat tail.jpg","icons/vizion.jpg"]
    raritys = ["old",'old','old',"normal",'normal','normal',"dorog",'dorog','dorog',"super",'super','super',"mill",'mill','mill']
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
                               name TEXT,
                               price INTEGER,
                               image TEXT,
                               rarity TEXT
                           )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM cars")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO cars(name, price, image,rarity) VALUES (?, ?, ?, ?)",
                (names[i], prices[i], images[i],raritys[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM cars").fetchall()
    print(all[0])
    conn.close()
def planes_base():
    names = ['Cezna 150','robertzon z44','Bonanzad 36','Beachkraft cing air d200','Liardjet60',
             'Havvker 900hp','Augusta cw149','Golfstrym g700','Aerobus 480 Prestige']
    prices = [15000,300000,600000,1400000,2500000,4000000,9000000,16000000,19500000]
    images = ['icons/cezna150.jpg', 'icons/robertzonz44.jpg', 'icons/bonanzad36.jpg', 'icons/beachkraft cing air d200.jpg',
              'icons/liardjet60.jpg',
             'icons/havvker900hp.jpg', 'icons/augusta cw149.jpg', 'icons/golfstrym g700.jpg', 'icons/aerobus 480 prestige.jpg']
    conn = sqlite3.connect("planes.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS planes(
                               name TEXT,
                               price INTEGER,
                               image TEXT
                           )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM planes")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO planes(name, price, image) VALUES (?, ?, ?)",
                (names[i], prices[i], images[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM planes").fetchall()
    print(all[0])
    conn.close()
def yaht_base():
    names = ['Mundomarina','Pelorius','Serene','Hydrogen prime','Garden']
    prices = [15000,300000,600000,1400000,2500000,4000000,9000000,16000000,19500000]
    images = ['icons/mundomarina.jpg','icons/pelorius.jpg','icons/serene.jpg','icons/hydrogen prime.jpg','icons/garden.jpg']
    conn = sqlite3.connect("yaht.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS yaht(
                               name TEXT,
                               price INTEGER,
                               image TEXT
                           )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM yaht")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO yaht(name, price, image) VALUES (?, ?, ?)",
                (names[i], prices[i], images[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM yaht").fetchall()
    print(all[0])
    conn.close()
def taxi_base():
    names = ['Bubnai Salaris','Kio Rio','Tobota cabri','Marcedes e','Marcedes meybex',]
    images = ['icons/taxi5.jpg', 'icons/taxi3.jpg', 'icons/taxi2.jpg', 'icons/taxi1.png','icons/taxi4.jpg']
    classes = ["Eco","Eco","Comf","Super","Super"]
    probeg = [120000,234000,453000,567000,987000]
    dohod = [700,1200,1500,4500,5400]
    conn = sqlite3.connect("taxis.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS taxis(
                               name TEXT,
                               probeg INTEGER,
                               image TEXT,
                               class TEXT,
                               dohod INTEGER
                           )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM taxis")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO taxis(name, probeg, image,class,dohod) VALUES (?, ?,?, ?,?)",
                (names[i], probeg[i], images[i],classes[i],dohod[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM taxis").fetchall()
    print(all[0])
    conn.close()
def gruz_base():
    names = ['Fort Transite','VVolkswagen Kraft','Scanniya FX','BAF MX']
    images = ['icons/g3.jpg', 'icons/g2.jpg', 'icons/g1.jpg', 'icons/g4.jpg']
    probeg = [780000,1234000,1453000,1567000,1987000]
    dohod = [1700,11200,11500,14500,15400]
    conn = sqlite3.connect("gruz.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS gruz(
                               name TEXT,
                               probeg INTEGER,
                               image TEXT,
                               dohod INTEGER
                           )""")

    # Проверка, чтобы не вставлять дубли
    cursor.execute("SELECT COUNT(*) FROM gruz")
    count = cursor.fetchone()[0]
    if count == 0:
        for i in range(len(names)):
            cursor.execute(
                "INSERT INTO gruz(name, probeg, image,dohod) VALUES (?,?, ?,?)",
                (names[i], probeg[i], images[i],dohod[i])
            )
        conn.commit()
        print("Данные успешно добавлены в базу.")
    else:
        print("Данные уже существуют в базе, вставка пропущена.")

    all = cursor.execute("SELECT * FROM gruz").fetchall()
    print(all[0])
    conn.close()
gruz_base()

