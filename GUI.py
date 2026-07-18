import customtkinter as ctk
import json
from pathlib import Path
from tkinter import messagebox
import arabic_reshaper
from bidi.algorithm import get_display

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "repairs.json"

def fa(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class RepairShopGUI:
    
    def __init__(self):

        self.app = ctk.CTk()
        self.app.title("Repair Shop Manager")
        self.app.geometry("1000x600")

        self.create_layout()

        self.app.mainloop()

    def load_repairs(self):

        if not DATA_FILE.exists():
            return []

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []

    def save_repairs(self, repairs):

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                repairs,
                file,
                ensure_ascii=False,
                indent=4
            )

    def get_next_id(self, repairs):

        if not repairs:
            return 400288

        return max(repair["id"] for repair in repairs) + 1

    def create_layout(self):

        self.sidebar = ctk.CTkFrame(
            self.app,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        self.content = ctk.CTkFrame(self.app)

        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text=fa("Repair Shop Manager"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        buttons = [
            ("ثبت تعمیر", self.show_add_repair),
            ("نمایش تعمیرات", self.show_repairs),
            ("جستجو", self.show_search),
            ("تغییر وضعیت", self.show_update_status),
            ("ویرایش تعمیر", self.show_edit_repair),
            ("داشبورد", self.show_dashboard),
            ("حذف تعمیر", self.show_delete_repair),
]

        for text, command in buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=fa(text),
                command=command
            )

            btn.pack(
                fill="x",
                padx=10,
                pady=5
            )

        self.show_welcome()

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text=fa("به Repair Shop Manager خوش آمدید"),
            font=("Arial", 28, "bold")
        )

        label.pack(expand=True)

    def save_repair(self):

        repairs = self.load_repairs()

        try:
            deposit = int(
                self.entries["بیعانه"].get()
            )
        except ValueError:
            messagebox.showerror(
                "خطا",
                ".باشد عدد باید بیعانه"
            )
            return

        repair = {
            "id": self.get_next_id(repairs),
            "customer_name": self.entries["مشتری نام"].get(),
            "phone": self.entries["تماس شماره"].get(),
            "device_type": self.entries["دستگاه نوع"].get(),
            "brand": self.entries["برند"].get(),
            "problem": self.entries["خرابی شرح"].get(),
            "deposit": deposit,
            "status": "تعمیر انتظار در"
        }

        repairs.append(repair)

        self.save_repairs(repairs)

        messagebox.showinfo(
            "موفق",
            f"تعمیر با شماره {repair['id']} ثبت شد."
        )

        for entry in self.entries.values():
            entry.delete(0, "end")

    def show_add_repair(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("ثبت تعمیر جدید"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        fields = [
            "مشتری نام",
            "تماس شماره",
            "دستگاه نوع",
            "برند",
            "خرابی شرح",
            "بیعانه"
        ]

        self.entries = {}

        for field in fields:

            label = ctk.CTkLabel(
                self.content,
                text=field
            )

            label.pack(
                anchor="w",
                padx=20
            )

            entry = ctk.CTkEntry(
                self.content,
                width=400
            )

            entry.pack(
                padx=20,
                pady=(0, 10)
            )

            self.entries[field] = entry

        save_button = ctk.CTkButton(
            self.content,
            text=fa("ثبت تعمیر"),
            command=self.save_repair
        )

        save_button.pack(pady=20)
    def show_repairs(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("نمایش تعمیرات"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        repairs = self.load_repairs()

        if not repairs:

            label = ctk.CTkLabel(
                self.content,
                text=fa("هیچ تعمیری ثبت نشده")
            )

            label.pack(pady=20)

            return

        textbox = ctk.CTkTextbox(
            self.content,
            width=800,
            height=450
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        for repair in repairs:

            textbox.insert(
                "end",
                f"پذیرش شماره: {repair['id']}\n"
            )

            textbox.insert(
                "end",
                f"مشتری نام: {repair['customer_name']}\n"
            )

            textbox.insert(
                "end",
                f"تماس شماره: {repair['phone']}\n"
            )

            textbox.insert(
                "end",
                f"دستگاه نوع: {repair['device_type']}\n"
            )

            textbox.insert(
                "end",
                f"برند: {repair['brand']}\n"
            )

            textbox.insert(
                "end",
                f"خرابی شرح: {repair['problem']}\n"
            )

            textbox.insert(
                "end",
                f"بیعانه: {repair['deposit']:,} تومان\n"
            )

            textbox.insert(
                "end",
                f"وضعیت: {repair['status']}\n"
            )

            textbox.insert(
                "end",
                "\n" + "=" * 60 + "\n\n"
            )

        textbox.configure(state="disabled")  
    
    def show_update_status(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("تغییر وضعیت تعمیر"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        label = ctk.CTkLabel(
            self.content,
            text=fa("شماره پذیرش")
        )

        label.pack()

        self.status_id_entry = ctk.CTkEntry(
        self.content,
        width=250
        )

        self.status_id_entry.pack(pady=10)

        self.new_status = ctk.StringVar(
            value="در انتظار تعمیر"
        )

        statuses = [
            "در انتظار تعمیر",
            "در حال تعمیر",
            "آماده تحویل",
            "تحویل داده شد"
        ]

        for status in statuses:

            ctk.CTkRadioButton(
                self.content,
                text=fa(status),
                variable=self.new_status,
                value=status
            ).pack(pady=5)

        ctk.CTkButton(
            self.content,
            text=fa("ثبت تغییرات"),
            command=self.update_status
        ).pack(pady=20)       

    def update_status(self):

        repairs = self.load_repairs()

        try:
            repair_id = int(
                self.status_id_entry.get()
            )
        except ValueError:

            messagebox.showerror(
                fa("خطا"),
                fa("شماره پذیرش نامعتبر است")
            )

            return

        for repair in repairs:

            if repair["id"] == repair_id:

                repair["status"] = (
                    self.new_status.get()
                )

                self.save_repairs(repairs)

                messagebox.showinfo(
                    fa("موفق"),
                    fa("وضعیت تعمیر بروزرسانی شد")
                )

                return

        messagebox.showerror(
            fa("خطا"),
            fa("تعمیر مورد نظر پیدا نشد")
        )
    def show_search(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("جستجو"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        self.search_type = ctk.StringVar(value="name")

        ctk.CTkRadioButton(
            self.content,
            text=fa("نام مشتری"),
            variable=self.search_type,
            value="name"
        ).pack(pady=5)

        ctk.CTkRadioButton(
            self.content,
            text=fa("شماره پذیرش"),
            variable=self.search_type,
            value="id"
        ).pack(pady=5)

        ctk.CTkRadioButton(
            self.content,
            text=fa("شماره تلفن"),
            variable=self.search_type,
            value="phone"
        ).pack(pady=5)

        self.search_entry = ctk.CTkEntry(
            self.content,
            width=300
        )

        self.search_entry.pack(pady=15)

        ctk.CTkButton(
            self.content,
            text=fa("جستجو"),
            command=self.search_repair
        ).pack(pady=10)

        self.result_box = ctk.CTkTextbox(
            self.content,
            width=750,
            height=300
        )

        self.result_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
    def search_repair(self):

        repairs = self.load_repairs()

        keyword = self.search_entry.get().strip()

        self.result_box.delete("1.0", "end")

        found = False

        for repair in repairs:

            if (
                self.search_type.get() == "name"
                and keyword.lower() in repair["customer_name"].lower()
            ):
                found = True

            elif (
                self.search_type.get() == "phone"
                and keyword in repair["phone"]
            ):
                found = True

            elif (
                self.search_type.get() == "id"
                and keyword == str(repair["id"])
            ):
                found = True

            else:
                continue

            self.result_box.insert(
                "end",
                f"شماره پذیرش: {repair['id']}\n"
            )

            self.result_box.insert(
                "end",
                f"نام مشتری: {repair['customer_name']}\n"
            )

            self.result_box.insert(
                "end",
                f"شماره تماس: {repair['phone']}\n"
            )

            self.result_box.insert(
                "end",
                f"نوع دستگاه: {repair['device_type']}\n"
            )

            self.result_box.insert(
                "end",
                f"برند: {repair['brand']}\n"
            )

            self.result_box.insert(
                "end",
                f"وضعیت: {repair['status']}\n"
            )

            self.result_box.insert(
                "end",
                "\n" + "=" * 50 + "\n\n"
            )

        if not found:

            self.result_box.insert(
                "end",
                "موردی پیدا نشد."
            )
    def show_edit_repair(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("ویرایش تعمیر"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        ctk.CTkLabel(
            self.content,
            text=fa("شماره پذیرش")
        ).pack()

        self.edit_id_entry = ctk.CTkEntry(
            self.content,
            width=250
        )

        self.edit_id_entry.pack(pady=10)

        ctk.CTkButton(
            self.content,
            text=fa("بارگذاری اطلاعات"),
            command=self.load_repair_for_edit
        ).pack(pady=10)

    def load_repair_for_edit(self):

        repairs = self.load_repairs()

        try:
            repair_id = int(
                self.edit_id_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                fa("خطا"),
                fa("شماره پذیرش نامعتبر است")
            )

            return

        self.current_repair = None

        for repair in repairs:

            if repair["id"] == repair_id:

                self.current_repair = repair
                break

        if self.current_repair is None:

            messagebox.showerror(
                fa("خطا"),
                fa("تعمیر پیدا نشد")
            )

            return

        self.show_edit_form()

    def show_edit_form(self):

        fields = {
            "مشتری نام": self.current_repair["customer_name"],
            "تماس شماره": self.current_repair["phone"],
            "دستگاه نوع": self.current_repair["device_type"],
            "برند": self.current_repair["brand"],
            "خرابی شرح": self.current_repair["problem"],
            "بیعانه": str(self.current_repair["deposit"])
        }

        self.edit_entries = {}

        for field, value in fields.items():

            ctk.CTkLabel(
                self.content,
                text=field
            ).pack()

            entry = ctk.CTkEntry(
                self.content,
                width=400
            )

            entry.insert(0, value)

            entry.pack(
                pady=5
            )

            self.edit_entries[field] = entry

        ctk.CTkButton(
            self.content,
            text=fa("ذخیره تغییرات"),
            command=self.save_edited_repair
        ).pack(pady=20)

    def save_edited_repair(self):

        repairs = self.load_repairs()

        for repair in repairs:

            if repair["id"] == self.current_repair["id"]:

                repair["customer_name"] = self.edit_entries["مشتری نام"].get()

                repair["phone"] = self.edit_entries["تماس شماره"].get()

                repair["device_type"] = self.edit_entries["دستگاه نوع"].get()

                repair["brand"] = self.edit_entries["برند"].get()

                repair["problem"] = self.edit_entries["خرابی شرح"].get()

                repair["deposit"] = int(
                    self.edit_entries["بیعانه"].get()
                )

                break

        self.save_repairs(repairs)

        messagebox.showinfo(
            fa("موفق"),
            fa("اطلاعات تعمیر بروزرسانی شد")
        )

    def show_dashboard(self):

        self.clear_content()

        repairs = self.load_repairs()

        total_repairs = len(repairs)

        total_deposit = sum(
            repair["deposit"]
            for repair in repairs
        )       

        waiting = 0
        repairing = 0
        ready = 0
        delivered = 0

        for repair in repairs:

            status = repair["status"]

            if status == "در انتظار تعمیر":
                waiting += 1

            elif status == "در حال تعمیر":
                repairing += 1

            elif status == "آماده تحویل":
                ready += 1

            elif status == "تحویل داده شد":
                delivered += 1

        title = ctk.CTkLabel(
            self.content,
            text=fa("داشبورد"),
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        stats = [
            f"کل تعمیرات: {total_repairs}",
            f"در انتظار تعمیر: {waiting}",
            f"در حال تعمیر: {repairing}",
            f"آماده تحویل: {ready}",
            f"تحویل داده شده: {delivered}"
        ]

        for stat in stats:

            card = ctk.CTkFrame(
                self.content,
                height=60
            )

            card.pack(
                fill="x",
                padx=30,
                pady=10
            )

            label = ctk.CTkLabel(
                card,
                text=fa(stat),
                font=("Arial", 20)
            )

            label.pack(
                pady=15
            )
            
        deposit_frame = ctk.CTkFrame(
    self.content,
    height=80
)

        deposit_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        deposit_label = ctk.CTkLabel(
            deposit_frame,
            text=fa(
                f"مجموع بیعانه: {total_deposit:,} تومان"
            ),
            font=("Arial", 24, "bold")
        )

        deposit_label.pack(pady=20)

    def show_delete_repair(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text=fa("حذف تعمیر"),
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        ctk.CTkLabel(
            self.content,
            text=fa("شماره پذیرش")
        ).pack()

        self.delete_id_entry = ctk.CTkEntry(
            self.content,
            width=250
        )

        self.delete_id_entry.pack(pady=10)

        ctk.CTkButton(
            self.content,
            text=fa("حذف تعمیر"),
            command=self.delete_repair
        ).pack(pady=20)

    def delete_repair(self):

        repairs = self.load_repairs()

        try:

            repair_id = int(
                self.delete_id_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                fa("خطا"),
                fa("شماره پذیرش نامعتبر است")
            )

            return

        target = None

        for repair in repairs:

            if repair["id"] == repair_id:

                target = repair
                break

        if target is None:

            messagebox.showerror(
                fa("خطا"),
                fa("تعمیر پیدا نشد")
            )

            return

        answer = messagebox.askyesno(
            fa("تایید حذف"),
            fa("آیا از حذف این تعمیر مطمئن هستید؟")
        )

        if not answer:
            return

        repairs.remove(target)

        self.save_repairs(repairs)

        messagebox.showinfo(
            fa("موفق"),
            fa("تعمیر حذف شد")
        )

        self.delete_id_entry.delete(
            0,
            "end"
        )
RepairShopGUI()
