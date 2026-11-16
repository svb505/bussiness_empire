import os
import json
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image, ImageTk,ImageGrab
import random

my_nfts = []  # список NFT объектов
my_badges = []  # знаки отличия пользователя
magazin_mal = 2500
magazin_sred = 7000
magazin_bol = 10000
proi_mal = 3000
proi_sred = 9000
proi_bol = 13000
hired_staff = {"devs": 0, "testers": 0, "designers": 0, "leads": 0}
salary = {
    "devs": 5000,
    "testers": 4000,
    "designers": 4500,
    "leads": 10000
}
my_crypto = []  # портфель пользователя
crypto_market = {
    "Bitcoin": {"price": 30000, "image": "icons/bitcoin.png"},
    "Ethereum": {"price": 2000, "image": "icons/ethereum.png"},
    "Dogecoin": {"price": 0.1, "image": "icons/dogecoin.png"}
}
price_level_mag1 = 100
price_level_mag2 = 200
price_level_mag3 = 300
price_level_pro1 = 300
price_level_pro2 = 400
price_level_pro3 = 600
total_fortune = 0
total_income_per_hour = 0
SAVE_FILE = "settings/last_exit.json"
MAX_INCOME_HOURS = 2
INCOME_PER_HOUR = 10
dohod_nedv = 0
nedv_for_rinok = []
my_nedvi = []
all_coins = []
all_cars = []
all_planes = []
all_yahts = []
my_cars = []
my_planes = []
my_yahts = []
my_coins = []
gruz_cars = []
max_slots = 5
extra_slots = 0  # можно увеличить за деньги
taxis_cars = []
balance = 0
CRYPTO_SAVE_FILE = "settings/crypto_portfolio.json"

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
if os.path.exists("my_nedv.db"):
    conn = sqlite3.connect("my_nedv.db")
    cursor = conn.cursor()
    all = cursor.execute("SELECT * FROM my_nedv").fetchall()
    for i in range(len(all)):
        my_nedvi.append({"price": all[i][0], "image": all[i][1], "city": all[i][2], "region": all[i][3]})
    conn.close()
balance = 0
conn = sqlite3.connect("taxis.db")
cursor = conn.cursor()
all = cursor.execute("SELECT * FROM taxis").fetchall()
for i in range(len(all)):
    taxis_cars.append({"name": all[i][0], "probeg": all[i][1], "image": all[i][2], "class": all[i][3],"dohod":all[i][4]})
conn.close()

conn = sqlite3.connect("gruz.db")
cursor = conn.cursor()
all = cursor.execute("SELECT * FROM gruz").fetchall()
for i in range(len(all)):
    gruz_cars.append(
        {"name": all[i][0], "probeg": all[i][1], "image": all[i][2], "dohod": all[i][3]})
conn.close()
#------------------------------
def load_balance():
    global balance
    try:
        with open("settings/balance.bin", "rb") as f:
            # Чтение 4 байт из файла и преобразование в целое число
            balance = int.from_bytes(f.read(4), byteorder='little', signed=True)
    except FileNotFoundError:
        # Если файл не существует, начинаем с нулевого баланса
        balance = 0
def save_balance():
    global balance
    with open("settings/balance.bin", "wb") as f:
        f.write(int(balance).to_bytes(4, byteorder='little', signed=True))
def load_slots():
    global extra_slots
    if os.path.exists("settings/extra_slots.cfg"):
        with open("settings/extra_slots.cfg", "r") as f:
            extra_slots = int(f.read())
def save_slots():
    with open("settings/extra_slots.cfg", "w") as f:
        f.write(str(extra_slots))
def save_crypto_data():
    with open(CRYPTO_SAVE_FILE, "w") as f:
        json.dump(my_crypto, f)
def load_crypto_data():
    global my_crypto
    if os.path.exists(CRYPTO_SAVE_FILE):
        with open(CRYPTO_SAVE_FILE, "r") as f:
            my_crypto = json.load(f)
    else:
        my_crypto = []
def save_my_nfts():
    with open("settings/nfts.json", "w") as f:
        json.dump(my_nfts, f)
def load_my_nfts():
    global my_nfts
    if os.path.exists("settings/nfts.json"):
        with open("settings/nfts.json", "r") as f:
            my_nfts = json.load(f)
    else:
        my_nfts = []
def save_badges():
    with open("settings/badges.json", "w") as f:
        json.dump(my_badges, f)
def load_badges():
    global my_badges
    if os.path.exists("settings/badges.json"):
        with open("settings/badges.json", "r") as f:
            my_badges = json.load(f)
    else:
        my_badges = []
#-------------------------------
def save_exit_time():
    data = {
        "last_exit": datetime.now().isoformat()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
def load_last_exit_time():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    return datetime.fromisoformat(data["last_exit"])
def calculate_income(last_exit):
    if last_exit is None:
        return 0
    now = datetime.now()
    delta = now - last_exit
    hours = delta.total_seconds() / 3600
    hours_capped = min(hours, MAX_INCOME_HOURS)
    income = int(hours_capped * INCOME_PER_HOUR)
    return income
def calculate_total_hourly_income():
    return sum(item['price'] // 100 for item in my_nedvi)
def add_offline_income():
    last_exit = load_last_exit_time()
    now = datetime.now()
    if last_exit:
        delta = now - last_exit
        hours = delta.total_seconds() / 3600
        capped_hours = min(hours, MAX_INCOME_HOURS)

        hourly_income = calculate_total_hourly_income()
        shop_income = calculate_shop_income()
        factory_income = calculate_factory_income()
        vehicle_income = calculate_vehicle_income()
        crypto_income = int(sum(crypto_market[c["name"]]["price"] * 0.01 for c in my_crypto))
        nft_income = sum(n.get("income", 0) for n in my_nfts)

        earned = int((hourly_income + shop_income + factory_income + vehicle_income + nft_income) * capped_hours)
        earned += int(crypto_income * capped_hours)

        if earned > 0:
            global balance
            balance += earned
            save_balance()
            messagebox.showinfo("Добро пожаловать!",
                f"Пока вас не было {int(hours)} ч. {int(delta.seconds % 3600) // 60} мин.\n"
                f"Доход от недвижимости: +${int(hourly_income * capped_hours)}\n"
                f"Доход от магазинов: +${int(shop_income * capped_hours)}\n"
                f"Доход от производств: +${int(factory_income * capped_hours)}\n"
                f"Доход от транспорта: +${int(vehicle_income * capped_hours)}\n"
                f"Доход от крипты: +${int(crypto_income * capped_hours)}\n"
                f"Доход от NFT: +${int(nft_income * capped_hours)}\n"
                f"Итого: +${earned}")
def add_vehicle_to_slot(db, table, name, probeg, dohod, image):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, probeg INTEGER, dohod INTEGER, image TEXT)")
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if count >= max_slots + extra_slots:
        messagebox.showwarning("Нет мест", "Нет свободных слотов. Купите дополнительные.")
        conn.close()
        return
    cursor.execute(f"INSERT INTO {table} VALUES(?, ?, ?, ?)", (name, probeg, dohod, image))
    conn.commit()
    conn.close()
    messagebox.showinfo("Куплено", f"{name} добавлено в парк.")
def update_crypto_prices():
    for coin in crypto_market.values():
        change = random.uniform(-0.05, 0.05)  # ±5%
        coin["price"] *= (1 + change)
        coin["price"] = round(coin["price"], 2)
    Win.after(5000, update_crypto_prices)
#-------------------------------
def create_my_planes_base(price,name,image):
    conn = sqlite3.connect("my_planes.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_planes(
                        price INTEGER,
                        name TEXT,
                        image TEXT
                    )""")
    conn.commit()
    cursor.execute("INSERT INTO my_planes(price,name,image) VALUES(?,?,?)",(price,name,image))
    conn.commit()
    conn.close()
def create_my_yahts_base(price,name,image):
    conn = sqlite3.connect("my_yahts.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_yahts(
                        price INTEGER,
                        name TEXT,
                        image TEXT
                    )""")
    conn.commit()
    cursor.execute("INSERT INTO my_yahts(price,name,image) VALUES(?,?,?)",(price,name,image))
    conn.commit()
    conn.close()
def create_my_cars_base(price,name,rarity,image):
    conn = sqlite3.connect("my_cars.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_cars(
                        price INTEGER,
                        name TEXT,
                        rarity TEXT,
                        image TEXT
                    )""")
    conn.commit()
    cursor.execute("INSERT INTO my_cars(price,name,rarity,image) VALUES(?,?,?,?)",(price,name,rarity,image))
    conn.commit()
    conn.close()
def create_my_nedv_base(price,image,city,region):
    conn = sqlite3.connect("my_nedv.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_nedv(
                        price INTEGER,
                        image TEXT,
                        region TEXT,
                        country TEXT
                    )""")
    conn.commit()
    cursor.execute("INSERT INTO my_nedv(price,image,region,country) VALUES(?,?,?,?)",(price,image,region,city))
    conn.commit()
    conn.close()
