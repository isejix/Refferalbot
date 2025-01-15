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
        [Button.text("رفرال")],
        [Button.text("رفع مسدودیت کاربر"), Button.text("مسدود کردن کاربر")],
        [Button.text("پیام همگانی"), Button.text("شارژ حساب کاربر")],
        [Button.text("مشتریان و گزارشات"), Button.text("ادمین")]
    ]
    return keyboard

async def key_start_admin(event):
    buttons = [
        [KeyboardButton('پیام همگانی'), KeyboardButton('ادمین')],
        [KeyboardButton('رفرال'), KeyboardButton('شارژ حساب کاربر')],
        [KeyboardButton('رفع مسدودیت کاربر'), KeyboardButton('مسدود کردن کاربر')]
    ]
    
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def key_join_ejbar():
    keyboard = [
        [Button.url("جوین چنل✔", url='https://t.me/refferall_bo')]
    ]
    return keyboard