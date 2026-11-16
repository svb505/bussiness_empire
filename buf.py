balance = 500000
def save_balance():
    global balance
    with open("settings/balance.bin", "wb") as f:
        f.write(balance.to_bytes(4, byteorder='little', signed=True))
save_balance()


def get_all_businesses():
        biz_list = []
        for name in ["mini", "medium", "big"]:
            if os.path.exists(f"mag_{name}.db"):
                biz_list.append(f"Магазин: {name}")
            if os.path.exists(f"pro_{name}.db"):
                biz_list.append(f"Производство: {name}")
        return biz_list
def bisunes():
    for widget in tab2.winfo_children():
        widget.destroy()

    businesses = get_all_businesses()

    if not businesses:
        Label(tab2, text="У вас нету бизнесов", font=("Arial", 16, "bold")).pack(pady=20)
    else:
        Label(tab2, text="Ваши бизнесы", font=("Arial", 14, "bold")).pack()
        for b in businesses:
            Label(tab2, text=b).pack()

    def open_business_window():
        if len(get_all_businesses()) >= 10:
            messagebox.showwarning("Ограничение", "Нельзя иметь больше 10 бизнесов")
            return
        window = Toplevel(Win)
        window.geometry("300x400")
        window.title("Открыть бизнес")

        Button(window, text="Таксопарк", command=taxi).pack(fill=X, padx=10, pady=5)
        Button(window, text="Грузоперевозки", command=gruz).pack(fill=X, padx=10, pady=5)
        Button(window, text="Магазин", command=prod).pack(fill=X, padx=10, pady=5)
        Button(window, text="Производство", command=proiz).pack(fill=X, padx=10, pady=5)

    Button(tab2, text="Открыть бизнес", command=open_business_window).pack(pady=15)