def create_my_coins_base(name,year,image,price):
    conn = sqlite3.connect("my_coins.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_coins(
                        price INTEGER,
                        name TEXT,
                        year INTEGER,
                        image TEXT
                    )""")
    conn.commit()
    cursor.execute("INSERT INTO my_coins(price,name,year,image) VALUES(?,?,?,?)",(price,name,year,image))
    conn.commit()
    conn.close()
def delete_data(price,image,city,region):
    conn = sqlite3.connect("nedv.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nedv WHERE price = ? AND image = ? AND region = ? AND country = ?",
                   (price, image, region, city))

    conn.commit()
    conn.close()
def create_my_taxi_base(probeg,name,dohod,image):
    conn = sqlite3.connect("my_taxi.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_taxi(
    name TEXT,
    probeg INTEGER,
    dohod INTEGER,
    image TEXT
)""")
    conn.commit()
    cursor.execute("INSERT INTO my_taxi(probeg,name,dohod,image) VALUES(?,?,?,?)",(probeg,name,dohod,image))
    conn.commit()
    conn.close()
def create_my_gruz_base(probeg,name,dohod,image):
    conn = sqlite3.connect("my_gruz.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_gruz(
    name TEXT,
    probeg INTEGER,
    dohod INTEGER,
    image TEXT
)""")
    conn.commit()
    cursor.execute("INSERT INTO my_gruz(probeg,name,dohod,image) VALUES(?,?,?,?)",(probeg,name,dohod,image))
    conn.commit()
    conn.close()
def create_business(name, biz_type):
    conn = sqlite3.connect("businesses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biz (
            name TEXT,
            type TEXT
        )
    """)
    cursor.execute("INSERT INTO biz (name, type) VALUES (?, ?)", (name, biz_type))
    conn.commit()
    conn.close()
