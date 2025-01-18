from telethon import Button
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup

def key_start_user():
    
    order = Button.text("سفارش استارت (زیر مجموعه) ⭐️", resize=True)
    detail = Button.text("اطلاعات حساب 👤", resize=True)
    inpacet =  Button.text("افزایش موجودی 👛", resize=True)
    message =  Button.text("اطلاع رسانی ها 📌", resize=True)
    rule =  Button.text("قوانین و راهنما 💡", resize=True)
    support =  Button.text("پشتیبانی ☎️", resize=True)
    
    return [[order,detail] ,[support,inpacet],[message],[rule]] 

def key_start_sudo():
    
    keyboard = [
        
        [Button.text("اپدیت قیمت"), Button.text("اپلود سشن")],
        [Button.text("پیام همگانی"), Button.text("شارژ حساب کاربر")],
        [Button.text("مشتریان و گزارشات"),Button.text("ساخت کلید🔑")]
    ]
    
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


def key_read_button_refferalbot(referalls, page=1, page_size=30):

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_data = referalls[start_index:end_index]

    key = []

    for i in current_page_data:
        key.append([
            Button.inline(f"🤖 اسم: {i[1]}", data=f"{i[0]}_name"),
            Button.inline(f"💰 قیمت: {i[3]}", data=f"{i[0]}_price"),
            Button.inline(f"🔢 شمارشگر: {i[0]}", data=f"{i[0]}_counter"),
        ])


    navigation_buttons = []
    if start_index > 0: 
        navigation_buttons.append(Button.inline("⏪ صفحه قبل", data=f"page_{page - 1}"))
    if end_index < len(referalls):
        navigation_buttons.append(Button.inline("⏩ صفحه بعد", data=f"page_{page + 1}"))

    if navigation_buttons:
        key.append(navigation_buttons) 

    return key