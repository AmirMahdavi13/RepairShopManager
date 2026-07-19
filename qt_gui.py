from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog
)

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "repairs.json"


class RepairShopGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Repair Shop Manager")
        self.resize(1200, 700)

        self.setup_ui()
        self.setStyleSheet("""
            QWidget{
                background-color:#202124;
                color:white;
                font-size:14px;
            }

            QFrame{
                background-color:#2b2b2b;
                border-radius:12px;
            }

            QPushButton{               
                border:1px solid #444;
                
                background-color:#3b82f6;

                border:none;

                border-radius:10px;

                padding:10px;

                font-size:15px;

                font-weight:bold;
            }

            QPushButton:hover{
                background-color:#2563eb;
            }

            QPushButton:pressed{
                background-color:#1d4ed8;
            }

            QLineEdit,
            QTextEdit{
                background-color:#303134;

                border:1px solid #555;

                border-radius:8px;

                padding:8px;
            }

            QTableWidget{
                background-color:#303134;

                border:none;

                gridline-color:#444;
            }

            QHeaderView::section{
                background-color:;

                color:white;

                padding:8px;

                border:none;

                font-weight:bold;
            }

            QLabel{
                color:white;
            }

            """)
        self.editing_repair_id = None

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

        return max(
            repair["id"]
            for repair in repairs
        ) + 1


    def clear_content(self):

        layout = self.content.layout()

        while layout.count():

            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():


                while item.layout().count():

                    child = item.layout().takeAt(0)

                    if child.widget():

                        child.widget().deleteLater() 

    def show_add_repair(self):

        self.clear_content()

        layout = self.content.layout()

        title = QLabel("ثبت تعمیر جدید")

        layout.addWidget(title)

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText(
            "نام مشتری"
        )

        layout.addWidget(self.customer_name)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText(
            "شماره تماس"
        )

        layout.addWidget(self.phone)

        self.device_type = QLineEdit()
        self.device_type.setPlaceholderText(
            "نوع دستگاه"
        )

        layout.addWidget(self.device_type)

        self.brand = QLineEdit()
        self.brand.setPlaceholderText(
            "برند"
        )

        layout.addWidget(self.brand)

        self.problem = QTextEdit()
        self.problem.setPlaceholderText(
            "شرح خرابی"
        )

        layout.addWidget(self.problem)

        self.deposit = QLineEdit()
        self.deposit.setPlaceholderText(
            "بیعانه"
        )

        layout.addWidget(self.deposit)

        self.save_button = QPushButton(
            "ثبت  تعمیر"
        )

        self.save_button.clicked.connect(self.save_repair_gui)

        layout.addWidget(self.save_button)

    def save_repair_gui(self):

        repairs = self.load_repairs()

        try:
            deposit = int(
                self.deposit.text()
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "خطا",
                "بیعانه باید عدد باشد"
            )

            return

        # حالت ویرایش
        if self.editing_repair_id is not None:

            for repair in repairs:

                if repair["id"] == self.editing_repair_id:

                    repair["customer_name"] = (
                        self.customer_name.text()
                    )

                    repair["phone"] = (
                        self.phone.text()
                    )

                    repair["device_type"] = (
                        self.device_type.text()
                    )

                    repair["brand"] = (
                        self.brand.text()
                    )

                    repair["problem"] = (
                        self.problem.toPlainText()
                    )

                    repair["deposit"] = deposit

                    self.save_repairs(repairs)

                    self.editing_repair_id = None

                    QMessageBox.information(
                        self,
                        "موفق",
                        "تعمیر ویرایش شد"
                    )

                    self.show_repairs()

                    return

        # حالت ثبت تعمیر جدید
        repair = {

            "id": self.get_next_id(repairs),

            "customer_name":
                self.customer_name.text(),

            "phone":
                self.phone.text(),

            "device_type":
                self.device_type.text(),

            "brand":
                self.brand.text(),

            "problem":
                self.problem.toPlainText(),

            "deposit":
                deposit,

            "status":
                "در انتظار تعمیر"
        }

        repairs.append(repair)

        self.save_repairs(repairs)

        QMessageBox.information(
            self,
            "موفق",
            f"تعمیر {repair['id']} ثبت شد"
        )

        self.show_add_repair()
    
    def show_repairs(self):

        self.clear_content()

        repairs = self.load_repairs()

        layout = self.content.layout()

        title = QLabel("نمایش تعمیرات")

        layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "پذیرش",
            "مشتری",
            "دستگاه",
            "بیعانه",
            "وضعیت"
        ])

        self.table.setRowCount(len(repairs))

        for row, repair in enumerate(repairs):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(repair["id"])
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    repair["customer_name"]
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    repair["device_type"]
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(repair["deposit"])
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    repair["status"]
                )
            )

        layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()

        edit_btn = QPushButton("ویرایش")
        delete_btn = QPushButton("حذف")
        status_btn = QPushButton("تغییر وضعیت")

        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(status_btn)

        layout.addLayout(buttons_layout)

        edit_btn.clicked.connect(self.edit_selected_repair)
        delete_btn.clicked.connect(self.delete_selected_repair)
        status_btn.clicked.connect(self.change_selected_status)

    def get_selected_repair_id(self):

            row = self.table.currentRow()

            if row == -1:
                return None

            return int(
                self.table.item(row, 0).text()
            )
        
    def delete_selected_repair(self):

        repair_id = self.get_selected_repair_id()

        if repair_id is None:

            QMessageBox.warning(
                self,
                "خطا",
                "ابتدا یک تعمیر انتخاب کنید"
            )

            return

        repairs = self.load_repairs()

        new_repairs = []

        for repair in repairs:

            if repair["id"] != repair_id:
                new_repairs.append(repair)

        self.save_repairs(new_repairs)

        QMessageBox.information(
            self,
            "موفق",
            "تعمیر حذف شد"
        )

        self.show_repairs()

    
    def edit_selected_repair(self):

        repair_id = self.get_selected_repair_id()

        if repair_id is None:

            QMessageBox.warning(
                self,
                "خطا",
                "ابتدا یک تعمیر انتخاب کنید"
            )

            return

        repairs = self.load_repairs()

        for repair in repairs:

            if repair["id"] == repair_id:

                self.editing_repair_id = repair_id

                self.show_add_repair()

                self.customer_name.setText(
                    repair["customer_name"]
                )

                self.phone.setText(
                    repair["phone"]
                )

                self.device_type.setText(
                    repair["device_type"]
                )

                self.brand.setText(
                    repair["brand"]
                )

                self.problem.setText(
                    repair["problem"]
                )

                self.deposit.setText(
                    str(repair["deposit"])
                )

                self.save_button.setText(
                    "ذخیره تغییرات"
                )

                return
    
    def change_selected_status(self):

        repair_id = self.get_selected_repair_id()

        if repair_id is None:

            QMessageBox.warning(
                self,
                "خطا",
                "ابتدا یک تعمیر انتخاب کنید"
            )

            return

        statuses = [
            "در انتظار تعمیر",
            "در حال تعمیر",
            "آماده تحویل",
            "تحویل داده شد"
        ]

        new_status, ok = QInputDialog.getItem(
            self,
            "تغییر وضعیت",
            "وضعیت جدید را انتخاب کنید:",
            statuses,
            0,
            False
        )

        if not ok:
            return

        repairs = self.load_repairs()

        for repair in repairs:

            if repair["id"] == repair_id:

                repair["status"] = new_status

                self.save_repairs(repairs)

                QMessageBox.information(
                    self,
                    "موفق",
                    "وضعیت بروزرسانی شد"
                )

                self.show_repairs()

                return

    def show_search(self):

        self.clear_content()

        layout = self.content.layout()

        title = QLabel("جستجو(فقط شماره پذیرش یا شماره)")

        layout.addWidget(title)

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "عبارت جستجو..."
        )

        layout.addWidget(self.search_box)

        search_btn = QPushButton(
            "جستجو"
        )

        search_btn.clicked.connect(
            self.search_repairs
        )

        layout.addWidget(search_btn)

        self.search_table = QTableWidget()

        self.search_table.setColumnCount(5)

        self.search_table.setHorizontalHeaderLabels([
            "پذیرش",
            "مشتری",
            "دستگاه",
            "بیعانه",
            "وضعیت"
        ])

        layout.addWidget(
            self.search_table
        )
    
    def search_repairs(self):

        keyword = (
            self.search_box.text()
            .strip()
            .lower()
        )

        repairs = self.load_repairs()

        results = []

        for repair in repairs:

            if (

                keyword in str(
                    repair["id"]
                ).lower()

                or

                keyword in repair[
                    "customer_name"
                ].lower()

                or

                keyword in repair[
                    "phone"
                ].lower()

            ):

                results.append(
                    repair
                )

        self.search_table.setRowCount(
            len(results)
        )

        for row, repair in enumerate(results):

            self.search_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(repair["id"])
                )
            )

            self.search_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    repair["customer_name"]
                )
            )

            self.search_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    repair["device_type"]
                )
            )

            self.search_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(repair["deposit"])
                )
            )

            self.search_table.setItem(
                row,
                4,
                QTableWidgetItem(
                    repair["status"]
                )
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

        layout = self.content.layout()

        title = QLabel("داشبورد")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:35px;
            font-weight:bold;
            margin:20px;
        """)

        layout.addWidget(title)

        grid = QGridLayout()

        stats = [

            ("کل تعمیرات", total_repairs),

            ("در انتظار تعمیر", waiting),

            ("در حال تعمیر", repairing),

            ("آماده تحویل", ready),

            ("تحویل داده شده", delivered),

            ("مجموع بیعانه", f"{total_deposit:,} تومان")
        ]

        row = 0
        col = 0

        for title_text, value in stats:

            card = QFrame()

            card.setFixedSize(250, 130)

            card.setStyleSheet("""
                QFrame{
                    background-color:#2b2b2b;
                    border-radius:15px;
                }
            """)

            card_layout = QVBoxLayout(card)

            title_label = QLabel(title_text)

            title_label.setAlignment(Qt.AlignCenter)

            title_label.setStyleSheet("""
                font-size:16px;
                font-weight:bold;
            """)

            value_label = QLabel(str(value))

            value_label.setAlignment(Qt.AlignCenter)

            value_label.setStyleSheet("""
                font-size:24px;
                font-weight:bold;
                color:#4CAF50;
            """)

            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)

            grid.addWidget(card, row, col)

            col += 1

            if col == 2:
                col = 0
                row += 1

        layout.addLayout(grid)

        layout.setAlignment(grid, Qt.AlignTop | Qt.AlignHCenter)   

    def setup_ui(self):

            main_layout = QHBoxLayout(self)

            # Sidebar
            sidebar = QFrame()
            sidebar.setFixedWidth(250)

            sidebar_layout = QVBoxLayout(sidebar)

            title = QLabel("Repair Shop Manager")

            title.setStyleSheet("""
                font-size:20px;
                font-weight:bold;
                """)
            sidebar_layout.addWidget(title)

            buttons = [
                ("ثبت تعمیر", self.show_add_repair),
                ("نمایش تعمیرات", self.show_repairs),
                ("جستجو", self.show_search),
                ("داشبورد", self.show_dashboard)
            ]

            for text, func in buttons:

                btn = QPushButton(text)
                btn.setMinimumHeight(45)

                btn.setStyleSheet("""
                    QPushButton{
                        background-color:#2f3136;

                        border:1px solid #444;

                        border-radius:10px;

                        padding:10px;

                        font-size:16px;

                        font-weight:bold;
                    }

                    QPushButton:hover{
                        background-color:#3a3d42;
                    }
                    """)
                
                if func:
                    btn.clicked.connect(func)

                sidebar_layout.addWidget(btn)
                sidebar_layout.setSpacing(12)
                sidebar_layout.setContentsMargins(
                    15,
                    20,
                    15,
                    20
                    )
            
            sidebar_layout.addStretch()

            # Content
            self.content = QFrame()

            content_layout = QVBoxLayout(self.content)
            content_layout.addStretch()

            self.welcome_label = QLabel(
                "به Repair Shop Manager خوش آمدید"
            )

            self.welcome_label.setStyleSheet("""
                font-size:32px;
                font-weight:bold;
            """)
            self.welcome_label.setAlignment(
                Qt.AlignCenter
            )

            content_layout.addWidget(
             self.welcome_label
            )

            content_layout.addStretch()

            main_layout.addWidget(sidebar)
            main_layout.addWidget(self.content)


if __name__ == "__main__":

        app = QApplication(sys.argv)

        window = RepairShopGUI()

        window.show()

        sys.exit(app.exec())
        
        