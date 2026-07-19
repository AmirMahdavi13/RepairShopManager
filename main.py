import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "repairs.json"


def load_repairs():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_repairs(repairs):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(repairs, file, ensure_ascii=False, indent=4)


def get_next_id(repairs):
    if not repairs:
        return 400288

    return max(repair["id"] for repair in repairs) + 1


def print_repair(repair):
    print("\n" + "=" * 50)
    print(f"شماره پذیرش : {repair['id']}")
    print(f"نام مشتری   : {repair['customer_name']}")
    print(f"شماره تماس  : {repair['phone']}")
    print(f"نوع دستگاه  : {repair['device_type']}")
    print(f"برند         : {repair['brand']}")
    print(f"شرح خرابی    : {repair['problem']}")
    print(f"بیعانه       : {repair['deposit']:,} تومان")
    print(f"وضعیت        : {repair['status']}")
    print("=" * 50)


def add_repair(repairs):
    print("\n===== ثبت تعمیر جدید =====")

    customer_name = input("نام مشتری: ")
    phone = input("شماره تماس: ")
    device_type = input("نوع دستگاه: ")
    brand = input("برند: ")
    problem = input("شرح خرابی: ")

    while True:
        try:
            deposit = int(input("بیعانه (فقط عدد): "))
            break
        except ValueError:
            print("❌ فقط عدد وارد کن.")

    repair = {
        "id": get_next_id(repairs),
        "customer_name": customer_name,
        "phone": phone,
        "device_type": device_type,
        "brand": brand,
        "problem": problem,
        "deposit": deposit,
        "status": "در انتظار تعمیر"
    }

    repairs.append(repair)
    save_repairs(repairs)

    print(f"\n✅ تعمیر با شماره {repair['id']} ثبت شد.")


def show_repairs(repairs):
    print("\n===== نمایش تعمیرات =====")

    print("1. در انتظار تعمیر")
    print("2. در حال تعمیر")
    print("3. آماده تحویل")
    print("4. تحویل داده شد")
    print("5. همه تعمیرات")

    choice = input("\nانتخاب: ")

    status_map = {
        "1": "در انتظار تعمیر",
        "2": "در حال تعمیر",
        "3": "آماده تحویل",
        "4": "تحویل داده شد"
    }

    found = False

    if choice == "5":
        for repair in repairs:
            print_repair(repair)
            found = True

    elif choice in status_map:
        selected_status = status_map[choice]

        for repair in repairs:
            if repair["status"] == selected_status:
                print_repair(repair)
                found = True

    else:
        print("❌ گزینه نامعتبر است.")
        return

    if not found:
        print("❌ موردی پیدا نشد.")


def search_repair(repairs):
    print("\n===== جستجو =====")
    print("1. نام مشتری")
    print("2. شماره پذیرش")
    print("3. شماره تلفن")

    choice = input("\nانتخاب: ")

    if choice == "1":
        name = input("نام مشتری: ").strip().lower()

        found = False

        for repair in repairs:
            if name in repair["customer_name"].lower():
                print_repair(repair)
                found = True

        if not found:
            print("❌ موردی پیدا نشد.")

    elif choice == "2":
        try:
            repair_id = int(input("شماره پذیرش: "))
        except ValueError:
            print("❌ شماره نامعتبر است.")
            return

        for repair in repairs:
            if repair["id"] == repair_id:
                print_repair(repair)
                return

        print("❌ تعمیری با این شماره پیدا نشد.")

    elif choice == "3":
        phone = input("شماره تلفن: ").strip()

        found = False

        for repair in repairs:
            if phone in repair["phone"]:
                print_repair(repair)
                found = True

        if not found:
            print("❌ موردی پیدا نشد.")

    else:
        print("❌ گزینه نامعتبر است.")


def update_status(repairs):
    print("\n===== تغییر وضعیت تعمیر =====")

    try:
        repair_id = int(input("شماره پذیرش: "))
    except ValueError:
        print("❌ شماره نامعتبر است.")
        return

    selected_repair = None

    for repair in repairs:
        if repair["id"] == repair_id:
            selected_repair = repair
            break

    if selected_repair is None:
        print("❌ تعمیری با این شماره پیدا نشد.")
        return

    print(f"\nوضعیت فعلی: {selected_repair['status']}")

    statuses = [
        "در انتظار تعمیر",
        "در حال تعمیر",
        "آماده تحویل",
        "تحویل داده شد"
    ]

    print("\nوضعیت جدید:")

    for i, status in enumerate(statuses, start=1):
        print(f"{i}. {status}")

    try:
        choice = int(input("\nانتخاب: "))
    except ValueError:
        print("❌ انتخاب نامعتبر است.")
        return

    if choice < 1 or choice > len(statuses):
        print("❌ انتخاب نامعتبر است.")
        return

    selected_repair["status"] = statuses[choice - 1]

    save_repairs(repairs)

    print("\n✅ وضعیت با موفقیت تغییر کرد.")

def dashboard(repairs):
    total = len(repairs)

    waiting = sum(1 for r in repairs if r["status"] == "در انتظار تعمیر")
    repairing = sum(1 for r in repairs if r["status"] == "در حال تعمیر")
    ready = sum(1 for r in repairs if r["status"] == "آماده تحویل")
    delivered = sum(1 for r in repairs if r["status"] == "تحویل داده شد")

    total_deposit = sum(r["deposit"] for r in repairs)

    print("\n" + "=" * 50)
    print("📊 داشبورد تعمیرگاه")
    print("=" * 50)

    print(f"\n📦 کل تعمیرات: {total}")

    print(f"\n🟡 در انتظار تعمیر : {waiting}")
    print(f"🔵 در حال تعمیر    : {repairing}")
    print(f"🟢 آماده تحویل     : {ready}")
    print(f"⚫ تحویل داده شده  : {delivered}")

    print(f"\n💰 مجموع بیعانه‌ها: {total_deposit:,} تومان")

    if repairs:
        print(f"🏷 آخرین شماره پذیرش: {max(r['id'] for r in repairs)}")

    print("\n📋 دستگاه‌های آماده تحویل:")

    found_ready = False

    for repair in repairs:
        if repair["status"] == "آماده تحویل":
            print(f"{repair['id']} - {repair['customer_name']} - {repair['device_type']}")
            found_ready = True

    if not found_ready:
        print("موردی وجود ندارد.")

    print("=" * 50)

def main():
    repairs = load_repairs()

    while True:
        print("\n===== Repair Shop Manager =====")
        print("1. ثبت تعمیر جدید")
        print("2. نمایش تعمیرات")
        print("3. جستجو")
        print("4. تغییر وضعیت تعمیر")
        print("5. داشبورد")
        print("6. خروچ")

        choice = input("\nانتخاب: ")

        if choice == "1":
            add_repair(repairs)

        elif choice == "2":
            show_repairs(repairs)

        elif choice == "3":
            search_repair(repairs)

        elif choice == "4":
            update_status(repairs)

        elif choice == "5":
            dashboard(repairs)
        
        elif choice == "6":
            print("\nخروج از برنامه...")
            break

        else:
            print("❌ گزینه نامعتبر است.")


if __name__ == "__main__":
    main()