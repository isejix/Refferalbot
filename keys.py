from telethon import Button
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup

def key_start_user():
    
    order = Button.text("سفارش استارت (زیر مجموعه) ⭐️", resize=True)
    detail = Button.text("اطلاعات حساب 👤", resize=True)
    inpacet =  Button.text("افزایش موجودی 👛", resize=True)
    star =  Button.text("خدمات ویژه 💫", resize=True)
    message =  Button.text("اطلاع رسانی ها 📌", resize=True)
    rule =  Button.text("قوانین و راهنما 💡", resize=True)
    support =  Button.text("پشتیبانی ☎️", resize=True)
    
    return [[order] ,[detail,inpacet],[star,message],[rule,support]] 

def key_start_sudo():
    
    keyboard = [
        
        [Button.text("اپدیت قیمت ها"), Button.text("اپلود سشن")],
        [Button.text("پیام همگانی"), Button.text("شارژ حساب کاربر")],
        [Button.text("مشتریان و گزارشات"), Button.text("ادمین")]
    ]
    
    return keyboard

async def key_start_admin(event):
    buttons = [
        
        [Button.text("اپدیت قیمت ها"), Button.text("اپلود سشن")],
        [Button.text("پیام همگانی"), Button.text("شارژ حساب کاربر")]

    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return keyboard

def key_join_ejbar():
    keyboard = [
        
        [Button.url("جوین چنل✔", url='https://t.me/refferall_bo')]
    ]
    return keyboard

def cancel():
    back =  Button.text("انصراف ❌", resize=True)
    return [[back]] 


def Back_Reply():
    keyboard = [
        [Button.text("بازگشت", resize=True, single_use=False, selective=False)]
    ]
    return keyboard


def AllAdmins(admins):
    keyboard = []
    
    for admin in admins:
        keyboard.append([
            Button.inline(f"{admin[1]}", b"ShowAlert"),
            Button.inline("⚙️", f"EditAcsess_{admin[1]}"),
            Button.inline("🗑", f"Delete_{admin[1]}")
        ])
    keyboard.append([
        Button.inline("افزودن ادمین", b"NewAdmin")
    ])
    
    return keyboard


def key_access_admin(userid, access, role):
    keyboard = []
    
    # سطر مربوط به شناسه کاربر
    keyboard.append([Button.inline(f"{userid}", b"ShowAlert")])
    
    # سطر مربوط به نقش کاربر
    role_text = "سودو" if role == 1 else "ادمین"
    keyboard.append([
        Button.inline("سطح دسترسی", b"ShowAlert"),
        Button.inline(role_text, f"AcsessTypeRole_{userid}".encode())
    ])

    # دسترسی ثبت ادمین
    new_admin_status = "🟢" if access[1] == 1 else "🔴"
    keyboard.append([
        Button.inline("ثبت ادمین", b"ShowAlert"),
        Button.inline(new_admin_status, f"NewAdminAcsess_{userid}".encode())
    ])
    
    # دسترسی حذف ادمین
    delete_admin_status = "🟢" if access[2] == 1 else "🔴"
    keyboard.append([
        Button.inline("حذف ادمین", b"ShowAlert"),
        Button.inline(delete_admin_status, f"DeleteAdminAcsess_{userid}".encode())
    ])
    
    # دسترسی ارسال پیام همگانی
    send_message_status = "🟢" if access[3] == 1 else "🔴"
    keyboard.append([
        Button.inline("ارسال پیام همگانی", b"ShowAlert"),
        Button.inline(send_message_status, f"SendMessageAllUsersAcsess_{userid}".encode())
    ])
    
    send_message_status = "🟢" if access[4] == 1 else "🔴"
    keyboard.append([
        Button.inline("آپلود سشن", b"ShowAlert"),
        Button.inline(send_message_status, f"uploadsessionAcsess_{userid}".encode())
    ])
    
    send_message_status = "🟢" if access[5] == 1 else "🔴"
    keyboard.append([
        Button.inline("آپدیت قیمت", b"ShowAlert"),
        Button.inline(send_message_status, f"upadtebalanceAcsess_{userid}".encode())
    ])
    
    # دسترسی مسدود کردن کاربر


    
    # دکمه بازگشت
    keyboard.append([Button.inline("بازگشت", b"Back")])
    
    return keyboard
