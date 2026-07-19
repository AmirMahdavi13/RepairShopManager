# Repair Shop Manager

A modern desktop application built with Python and PySide6 for managing repair shop operations.

## Overview

Repair Shop Manager is designed to simplify the workflow of repair centers by providing an easy-to-use interface for registering, tracking, editing, searching, and managing repair records.

The application stores data locally using JSON and offers a clean graphical user interface optimized for everyday business use.

---

## Features

### Repair Management
- Register new repairs
- Automatic repair ID generation
- Edit repair information
- Delete repair records
- Track repair status
<img width="1204" height="731" alt="image" src="https://github.com/user-attachments/assets/09a7748b-1e36-4164-a1c0-aa3ae8d11943" />
<img width="1204" height="728" alt="image" src="https://github.com/user-attachments/assets/65ac1d94-26f5-48f3-9845-9f7b1e405d72" />


### Search System
- Search by repair ID
- Search by customer name
- Search by phone number
<img width="1206" height="726" alt="image" src="https://github.com/user-attachments/assets/46d9546d-5722-471a-9f3c-abb0ab393b5c" />

### Dashboard
- Total repairs count
- Repairs waiting for service
- Repairs currently being repaired
- Repairs ready for delivery
- Delivered repairs count
- Total deposits summary
<img width="1201" height="730" alt="image" src="https://github.com/user-attachments/assets/0944503a-d330-4599-81da-d2f4263a15d9" />


### User Interface
- Modern PySide6 GUI
- Dark theme
- Persian language support
- Responsive layout
- Simple and user-friendly workflow

---

## Technologies Used

- Python 3
- PySide6 (Qt for Python)
- JSON
- Pathlib

---

## Project Structure

```text
RepairShopManager/
│
├── qt_gui.py
├── repairs.json
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/AmirMahdavi13/RepairShopManager.git
```

Move into the project folder:

```bash
cd RepairShopManager
```

Install dependencies:

```bash
pip install PySide6
```

Run the application:

```bash
python qt_gui.py
```

---

## Current Version

### Version 1.0

Implemented:

- Repair registration
- Repair listing
- Search system
- Repair editing
- Repair deletion
- Status management
- Dashboard
- Local JSON persistence
- Modern UI

---

## Future Improvements

- SQLite database support
- Export to PDF
- Export to Excel
- Cost and profit management
- Delivery history
- Customer management
- Backup system

---

## Author

Developed by Amir Mahdavi

GitHub:
https://github.com/AmirMahdavi13

---

## License

This project is available for educational, personal, and portfolio purposes.
# مدیریت تعمیرگاه (Repair Shop Manager)

نرم‌افزار دسکتاپ مدیریت تعمیرگاه، توسعه داده شده با Python و PySide6.

## معرفی

Repair Shop Manager یک نرم‌افزار ساده و کاربردی برای مدیریت فرآیندهای روزانه تعمیرگاه است که امکان ثبت، ویرایش، جستجو، حذف و پیگیری وضعیت تعمیرات را فراهم می‌کند.

اطلاعات به صورت محلی در فایل JSON ذخیره شده و رابط کاربری برنامه با تمرکز بر سادگی و سرعت طراحی شده است.

---

## امکانات

### مدیریت تعمیرات
- ثبت تعمیر جدید
- تولید خودکار شماره پذیرش
- ویرایش اطلاعات تعمیر
- حذف تعمیر
- مدیریت وضعیت تعمیر

### سیستم جستجو
- جستجو بر اساس شماره پذیرش
- جستجو بر اساس نام مشتری
- جستجو بر اساس شماره تماس

### داشبورد
- تعداد کل تعمیرات
- تعداد تعمیرات در انتظار تعمیر
- تعداد تعمیرات در حال تعمیر
- تعداد تعمیرات آماده تحویل
- تعداد تعمیرات تحویل داده شده
- مجموع بیعانه‌های ثبت شده

### رابط کاربری
- رابط گرافیکی مدرن مبتنی بر PySide6
- تم تیره
- پشتیبانی از زبان فارسی
- طراحی ساده و کاربردی

---

## تکنولوژی‌های استفاده شده

- Python 3
- PySide6
- JSON
- Pathlib

---

## ساختار پروژه

```text
RepairShopManager/
│
├── qt_gui.py
├── repairs.json
└── README.md
```

---

## نصب و اجرا

دریافت پروژه:

```bash
git clone https://github.com/AmirMahdavi13/RepairShopManager.git
```

ورود به پوشه پروژه:

```bash
cd RepairShopManager
```

نصب کتابخانه‌ها:

```bash
pip install PySide6
```

اجرای برنامه:

```bash
python qt_gui.py
```

---

## نسخه فعلی

### نسخه 1.0

قابلیت‌های تکمیل شده:

- ثبت تعمیر
- نمایش تعمیرات
- جستجو
- ویرایش تعمیر
- حذف تعمیر
- تغییر وضعیت تعمیر
- داشبورد آماری
- ذخیره‌سازی اطلاعات در JSON
- رابط کاربری مدرن

---

## برنامه‌های آینده

- استفاده از پایگاه داده SQLite
- خروجی PDF
- خروجی Excel
- مدیریت هزینه‌ها و سود
- تاریخچه تحویل
- مدیریت مشتریان
- سیستم پشتیبان‌گیری

---

## توسعه‌دهنده

امیر مهدوی

گیت‌هاب:
https://github.com/AmirMahdavi13

---

## مجوز

این پروژه برای اهداف آموزشی، شخصی و رزومه قابل استفاده است.