def get_all_businesses():
    if not os.path.exists("businesses.db"):
        return []

    conn = sqlite3.connect("businesses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biz (
            name TEXT,
            type TEXT
        )
    """)
    all = cursor.execute("SELECT name, type FROM biz").fetchall()
    conn.close()
    return [{"name": row[0], "type": row[1]} for row in all]
def delete_business(name, biz_type):
    conn = sqlite3.connect("businesses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM biz WHERE name=? AND type=?", (name, biz_type))
    conn.commit()
    conn.close()
    messagebox.showinfo("Удалено", f"Бизнес '{name}' удалён.")
    bisunes()
def buy_slot_logic(btype):
    global balance, extra_slots
    cost = 10000 * (extra_slots + 1)
    if balance >= cost:
        balance -= cost
        extra_slots += 1
        save_balance()
        messagebox.showinfo("Слот куплен", f"Вы купили слот. Всего: {max_slots + extra_slots}")
    else:
        messagebox.showwarning("Недостаточно средств", "Пополните баланс")
def upgrade_shop(name):
    otkr_magazin_info(name, 1000, 2500)  # Поставь реальные значения или сделай поиск по имени
def upgrade_factory(name):
    otkr_proiz_info(name, 3000, 3500)  # Тоже подставь значения в соответствии с именем
def create_build_orders_table():
    conn = sqlite3.connect("build.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS build_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            reward INTEGER,
            iron_needed INTEGER,
            concrete_needed INTEGER,
            wood_needed INTEGER,
            built INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
def add_build_order(name, reward, iron, concrete, wood):
    conn = sqlite3.connect("build.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO build_orders (name, reward, iron_needed, concrete_needed, wood_needed) VALUES (?, ?, ?, ?, ?)",
                   (name, reward, iron, concrete, wood))
    conn.commit()
    conn.close()
def create_it_projects_table():
    conn = sqlite3.connect("it_projects.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            reward INTEGER,
            devs_needed INTEGER,
            testers_needed INTEGER,
            designers_needed INTEGER,
            leads_needed INTEGER,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
def seed_build_projects():
    add_build_order("ТЦ Мега", 150000, 100, 200, 50)
    add_build_order("Офис центр", 100000, 80, 150, 40)
    add_build_order("Дом элитный", 120000, 60, 100, 70)
    add_build_order("Элитный ЖК", 1200000, 600, 1000, 700)
def seed_it_projects():
    conn = sqlite3.connect("it_projects.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO projects (name, reward, devs_needed, testers_needed, designers_needed, leads_needed) VALUES (?, ?, ?, ?, ?, ?)", [
        ("Верстка сайта", 50000, 2, 1, 1, 0),
        ("Разработка игры", 150000, 4, 3, 2, 1),
        ("Разработка ОС", 250000, 6, 4, 2, 2),
        ("Мобильное приложение", 80000, 3, 2, 2, 1),
    ])
    conn.commit()
    conn.close()
# -------------------------------
def invest():
    def rinok():
        def buy(price, image, city, region):
            global balance, total_fortune, total_income_per_hour
            load_balance()
            if balance >= price:
                delete_data(price, image, city, region)
                create_my_nedv_base(price, image, city, region)
                balance -= price
                total_fortune += price
                total_income_per_hour += price // 1000
                save_balance()
                messagebox.showinfo("Успешно", "Недвижимость куплена!")
            else:
                messagebox.showwarning("Внимание", "Недостаточно средств")

        global nedv_for_rinok
        nedv_for_rinok = []
        conn = sqlite3.connect("nedv.db")
        cursor = conn.cursor()
        all = cursor.execute("SELECT * FROM nedv").fetchall()
        for i in range(len(all)):
            nedv_for_rinok.append({"price": all[i][0], "image": all[i][1], "city": all[i][2], "region": all[i][3]})
        conn.close()
        w = Toplevel(Win)
        w.geometry('500x400')
        w.title("Рынок недвижимости")

        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        image1 = Image.open('icons/map.png').resize((20, 20))
        map = ImageTk.PhotoImage(image1)

        for item in nedv_for_rinok:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=f"$ {item['price']}").grid(row=0, column=1, sticky=W)
            Label(frame, image=map).grid(row=1, column=1, sticky=W)
            Label(frame, text=item['city']).grid(row=1, column=2, sticky=W)
            Label(frame, text=item['region']).grid(row=2, column=1, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["price"], img=item["image"], c=item["city"], r=item["region"]:
                       buy(p, img, c, r)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку

    def my_nedv():
        def sell(price, image, city, region):
            global balance, total_fortune, total_income_per_hour

            price = int(price)
            conn = sqlite3.connect("my_nedv.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_nedv WHERE price=? AND image=? AND region=? AND country=?",
                           (price, image, region, city))
            conn.commit()
            conn.close()

            balance += price
            total_fortune -= price
            total_income_per_hour -= price // 1000
            save_balance()
            messagebox.showinfo("Продано", "Недвижимость продана.")

        w = Toplevel(Win)
        w.geometry("500x400")
        w.title("Моя недвижимость")

        global my_nedvi

        if not my_nedvi:
            Label(w, text='Вы не владеете недвижимостью', font=("Arial", 16, "bold")).pack()
            Label(w, text='Посетите рынок, чтобы приобрести недвижимость').pack()
            return

        # === Скроллбар + Canvas ===
        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        map_img = Image.open('icons/map.png').resize((20, 20))
        map = ImageTk.PhotoImage(map_img)

        for item in my_nedvi:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=f"$ {item['price']}").grid(row=0, column=1, sticky=W)
            Label(frame, image=map).grid(row=1, column=1, sticky=W)
            Label(frame, text=item['city']).grid(row=1, column=2, sticky=W)
            Label(frame, text=item['region']).grid(row=2, column=1, sticky=W)
            ttk.Button(frame, text='Продать',
                       command=lambda p=item["price"], img=item["image"], c=item["city"], r=item["region"]:
                       sell(p, img, c, r)).grid(row=0, column=3, rowspan=3)

            # сохранить изображение, чтобы не исчезало
            frame.image = photo
            frame.map_icon = map

    global dohod_nedv
    Label(tab1,text = 'Недвижимость',font = ("Arial",16,"bold")).pack()
    Label(tab1, text=f'$ {dohod_nedv}').pack()
    Label(tab1, text='Доход от аренды в час').pack()
    ttk.Button(tab1,text = "Рынок недвижимости",command = rinok).pack()
    ttk.Button(tab1,text = "Моя недвижимость",command = my_nedv).pack()
    ttk.Button(tab1, text="Крипторынок", command=crypto_market_window).pack()
    ttk.Button(tab1, text="NFT", command=show_nft_market).pack()
def zarabotok():
    def func(event):
        nonlocal per_click, click_balance
        global balance
        balance += per_click
        click_balance += per_click
        save_balance()
        label_balance.config(text=f"$ {balance:.2f}")
        write_click_balance(click_balance)

        # Прогресс до следующего уровня
        if click_balance >= upgrade_cost:
            level_up()

        update_progress_bar()
    def level_up():
        nonlocal level, per_click, click_balance, upgrade_cost
        click_balance = 0
        level += 1
        write_level(level)
        per_click += 1  # или *= 2 для ускорения роста
        write_per_click(per_click)
        upgrade_cost *= 2
        write_update_cost(upgrade_cost)
        label_per_click.config(text=f"$ {per_click:.2f} per click")
        label_levels.config(text=f"{level} level")
        click_balance = 0
        write_click_balance(click_balance)

    def update_progress_bar():
        progress = min(click_balance / upgrade_cost, 1.0)
        progress_var.set(progress)
        label_upgrade.config(text=f"$ {upgrade_cost - click_balance:.0f} до след. уровня")

    # Начальные значения
    global balance
    load_balance()
    per_click = func_per_click()
    level = func_level()
    click_balance = func_click_balance()  # Вместо click_balance = balance

    upgrade_cost = func_update_cost()

    # Очистка таба
    for widget in tab3.winfo_children():
        widget.destroy()

    # Верхняя панель (баланс)
    card = Frame(tab3, bg="#1c1c1c", padx=10, pady=10)
    card.pack(fill=X, padx=10, pady=10)

    Label(card, text="Balance:", fg="white", bg="#1c1c1c", font=("Arial", 12)).pack(anchor=W)
    label_balance = Label(card, text=f"$ {balance:.2f}", fg="white", bg="#1c1c1c", font=("Arial", 24, "bold"))
    label_balance.pack(anchor=W)

    # Панель клика и уровня
    stats_frame = Frame(tab3, bg="#263859", pady=10)
    stats_frame.pack(fill=X, padx=10)

    label_per_click = Label(stats_frame, text=f"$ {per_click:.2f} per click", fg="white", bg="#263859", font=("Arial", 12))
    label_per_click.pack()

    label_levels = Label(stats_frame, text=f"{level} level", fg="white", bg="#263859", font=("Arial", 12))
    label_levels.pack()

    progress_var = IntVar()
    progress_bar = ttk.Progressbar(stats_frame, variable=progress_var, maximum=1.0, length=300)
    progress_bar.pack(pady=5)

    label_upgrade = Label(stats_frame, text=f"$ {upgrade_cost} до след. уровня", fg="white", bg="#263859", font=("Arial", 10))
    label_upgrade.pack()

    # Зона клика
    click_area = Frame(tab3, bg="white")
    click_area.pack(expand=True, fill=BOTH)

    image = Image.open('icons/click.png').resize((100, 100))
    click_img = ImageTk.PhotoImage(image)

    click_label = Label(click_area, image=click_img, bg="white")
    click_label.image = click_img
    click_label.pack(pady=50)
    click_label.bind("<Button-1>", func)

    # Обновление прогресса при запуске
    update_progress_bar()
def predm():
    def show_coins():
        def buy(name, year, image, price):
            global balance, total_fortune, total_income_per_hour
            load_balance()
            if balance >= price:
                create_my_coins_base(name, year, image, price)

                # УДАЛЕНИЕ монеты из общей БД:
                conn = sqlite3.connect("coins.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM coins WHERE name=? AND year=? AND image=? AND price=?",
                               (name, year, image, price))
                conn.commit()
                conn.close()

                balance -= price
                total_fortune += price
                total_income_per_hour += price // 1000
                save_balance()
                messagebox.showinfo("Успешно", "Монета куплена!")
            else:
                messagebox.showwarning("Внимание", "Недостаточно средств")

        global all_coins
        all_coins = []
        conn = sqlite3.connect("coins.db")
        cursor = conn.cursor()
        all = cursor.execute("SELECT * FROM coins").fetchall()
        for i in range(len(all)):
            all_coins.append({"name": all[i][0], "year": all[i][1], "price": all[i][2], "image": all[i][3]})
        w = Toplevel(Win)
        w.geometry('550x400')
        w.title("")

        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in all_coins:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Цена: $ {item['price']}",font = ("Arial",9,"bold")).grid(row=1, column=2, sticky=W)
            Label(frame, text=f"Год: {item['year']}").grid(row=2, column=1, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["price"], img=item["image"], y=item["year"], n=item["name"]:
                       buy(n,y,img,p)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
    def show_cars():
        def buy(price,name,rarity,image):
            global balance, total_fortune, total_income_per_hour
            load_balance()
            if balance >= price:
                create_my_cars_base(price,name,rarity,image)
                balance -= price
                total_fortune += price
                total_income_per_hour += price // 1000
                save_balance()
                messagebox.showinfo("Успешно", "Монета куплена!")
            else:
                messagebox.showwarning("Внимание", "Недостаточно средств")
        global all_cars
        all_cars = []
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        all = cursor.execute("SELECT * FROM cars").fetchall()
        for i in range(len(all)):
            all_cars.append({"name": all[i][0], "price": all[i][1], "image": all[i][2], "rarity": all[i][3]})
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")

        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in all_cars:
            color = ""
            if item["rarity"] == "old":
                color = "gray"
            if item["rarity"] == "normal":
                color = 'lightblue'
            if item["rarity"] == "dorog":
                color = "violet"
            if item["rarity"] == "super":
                color = "red"
            if item["rarity"] == "mill":
                color = "yellow"
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5,background=color)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((170, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"],bg = color).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Цена: $ {item['price']}",font = ("Arial",9,"bold"),bg = color).grid(row=1, column=2, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["price"], img=item["image"], r=item["rarity"], n=item["name"]:
                       buy(p,n,r,img)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
    def show_planes():
        def buy(price,name,image):
            global balance, total_fortune, total_income_per_hour
            load_balance()
            if balance >= price:
                create_my_planes_base(price,name,image)
                balance -= price
                total_fortune += price
                total_income_per_hour += price // 1000
                save_balance()
                messagebox.showinfo("Успешно", "Монета куплена!")
            else:
                messagebox.showwarning("Внимание", "Недостаточно средств")
        global all_planes
        all_planes = []
        conn = sqlite3.connect("planes.db")
        cursor = conn.cursor()
        all = cursor.execute("SELECT * FROM planes").fetchall()
        for i in range(len(all)):
            all_planes.append({"name": all[i][0], "price": all[i][1], "image": all[i][2]})
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")

        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in all_planes:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((170, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Цена: $ {item['price']}",font = ("Arial",9,"bold")).grid(row=1, column=2, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["price"], img=item["image"], n=item["name"]:
                       buy(p,n,img)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
    def show_yahts():
        def buy(price, name, image):
            global balance, total_fortune, total_income_per_hour
            load_balance()
            if balance >= price:
                create_my_yahts_base(price, name, image)
                balance -= price
                total_fortune += price
                total_income_per_hour += price // 1000
                save_balance()
                messagebox.showinfo("Успешно", "Монета куплена!")
            else:
                messagebox.showwarning("Внимание", "Недостаточно средств")

        global all_yahts
        all_yahts = []
        conn = sqlite3.connect("yaht.db")
        cursor = conn.cursor()
        all = cursor.execute("SELECT * FROM yaht").fetchall()
        for i in range(len(all)):
            all_yahts.append({"name": all[i][0], "price": all[i][1], "image": all[i][2]})
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")

        canvas = Canvas(w)
        scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in all_yahts:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((170, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Цена: $ {item['price']}", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["price"], img=item["image"], n=item["name"]:
                       buy(p, n, img)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
    def cars():
        def sell(price, name, image):
            global balance, total_fortune, total_income_per_hour

            price = int(price)
            conn = sqlite3.connect("my_cars.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_cars WHERE price=? AND image=? AND name=? AND rarity=?",
                           (price, image, name,r))
            conn.commit()
            conn.close()

            balance += price
            total_fortune -= price
            total_income_per_hour -= price // 1000
            save_balance()
            messagebox.showinfo("Продано", "Недвижимость продана.")

        global my_cars
        my_cars = []
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")
        if os.path.exists('my_cars.db'):
            conn = sqlite3.connect("my_cars.db")
            cursor = conn.cursor()
            all = cursor.execute("SELECT * FROM my_cars").fetchall()
            print(all)
            for i in range(len(all)):
                my_cars.append({"price": all[i][0], "name": all[i][1], "rarity": all[i][2],"image": all[i][3]})
            print(my_cars)
            canvas = Canvas(w)
            scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            for item in my_cars:
                color = ""
                if item["rarity"] == "old":
                    color = "gray"
                if item["rarity"] == "normal":
                    color = 'lightblue'
                if item["rarity"] == "dorog":
                    color = "violet"
                if item["rarity"] == "super":
                    color = "red"
                if item["rarity"] == "mill":
                    color = "yellow"
                frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5,background=color)
                frame.pack(pady=5, padx=5, fill=X)

                img = Image.open(item['image']).resize((170, 100))
                photo = ImageTk.PhotoImage(img)

                Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
                Label(frame, text=item["name"],bg = color,).grid(row=0, column=1, sticky=W)
                Label(frame, text=f"Цена: $ {item['price']}", bg = color,font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
                ttk.Button(frame, text='Продать',
                           command=lambda p=item["price"], img=item["image"], n=item["name"],r = item["rarity"]:
                           sell(p, n, img,r)).grid(row=0, column=3, rowspan=3)

                frame.image = photo  # сохранить ссылку
        else:
            Label(w, text="У вас нету машин", font=("Arial", 16, 'bold')).pack()
    def planes():
        def sell(price, name, image):
            global balance, total_fortune, total_income_per_hour

            price = int(price)
            conn = sqlite3.connect("my_planes.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_yahts WHERE price=? AND image=? AND name=?",
                           (price, image, name))
            conn.commit()
            conn.close()

            balance += price
            total_fortune -= price
            total_income_per_hour -= price // 1000
            save_balance()
            messagebox.showinfo("Продано", "Недвижимость продана.")

        global my_planes
        my_planes = []
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")
        if os.path.exists('my_planes.db'):
            conn = sqlite3.connect("my_planes.db")
            cursor = conn.cursor()
            all = cursor.execute("SELECT * FROM my_planes").fetchall()
            for i in range(len(all)):
                my_planes.append({"name": all[i][0], "price": all[i][1], "image": all[i][2]})

            canvas = Canvas(w)
            scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            for item in my_planes:
                frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
                frame.pack(pady=5, padx=5, fill=X)

                img = Image.open(item['image']).resize((170, 100))
                photo = ImageTk.PhotoImage(img)

                Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
                Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
                Label(frame, text=f"Цена: $ {item['price']}", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
                ttk.Button(frame, text='Продать',
                           command=lambda p=item["price"], img=item["image"], n=item["name"]:
                           sell(p, n, img)).grid(row=0, column=3, rowspan=3)

                frame.image = photo  # сохранить ссылку
        else:
            Label(w, text="У вас нету самолетов", font=("Arial", 16, 'bold')).pack()
    def yahts():
        def sell(price, name, image):
            global balance, total_fortune, total_income_per_hour

            price = int(price)
            conn = sqlite3.connect("my_yahts.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_yahts WHERE price=? AND image=? AND name=?",
                           (price, image, name))
            conn.commit()
            conn.close()

            balance += price
            total_fortune -= price
            total_income_per_hour -= price // 1000
            save_balance()
            messagebox.showinfo("Продано", "Недвижимость продана.")

        global my_yahts
        my_yahts = []
        w = Toplevel(Win)
        w.geometry('650x500')
        w.title("")
        if os.path.exists('my_yahts.db'):
            conn = sqlite3.connect("my_yaht.db")
            cursor = conn.cursor()
            all = cursor.execute("SELECT * FROM my_yaht").fetchall()
            for i in range(len(all)):
                my_yahts.append({"name": all[i][0], "price": all[i][1], "image": all[i][2]})


            canvas = Canvas(w)
            scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            for item in my_yahts:
                frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
                frame.pack(pady=5, padx=5, fill=X)

                img = Image.open(item['image']).resize((170, 100))
                photo = ImageTk.PhotoImage(img)

                Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
                Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
                Label(frame, text=f"Цена: $ {item['price']}", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
                ttk.Button(frame, text='Продать',
                           command=lambda p=item["price"], img=item["image"], n=item["name"]:
                           sell(p, n, img)).grid(row=0, column=3, rowspan=3)

                frame.image = photo  # сохранить ссылку
        else:
            Label(w,text = "У вас нету яхт",font = ("Arial",16,'bold')).pack()
    ttk.Button(tab4,text = "Гараж",command = cars).pack(side = TOP)
    ttk.Button(tab4, text="Ангар", command= planes).pack(side = TOP)
    ttk.Button(tab4, text="Яхты", command= yahts).pack(side = TOP)
    left_frame = Frame(tab4)
    left_frame.pack(side = LEFT)
    left_frame2 = Frame(tab4)
    left_frame2.pack(side=LEFT)

    image1 = Image.open('icons/coin1.jpg')
    image1 = image1.resize((60, 60))
    photo1 = ImageTk.PhotoImage(image1)
    image2 = Image.open('icons/car.png')
    image2 = image2.resize((60, 60))
    photo2 = ImageTk.PhotoImage(image2)
    image3 = Image.open('icons/plane.png')
    image3 = image3.resize((60, 60))
    photo3 = ImageTk.PhotoImage(image3)
    image4 = Image.open('icons/yaht.png')
    image4 = image4.resize((60, 60))
    photo4 = ImageTk.PhotoImage(image4)

    btn = Button(left_frame, image=photo2, command=show_cars)
    btn.image = photo2
    btn.pack()
    btn = Button(left_frame, image=photo3, command=show_planes)
    btn.image = photo3
    btn.pack()
    btn = Button(left_frame, image=photo4, command=show_yahts)
    btn.image = photo4
    btn.pack()
    btn = Button(left_frame2,image = photo1,command = show_coins)
    btn.image = photo1
    btn.pack()
def taxi():
        def buy_slot():
            global balance, extra_slots
            cost = 10000 * (extra_slots + 1)
            if balance >= cost:
                balance -= cost
                extra_slots += 1
                save_balance()
                messagebox.showinfo("Успешно",
                                    f"Вы купили дополнительный слот. Всего слотов: {max_slots + extra_slots}")
            else:
                messagebox.showwarning("Ошибка", "Недостаточно средств.")
        def pay(name, probeg, dohod, image,table = "my_taxi.db"):
            add_vehicle_to_slot("my_taxi.db", "my_taxi", name, probeg, dohod, image)
            conn = sqlite3.connect("my_taxi.db")
            cursor = conn.cursor()
            count = cursor.execute("SELECT COUNT(*) FROM {}".format(table.split('.')[0])).fetchone()[0]
            if count < max_slots + extra_slots:
                cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?)".format(table.split('.')[0]),
                               (name, probeg, dohod, image))
                conn.commit()
                conn.close()
                messagebox.showinfo("Куплено", f"{name} добавлено в ваш автопарк.")
            else:
                conn.close()
                messagebox.showwarning("Нет слотов", "Нет свободных слотов. Купите дополнительные.")

        global gruz_cars
        window = Toplevel(Win)
        window.geometry("500x400")
        window.title("Таксопарк")
        display_slots_ui(window, "my_taxi.db", "my_taxi")
        ttk.Button(window, text="Купить слот", command=buy_slot).pack(pady=5)
        canvas = Canvas(window)
        scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in taxis_cars:
            cls = ""
            if item["class"] == "Eco":
                cls = "Економ"
            if item["class"] == "Comf":
                cls = "Комфорт"
            else:
                cls = "Бизнесс класс"
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((170, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Пробег: {item['probeg']}", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
            Label(frame, text=f"Класс: {cls}", font=("Arial", 9, "bold")).grid(row=2, column=2, sticky=W)
            Label(frame, text=f"Доход в час: {item['dohod']}").grid(row=3, column=2, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["probeg"], img=item["image"], n=item["name"],d = item["dohod"]:
                       pay(n, p,d,img)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
def gruz():
        def buy_slot():
            global balance, extra_slots
            cost = 10000 * (extra_slots + 1)
            if balance >= cost:
                balance -= cost
                extra_slots += 1
                save_balance()
                messagebox.showinfo("Успешно",
                                    f"Вы купили дополнительный слот. Всего слотов: {max_slots + extra_slots}")
            else:
                messagebox.showwarning("Ошибка", "Недостаточно средств.")
        def pay(name, probeg, dohod, image,table = "my_gruz.db"):
            add_vehicle_to_slot("my_gruz.db", "my_gruz", name, probeg, dohod, image)
            conn = sqlite3.connect("my_gruz.db")
            cursor = conn.cursor()
            count = cursor.execute("SELECT COUNT(*) FROM {}".format(table.split('.')[0])).fetchone()[0]
            if count < max_slots + extra_slots:
                cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?)".format(table.split('.')[0]),
                               (name, probeg, dohod, image))
                conn.commit()
                conn.close()
                messagebox.showinfo("Куплено", f"{name} добавлено в ваш автопарк.")
            else:
                conn.close()
                messagebox.showwarning("Нет слотов", "Нет свободных слотов. Купите дополнительные.")

        global gruz_cars
        window = Toplevel(Win)
        window.geometry("500x400")
        window.title("Грузоперевозки")
        display_slots_ui(window, "my_gruz.db", "my_gruz")
        ttk.Button(window, text="Купить слот", command=buy_slot).pack(pady=5)
        canvas = Canvas(window)
        scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for item in gruz_cars:
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            frame.pack(pady=5, padx=5, fill=X)

            img = Image.open(item['image']).resize((170, 100))
            photo = ImageTk.PhotoImage(img)

            Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
            Label(frame, text=item["name"]).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Пробег: {item['probeg']}", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W)
            Label(frame, text=f"Доход в час: {item['dohod']}").grid(row=2, column=2, sticky=W)
            ttk.Button(frame, text='Купить',
                       command=lambda p=item["probeg"], d=item["dohod"], n=item["name"],img = item["image"]:
                       pay(n, p, d,img)).grid(row=0, column=3, rowspan=3)

            frame.image = photo  # сохранить ссылку
def prod():
        def check_shop_exists(name):
            db_name = f"mag_{name}.db"
            table = "mag_table"
            if not os.path.exists(db_name):
                return False
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (level INTEGER, income INTEGER)")
            exists = cursor.execute(f"SELECT * FROM {table}").fetchone() is not None
            conn.close()
            return exists

        global magazin_mal,magazin_sred,magazin_bol
        window = Toplevel(Win)
        window.geometry("500x500")
        window.title("Продажи")
        image1 = Image.open("icons/mal_mag.png")  # просто последняя картинка как "транспорт"
        image1 = image1.resize((100, 100))
        photo1 = ImageTk.PhotoImage(image1)
        image2 = Image.open("icons/sred_mag.png")  # просто последняя картинка как "транспорт"
        image2 = image2.resize((100, 100))
        photo2 = ImageTk.PhotoImage(image2)
        image3 = Image.open("icons/bol_mag.png")  # просто последняя картинка как "транспорт"
        image3 = image3.resize((100, 100))
        photo3 = ImageTk.PhotoImage(image3)

        names = ["mini", "medium", "big"]
        labels = ["Маленький магазин", "Средний магазин", "Большой магазин"]
        images = ["icons/mal_mag.png", "icons/sred_mag.png", "icons/bol_mag.png"]
        base_prices = [1000, 2500, 4000]
        base_incomes = [magazin_mal, magazin_sred, magazin_bol]

        for i in range(3):
            frame = Frame(window, bd=1, relief=SOLID, padx=10, pady=10)
            frame.pack(padx=10, pady=10, fill=X)

            img = Image.open(images[i]).resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            lbl_img = Label(frame, image=photo)
            lbl_img.image = photo
            lbl_img.grid(row=0, column=0, rowspan=3)

            Label(frame, text=labels[i], font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Базовый доход: ${base_incomes[i]}").grid(row=1, column=1, sticky=W)
            Label(frame, text=f"Базовая цена: ${base_prices[i]}").grid(row=2, column=1, sticky=W)

            label_text = "Посмотреть подробности" if check_shop_exists(names[i]) else "Открыть"
            ttk.Button(frame, text=label_text,
                   command=lambda n=names[i], p=base_prices[i], d=base_incomes[i]: otkr_magazin_info(n, p, d)
                   ).grid(row=0, column=2, rowspan=3)
def proiz():
        def check_proiz_exists(name):
            db_name = f"pro_{name}.db"
            table = "proiz_table"
            if not os.path.exists(db_name):
                return False
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (level INTEGER, income INTEGER)")
            exists = cursor.execute(f"SELECT * FROM {table}").fetchone() is not None
            conn.close()
            return exists

        global proi_mal,proi_sred,proi_bol
        window = Toplevel(Win)
        window.geometry("500x500")
        window.title("Продажи")
        image1 = Image.open("icons/mal_mag.png")  # просто последняя картинка как "транспорт"
        image1 = image1.resize((100, 100))
        photo1 = ImageTk.PhotoImage(image1)
        image2 = Image.open("icons/sred_mag.png")  # просто последняя картинка как "транспорт"
        image2 = image2.resize((100, 100))
        photo2 = ImageTk.PhotoImage(image2)
        image3 = Image.open("icons/bol_mag.png")  # просто последняя картинка как "транспорт"
        image3 = image3.resize((100, 100))
        photo3 = ImageTk.PhotoImage(image3)

        names = ["mini", "medium", "big"]
        labels = ["Маленькое производство", "Среднее производство", "Большое производствон"]
        images = ["icons/mal_pro.png", "icons/sred_pro.png", "icons/bol_pro.png"]
        base_prices = [3000, 6500, 14000]
        base_incomes = [magazin_mal, magazin_sred, magazin_bol]

        for i in range(3):
            frame = Frame(window, bd=1, relief=SOLID, padx=10, pady=10)
            frame.pack(padx=10, pady=10, fill=X)

            img = Image.open(images[i]).resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            lbl_img = Label(frame, image=photo)
            lbl_img.image = photo
            lbl_img.grid(row=0, column=0, rowspan=3)

            Label(frame, text=labels[i], font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=W)
            Label(frame, text=f"Базовый доход: ${base_incomes[i]}").grid(row=1, column=1, sticky=W)
            Label(frame, text=f"Базовая цена: ${base_prices[i]}").grid(row=2, column=1, sticky=W)

            label_text = "Посмотреть подробности" if check_proiz_exists(names[i]) else "Открыть"
            ttk.Button(frame, text=label_text,
                   command=lambda n=names[i], p=base_prices[i], d=base_incomes[i]: otkr_proiz_info(n, p, d)
                   ).grid(row=0, column=2, rowspan=3)
def bisunes():
    for widget in tab2.winfo_children():
        widget.destroy()

    businesses = get_all_businesses()

    # Создаем обернутый Scrollable Canvas
    canvas = Canvas(tab2)
    scrollbar = Scrollbar(tab2, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)
    total_income = (
            calculate_shop_income() +
            calculate_factory_income() +
            calculate_vehicle_income() +
            sum(item['price'] // 100 for item in my_nedvi)
    )

    Label(scrollable_frame, text=f"Общий доход в час: $ {total_income}", font=("Arial", 12, "bold")).pack(pady=10)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    if not businesses:
        Label(scrollable_frame, text="У вас нет бизнесов", font=("Arial", 16, "bold")).pack(pady=20)
    else:
        Label(scrollable_frame, text="Ваши бизнесы", font=("Arial", 14, "bold")).pack(pady=5)

        for biz in businesses:
            frame = Frame(scrollable_frame, relief=SOLID, bd=1, padx=5, pady=5)
            frame.pack(fill=X, padx=10, pady=5)

            Label(frame, text=f"{biz['type']}: {biz['name']}", font=("Arial", 12, "bold")).pack(anchor=W)

            if biz['type'] == "Таксопарк":
                ttk.Button(frame, text="Купить машину", command=taxi).pack(side=LEFT, padx=5)
                ttk.Button(frame, text="Купить слот", command=lambda: buy_slot_logic("taxi")).pack(side=LEFT, padx=5)
            elif biz['type'] == "Строительство":
                ttk.Button(frame, text="Строить", command=lambda n=biz['name']: open_building_window(n)).pack(side=LEFT, padx=5)
                ttk.Button(frame, text="Управлять", command=lambda n=biz['name']: open_building_window(n)).pack(side=LEFT, padx=5)
            elif biz['type'] == "Грузоперевозки":
                ttk.Button(frame, text="Купить машину", command=gruz).pack(side=LEFT, padx=5)
                ttk.Button(frame, text="Купить слот", command=lambda: buy_slot_logic("gruz")).pack(side=LEFT, padx=5)
            elif biz['type'] == "Магазин":
                ttk.Button(frame, text="Улучшить", command=lambda n=biz['name']: upgrade_shop(n)).pack(side=LEFT, padx=5)
            elif biz['type'] == "IT-компания":
                ttk.Button(frame, text="Проекты", command=lambda n=biz['name']: open_it_company_window(n)).pack(side=LEFT, padx=5)
            elif biz['type'] == "Производство":
                ttk.Button(frame, text="Улучшить", command=lambda n=biz['name']: upgrade_factory(n)).pack(side=LEFT, padx=5)

            ttk.Button(frame, text="Удалить бизнес", command=lambda n=biz['name'], t=biz['type']: delete_business(n, t)).pack(side=RIGHT, padx=5)

    def open_business_window():
        if len(get_all_businesses()) >= 10:
            messagebox.showwarning("Ограничение", "Нельзя иметь больше 10 бизнесов")
            return

        window = Toplevel(Win)
        window.geometry("300x300")
        window.title("Открыть бизнес")

        def create_biz_window(biz_type):
            def submit():
                biz_name = entry.get().strip()
                if not biz_name:
                    messagebox.showwarning("Ошибка", "Введите имя бизнеса")
                    return
                create_business(biz_name, biz_type)
                messagebox.showinfo("Успешно", f"{biz_type} '{biz_name}' открыт!")
                window.destroy()
                bisunes()

            for widget in window.winfo_children():
                widget.destroy()
            Label(window, text=f"Введите имя для бизнеса ({biz_type}):").pack(pady=10)
            entry = Entry(window)
            entry.pack(pady=5)
            ttk.Button(window, text="Открыть", command=submit).pack(pady=10)

        ttk.Button(window, text="Таксопарк", command=lambda: create_biz_window("Таксопарк")).pack(fill=X, padx=10, pady=5)
        ttk.Button(window, text="Грузоперевозки", command=lambda: create_biz_window("Грузоперевозки")).pack(fill=X, padx=10, pady=5)
        ttk.Button(window, text="Магазин", command=lambda: create_biz_window("Магазин")).pack(fill=X, padx=10, pady=5)
        ttk.Button(window, text="Производство", command=lambda: create_biz_window("Производство")).pack(fill=X, padx=10, pady=5)
        ttk.Button(window, text="Строительство", command=lambda: create_biz_window("Строительство")).pack(fill=X, padx=10, pady=5)
        ttk.Button(window, text="IT-компания", command=lambda: create_biz_window("IT-компания")).pack(fill=X, padx=10, pady=5)

    ttk.Button(scrollable_frame, text="Открыть бизнес", command=open_business_window).pack(pady=15)
def open_building_window(biz_name):
    def load_projects():
        conn = sqlite3.connect("build.db")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM build_orders WHERE built=0").fetchall()
        conn.close()
        return rows

    def open_project_window(order):
        def buy_resource(resource, amount, price_per_unit):
            global  balance
            total = amount * price_per_unit
            if balance >= total:
                balance -= total
                owned[resource] += amount
                save_balance()
                update_ui()
            else:
                messagebox.showwarning("Недостаточно средств", "Пополните баланс")

        def build():
            if (owned["iron"] >= order["iron_needed"] and
                owned["concrete"] >= order["concrete_needed"] and
                owned["wood"] >= order["wood_needed"]):
                conn = sqlite3.connect("build.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE build_orders SET built=1 WHERE id=?", (order["id"],))
                conn.commit()
                conn.close()
                global balance
                balance += order["reward"]
                save_balance()
                messagebox.showinfo("Построено", f"Вы заработали ${order['reward']}!")
                win.destroy()
            else:
                messagebox.showwarning("Не хватает ресурсов", "Закупите всё необходимое")

        owned = {"iron": 0, "concrete": 0, "wood": 0}
        win = Toplevel(Win)
        win.geometry("400x400")
        win.title(f"Стройка: {order['name']}")

        def update_ui():
            label_status.config(
                text=f"Железо: {owned['iron']}/{order['iron_needed']}\n"
                     f"Бетон: {owned['concrete']}/{order['concrete_needed']}\n"
                     f"Дерево: {owned['wood']}/{order['wood_needed']}"
            )
            label_balance.config(text=f"Баланс: ${balance}")

        label_balance = Label(win, text="")
        label_balance.pack()
        label_status = Label(win, text="", font=("Arial", 12))
        label_status.pack()

        for res, cost in [("iron", 100), ("concrete", 50), ("wood", 30)]:
            Button(win, text=f"Купить 10 {res} (${cost*10})",
                   command=lambda r=res, c=cost: buy_resource(r, 10, c)).pack()

        Button(win, text="Построить", command=build).pack(pady=10)
        update_ui()

    # Главное окно выбора
    projects = load_projects()
    if not projects:
        messagebox.showinfo("Нет проектов", "Все здания построены.")
        return

    w = Toplevel(Win)
    w.geometry("400x400")
    w.title("Доступные стройки")

    Label(w, text="Выберите проект:", font=("Arial", 14, "bold")).pack(pady=5)

    shown_names = set()

    for row in projects:
        name = row[1]
        if name in shown_names:
            continue
        shown_names.add(name)

        order = {
            "id": row[0],
            "name": row[1],
            "reward": row[2],
            "iron_needed": row[3],
            "concrete_needed": row[4],
            "wood_needed": row[5]
        }

        Button(w, text=f"{order['name']} — ${order['reward']}", width=30,
               command=lambda o=order: (w.destroy(), open_project_window(o))).pack(pady=3)
def show_nft_market():
    import os
    global my_nfts, balance
    nfts = [
        {"name": "CryptoCat", "price": 5000, "income": 100, "image": "icons/nft_cat.jpg"},
        {"name": "GoldenBanana", "price": 8000, "income": 150, "image": "icons/nft_banana.jpg"},
        {"name": "MetaRocket", "price": 12000, "income": 250, "image": "icons/nft_rocket.jpg"}
    ]

    def buy(nft):
        global balance
        if balance >= nft["price"]:
            save_my_nfts()
            check_badges()
            save_badges()
            balance -= nft["price"]
            my_nfts.append(nft)
            save_balance()
            messagebox.showinfo("Покупка", f"Вы купили NFT: {nft['name']}")
        else:
            messagebox.showwarning("Ошибка", "Недостаточно средств")

    w = Toplevel(Win)
    w.geometry("500x400")
    w.title("Рынок NFT")

    canvas = Canvas(w)
    scrollbar = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    for item in nfts:
        frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
        frame.pack(pady=5, padx=5, fill=X)

        img = Image.open(item["image"]).resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        Label(frame, image=photo).grid(row=0, column=0, rowspan=3)
        Label(frame, text=f"{item['name']} - ${item['price']}\nДоход: ${item['income']}/час").grid(row=0, column=1, sticky=W)
        Button(frame, text="Купить", command=lambda i=item: buy(i)).grid(row=1, column=1)
        frame.image = photo
def open_it_company_window(biz_name):
    def load_projects():
        conn = sqlite3.connect("it_projects.db")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM projects WHERE done=0").fetchall()
        conn.close()
        return rows

    def open_project_window(project):
        global hired_staff

        def hire(role, count):
            cost = salary[role] * count
            global balance
            if balance >= cost:
                balance -= cost
                hired_staff[role] += count
                save_balance()
                update_ui()
            else:
                messagebox.showwarning("Ошибка", "Недостаточно средств")

        def finish_project():
            reqs = {
                "devs": project["devs_needed"],
                "testers": project["testers_needed"],
                "designers": project["designers_needed"],
                "leads": project["leads_needed"]
            }
            for role, needed in reqs.items():
                if hired_staff[role] < needed:
                    messagebox.showwarning("Ошибка", f"Не хватает: {role}")
                    return
            # успех
            conn = sqlite3.connect("it_projects.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE projects SET done=1 WHERE id=?", (project["id"],))
            conn.commit()
            conn.close()

            global balance
            balance += project["reward"]
            save_balance()
            messagebox.showinfo("Успех", f"Проект завершен! Вы получили ${project['reward']}")
            win.destroy()

        win = Toplevel(Win)
        win.geometry("400x400")
        win.title(f"Проект: {project['name']}")

        def update_ui():
            status.config(text=
                f"Dev: {hired_staff['devs']}/{project['devs_needed']}\n"
                f"Tester: {hired_staff['testers']}/{project['testers_needed']}\n"
                f"Designer: {hired_staff['designers']}/{project['designers_needed']}\n"
                f"Lead: {hired_staff['leads']}/{project['leads_needed']}\n"
                f"Баланс: ${balance}")

        status = Label(win, text="", font=("Arial", 12))
        status.pack()

        for role in ["devs", "testers", "designers", "leads"]:
            Button(win, text=f"Нанять 1 {role} (${salary[role]})", command=lambda r=role: hire(r, 1)).pack(pady=2)

        Button(win, text="Завершить проект", command=finish_project).pack(pady=10)
        update_ui()

    # Главное окно выбора проекта
    projects = load_projects()
    if not projects:
        messagebox.showinfo("Нет проектов", "Все проекты завершены.")
        return

    w = Toplevel(Win)
    w.geometry("400x400")
    w.title("Доступные проекты")

    Label(w, text="Выберите проект:", font=("Arial", 14)).pack(pady=5)
    shown_names = set()

    for row in projects:
        name = row[1]
        if name in shown_names:
            continue
        shown_names.add(name)

        project = {
            "id": row[0],
            "name": row[1],
            "reward": row[2],
            "devs_needed": row[3],
            "testers_needed": row[4],
            "designers_needed": row[5],
            "leads_needed": row[6]
        }

        Button(w, text=f"{project['name']} — ${project['reward']}",
               command=lambda p=project: (w.destroy(), open_project_window(p))).pack(pady=2)
def crypto_market_window():
    def update_crypto_prices():
        for coin in crypto_market.values():
            change = random.uniform(-0.05, 0.05)
            coin["price"] *= (1 + change)
            coin["price"] = round(coin["price"], 2)
        if Win.winfo_exists():
            Win.after(5000, update_crypto_prices)

    win = Toplevel()
    win.geometry("800x600")
    win.title("Крипторынок")

    canvas = Canvas(win)
    scrollbar = Scrollbar(win, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    def buy_crypto(name, price):
        global balance
        if balance >= price:
            my_crypto.append({"name": name, "buy_price": price, "amount": 1})
            balance -= price
            save_crypto_data()
            save_balance()
            refresh()

    def sell_crypto(index):
        global balance
        if 0 <= index < len(my_crypto):
            coin = my_crypto.pop(index)
            price_now = crypto_market[coin["name"]]["price"]
            balance += price_now
            save_crypto_data()
            save_balance()
            refresh()

    def refresh():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        Label(scrollable_frame, text="Рынок", font=("Arial", 14, "bold")).pack()
        for name, data in crypto_market.items():
            frame = Frame(scrollable_frame, bd=1, relief=SOLID, padx=10, pady=10)
            frame.pack(fill=X, padx=10, pady=5)

            try:
                img = Image.open(data["image"]).resize((40, 40))
                photo = ImageTk.PhotoImage(img)
                Label(frame, image=photo).pack(side=LEFT)
                frame.image = photo
            except:
                Label(frame, text="[img]").pack(side=LEFT)

            Label(frame, text=f"{name}: ${data['price']:.2f}", font=("Arial", 12)).pack(side=LEFT, padx=10)
            Button(frame, text="Купить", command=lambda n=name, p=data["price"]: buy_crypto(n, p)).pack(side=RIGHT)

        Label(scrollable_frame, text="Портфель", font=("Arial", 14, "bold")).pack(pady=10)

        total_value = 0
        for i, coin in enumerate(my_crypto):
            curr_price = crypto_market[coin["name"]]["price"]
            profit = round(curr_price - coin["buy_price"], 2)
            total_value += curr_price

            info = f"{coin['name']} | Куплено за ${coin['buy_price']} | Сейчас: ${curr_price:.2f} | {'+' if profit > 0 else ''}{profit:.2f}"
            f2 = Frame(scrollable_frame, bd=1, relief=SOLID, padx=5, pady=5)
            f2.pack(fill=X, padx=10, pady=3)
            Label(f2, text=info).pack(side=LEFT)
            Button(f2, text="Продать", command=lambda idx=i: sell_crypto(idx)).pack(side=RIGHT)

        Label(scrollable_frame, text=f"Общая стоимость портфеля: ${total_value:.2f}", font=("Arial", 10)).pack(pady=5)
        win.after(5000, refresh)

    refresh()
def show_all_badges():
    badge_list = [
        {"name": "NFT коллекционер", "desc": "Купите 3 NFT"},
        {"name": "Бизнесмен", "desc": "Откройте 5 бизнесов"},
        {"name": "Криптобарон", "desc": "Вложите $100000 в крипту"}
    ]

    w = Toplevel(Win)
    w.geometry("400x400")
    w.title("Знаки отличия")

    Label(w, text="Все знаки отличия", font=("Arial", 14, "bold")).pack(pady=10)

    for b in badge_list:
        owned = "✅" if b["name"] in my_badges else "❌"
        Label(w, text=f"{owned} {b['name']}: {b['desc']}", anchor="w").pack(fill=X, padx=10, pady=2)
#-------------------------------
def func_per_click():
    with open("settings/per_click.cfg","r") as f:
        return int(f.read())
def func_level():
    with open("settings/level.cfg","r") as f:
        return int(f.read())
def func_update_cost():
    with open("settings/update_cost.cfg", "r") as f:
        return int(f.read())
def func_click_balance():
    try:
        with open("settings/click_balance.cfg", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
def write_per_click(p):
    with open("settings/per_click.cfg","w") as f:
        f.write(str(p))
def write_level(level):
    with open("settings/level.cfg","w") as f:
        f.write(str(level))
def write_update_cost(u):
    with open("settings/update_cost.cfg", "w") as f:
        f.write(str(u))
def write_click_balance(cb):
    with open("settings/click_balance.cfg", "w") as f:
        f.write(str(cb))
#-------------------------------
def otkr_magazin_info(name, base_price, base_income):
    w = Toplevel(Win)
    w.geometry("400x300")
    w.title(f"{name} — Магазин")

    db_name = f"mag_{name}.db"
    table = "mag_table"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            level INTEGER,
            income INTEGER
        )
    """)
    conn.commit()
    data = cursor.execute(f"SELECT * FROM {table}").fetchone()

    if data is None:
        level = 1
        income = base_income
        cursor.execute(f"INSERT INTO {table} VALUES (?, ?)", (level, income))
        conn.commit()
    else:
        level, income = data

    def upgrade():
        nonlocal level, income
        cost = int(base_price * (1.2 ** level))
        global balance
        if balance >= cost:
            balance -= cost
            level += 1
            income = int(income * 1.2)

            # открой соединение и обнови
            conn2 = sqlite3.connect(db_name)
            cursor2 = conn2.cursor()
            cursor2.execute(f"UPDATE {table} SET level=?, income=?", (level, income))
            conn2.commit()
            conn2.close()

            update_ui()
            save_balance()
            messagebox.showinfo("Успешно", f"Магазин улучшен до уровня {level}")
        else:
            messagebox.showwarning("Ошибка", "Недостаточно средств")

    def update_ui():
        label_lvl.config(text=f"Уровень: {level}")
        label_inc.config(text=f"Доход: ${income}/час")
        label_cost.config(text=f"Улучшение за: ${int(base_price * (1.2 ** level))}")

    label_lvl = Label(w, text="", font=("Arial", 14))
    label_lvl.pack()
    label_inc = Label(w, text="", font=("Arial", 14))
    label_inc.pack()
    label_cost = Label(w, text="", font=("Arial", 12))
    label_cost.pack()
    Button(w, text="Улучшить", command=upgrade).pack(pady=10)

    update_ui()
    conn.close()
def otkr_proiz_info(name, base_price, base_income):
    w = Toplevel(Win)
    w.geometry("400x300")
    w.title(f"{name} — Производство")

    db_name = f"pro_{name}.db"
    table = "proiz_table"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            level INTEGER,
            income INTEGER
        )
    """)
    conn.commit()
    data = cursor.execute(f"SELECT * FROM {table}").fetchone()

    if data is None:
        level = 1
        income = base_income
        cursor.execute(f"INSERT INTO {table} VALUES (?, ?)", (level, income))
        conn.commit()
    else:
        level, income = data

    def upgrade():
        nonlocal level, income
        cost = int(base_price * (1.2 ** level))
        global balance
        if balance >= cost:
            balance -= cost
            level += 1
            income = int(income * 1.2)

            # открой соединение и обнови
            conn2 = sqlite3.connect(db_name)
            cursor2 = conn2.cursor()
            cursor2.execute(f"UPDATE {table} SET level=?, income=?", (level, income))
            conn2.commit()
            conn2.close()

            update_ui()
            save_balance()
            messagebox.showinfo("Успешно", f"Магазин улучшен до уровня {level}")
        else:
            messagebox.showwarning("Ошибка", "Недостаточно средств")

    def update_ui():
        label_lvl.config(text=f"Уровень: {level}")
        label_inc.config(text=f"Доход: ${income}/час")
        label_cost.config(text=f"Улучшение за: ${int(base_price * (1.2 ** level))}")

    label_lvl = Label(w, text="", font=("Arial", 14))
    label_lvl.pack()
    label_inc = Label(w, text="", font=("Arial", 14))
    label_inc.pack()
    label_cost = Label(w, text="", font=("Arial", 12))
    label_cost.pack()
    Button(w, text="Улучшить", command=upgrade).pack(pady=10)

    update_ui()
    conn.close()
def update_profile_tab():
    global balance, my_nedvi, dohod_nedv
    for widget in tab5.winfo_children():
        widget.destroy()
    Button(tab5, text="Все знаки отличия", command=show_all_badges).pack()
    Label(tab5, text="Профиль", font=("Arial", 18, "bold")).pack()

    # Общий доход в час
    dohod_nedv = sum([item.get("price", 0) // 100 for item in my_nedvi])  # доход = цена / 100 для примера

    # Общая стоимость недвижимости
    total_real_estate = sum([item["price"] for item in my_nedvi])

    total_fortune = balance + total_real_estate

    Label(tab5, text=f"Общее состояние: $ {total_fortune}", font=("Arial", 14)).pack()
    Label(tab5, text=f"Доход от недвижимости в час: $ {dohod_nedv}", font=("Arial", 12)).pack()
    Label(tab5, text=f"Баланс: $ {balance}", font=("Arial", 12)).pack()
    Label(tab5, text=f"Объектов недвижимости: {len(my_nedvi)}", font=("Arial", 12)).pack()

    # Отображение транспорта (если есть)
    Label(tab5, text="Основной транспорт:").pack()
    try:
        image = Image.open(my_nedvi[-1]['image'])  # просто последняя картинка как "транспорт"
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        Label(tab5, image=photo).pack()
        tab5.image = photo
    except Exception as e:
        Label(tab5, text="Нет транспорта").pack()
def update_vehicle_income_and_wear():
    now = datetime.now()
    last_exit = load_last_exit_time()
    if not last_exit:
        return

    hours_passed = (now - last_exit).total_seconds() // 3600
    if hours_passed <= 0:
        return

    global balance

    for table in ['my_taxi.db', 'my_gruz.db']:
        conn = sqlite3.connect(table)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT rowid, name, probeg, dohod, image FROM {}".format(table.split('.')[0])).fetchall()

        for row in rows:
            rowid, name, probeg, dohod, image = row
            used = int(hours_passed * 100)
            new_probeg = probeg - used
            if new_probeg <= 0:
                cursor.execute("DELETE FROM {} WHERE rowid=?".format(table.split('.')[0]), (rowid,))
            else:
                cursor.execute("UPDATE {} SET probeg=? WHERE rowid=?".format(table.split('.')[0]), (new_probeg, rowid))
                balance += dohod * hours_passed

        conn.commit()
        conn.close()
    save_balance()
def display_slots_ui(parent, db, table):
    frame_slots = Frame(parent)
    frame_slots.pack()

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, probeg INTEGER, dohod INTEGER, image TEXT)")
    rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()

    total = max_slots + extra_slots
    for i in range(total):
        frame = Frame(frame_slots, width=110, height=100, relief=SOLID, bd=1)
        frame.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        if i < len(rows):
            img_path = rows[i][3]
            img = Image.open(img_path).resize((100, 60))
            photo = ImageTk.PhotoImage(img)
            lbl = Label(frame, image=photo)
            lbl.image = photo
            lbl.pack()
            Label(frame, text=f"{rows[i][0]}\n{rows[i][1]} км").pack()
        else:
            Label(frame, text="Свободно").pack()
def calculate_shop_income():
    total_income = 0
    for name in ["mini", "medium", "big"]:
        db_name = f"mag_{name}.db"
        table = "mag_table"
        if not os.path.exists(db_name):
            continue
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (level INTEGER, income INTEGER)")
        row = cursor.execute(f"SELECT income FROM {table}").fetchone()
        if row:
            total_income += row[0]
        conn.close()
    return total_income
def calculate_factory_income():
    total_income = 0
    for name in ["mini", "medium", "big"]:
        db_name = f"pro_{name}.db"
        table = "proiz_table"
        if not os.path.exists(db_name):
            continue
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (level INTEGER, income INTEGER)")
        row = cursor.execute(f"SELECT income FROM {table}").fetchone()
        if row:
            total_income += row[0]
        conn.close()
    return total_income
def calculate_vehicle_income():
    total = 0
    for db_name, table in [("my_taxi.db", "my_taxi"), ("my_gruz.db", "my_gruz")]:
        if not os.path.exists(db_name):
            continue
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, probeg INTEGER, dohod INTEGER, image TEXT)")
        rows = cursor.execute(f"SELECT dohod FROM {table}").fetchall()
        total += sum([row[0] for row in rows])
        conn.close()
    return total
def show_profile_window():
    # === Расчёт общего состояния ===
    total_value = balance
    for coin in my_crypto:
        curr_price = crypto_market[coin["name"]]["price"]
        total_value += curr_price
    for obj_list in [my_nedvi, my_planes, my_yahts, my_cars, my_coins]:
        for item in obj_list:
            try:
                total_value += int(item.get('price', 0))
            except:
                pass

    # === Frame 1 – Панель игрока ===
    frame1 = Frame(tab5, bd=2, relief=SOLID, padx=10, pady=10)
    frame1.pack(side=RIGHT, fill=Y, padx=5)
    Label(frame1, text="Ваши NFT", font=("Arial", 12, "bold")).pack()
    load_badges()
    load_my_nfts()
    for nft in my_nfts:
        Label(frame1, text=f"{nft['name']} | Доход: ${nft['income']}/час").pack()

    for badge in my_badges:
        Label(frame1, text=f"🏅 {badge}").pack()

    Label(frame1, text="Панель игрока", font=("Arial", 12, "bold")).pack()
    stats = [
        f"Деньги: ${balance}",
        f"Кликер: {func_click_balance()} / {func_update_cost()}",
        f"Магазин: {calculate_shop_income()} / час",
        f"Производство: {calculate_factory_income()} / час",
        f"Транспорт: {calculate_vehicle_income()} / час"
    ]
    for stat in stats:
        Label(frame1, text=stat, anchor="w").pack(fill=X)

    # === Frame 2 – Центр (Имущество) ===
    frame2 = Frame(tab5, bd=2, relief=SOLID, padx=10, pady=10)
    frame2.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

    Label(frame2, text="На аккаунте", font=("Arial", 12, "bold")).pack()
    for item in my_nedvi[:3]:  # Покажем первые 3 объекта
        try:
            img = Image.open(item['image']).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            lbl = Label(frame2, image=photo)
            lbl.image = photo
            lbl.pack(pady=5,side = LEFT)
        except:
            Label(frame2, text="[Недвижимость]").pack(pady=5)

    # === Frame 3 – Левая панель (Состояние) ===
    frame3 = Frame(tab5, bd=2, relief=SOLID, padx=10, pady=10)
    frame3.pack(side=LEFT, fill=Y, padx=5)

    Label(frame3, text=f"Общее состояние: ${total_value}", font=("Arial", 10, "bold")).pack(pady=5)

    def show_asset(label, items):
        if items:
            try:
                img = Image.open(items[0]['image']).resize((80, 80))
                photo = ImageTk.PhotoImage(img)
                lbl = Label(frame3, image=photo, text=label, compound=BOTTOM)
                lbl.image = photo
                lbl.pack(pady=5)
            except:
                Label(frame3, text=f"[{label}]").pack(pady=5)
        else:
            Label(frame3, text=f"[{label}] (0)").pack(pady=5)

    show_asset("Недвижка", my_nedvi)
    show_asset("Самолёты", my_planes)
    show_asset("Яхты", my_yahts)
    show_asset("Машины", my_cars)
    show_asset("Монеты", my_coins)
def on_closing():
    save_exit_time()
    save_my_nfts()
    save_crypto_data()
    save_badges()
    Win.destroy()
def check_badges():
    global my_nfts, my_crypto, my_badges

    # Знак: NFT коллекционер
    if len(my_nfts) >= 3 and "NFT коллекционер" not in my_badges:
        my_badges.append("NFT коллекционер")

    # Знак: Криптобарон — вложено более $100,000 в крипту
    crypto_total = 0
    for coin in my_crypto:
        coin_name = coin["name"]
        amount = coin["amount"]
        price = crypto_market.get(coin_name, {}).get("price", 0)
        crypto_total += amount * price

    if crypto_total >= 100000 and "Криптобарон" not in my_badges:
        my_badges.append("Криптобарон")

    # Знак: Бизнесмен — если открыто более 5 бизнесов
    businesses = get_all_businesses()
    if len(businesses) >= 5 and "Бизнесмен" not in my_badges:
        my_badges.append("Бизнесмен")

    # Знак: Добро пожаловать — даём один раз
    if "Добро пожаловать" not in my_badges:
        my_badges.append("Добро пожаловать")



Win = Tk()
Win.title()
Win.geometry('760x600')
Win.state('zoomed')
notebook = ttk.Notebook(Win)
notebook.pack(fill='both', expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)

notebook.add(tab1, text='Инвестиции')
notebook.add(tab2, text='Бизнес')
notebook.add(tab3, text='Заработок')
notebook.add(tab4, text='Предметы')
notebook.add(tab5, text='Профиль')

update_profile_tab()
load_balance()
zarabotok()
invest()
predm()
bisunes()
show_profile_window()
update_crypto_prices()


add_offline_income()
update_vehicle_income_and_wear()
load_slots()
create_build_orders_table()
seed_build_projects()
create_it_projects_table()
seed_it_projects()
load_crypto_data()
load_badges()
check_badges()
load_my_nfts()


Win.protocol("WM_DELETE_WINDOW",on_closing)
Win.mainloop()







