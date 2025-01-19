from telethon import Button

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
        
        [Button.text("کلید رفرال 📍",resize=True), Button.text("آپلود سشن 📤",resize=True)],
        [Button.text("پیام همگانی ✉️",resize=True), Button.text("شارژ حساب کاربر ➕",resize=True)],
        [Button.text("مشتریان و گزارشات 📎",resize=True)]
    ]
    
    return keyboard

def refferal_key():
    keyboard = [
        [Button.text("آپدیت قیمت 📌", resize=True),Button.text("➕ ساخت کلید 🔑", resize=True)],
        [Button.text("♾️ نمایش کلید ها 🔑", resize=True),Button.text("➖ حذف کلید 🔑", resize=True)],
        [Button.text("بازگشت 🔙", resize=True)]
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
        [Button.text("بازگشت 🔙", resize=True, single_use=False, selective=False)]
    ]
    return keyboard

def Back_menu():
    keyboard = [
        [Button.text("منو قبل 🔙", resize=True, single_use=False, selective=False)]
    ]
    return keyboard

def how_pay():
    keyboard = [
        [Button.text("💵 درگاه بانکی", resize=True),Button.text("پرداخت مستقیم 📥", resize=True)],
        [Button.text("بازگشت 🔙", resize=True)]
    ]
    return keyboard

def pay_dargah(payment_url,code,amount):
    try:
        keyboard = [
            [Button.url("درگاه پرداخت 🛍", url=payment_url),
            Button.inline("تایید پرداخت ✅", data=f"at_{code},am_{amount}")
            ]
        ]
        return keyboard
    except Exception as e:
        print(f"Error generating payment link: {e}")
        return [[Button.inline("خطا در ایجاد لینک پرداخت", data="sss")]]

def key_read_button_refferalbot(referalls, page=1, page_size=30):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_data = referalls[start_index:end_index]

    key = []
    key.append([
        
            Button.inline("ردیف ⚪️", data="ShowAlert"),
            Button.inline("اسم ربات 🎯", data="ShowAlert"),
            Button.inline("💰 قیمت: ", data="ShowAlert")
         
                ])
    
    for i in current_page_data:
        key.append([
            Button.inline(f"✅ {i[0]})", data=f"{i[0]}_counter"),
            Button.inline(f"{i[1]}", data=f"{i[0]}_name"),
            Button.inline(f"{i[3]}", data=f"{i[0]}_price"),
        ])

    navigation_buttons = []
    if start_index > 0: 
        navigation_buttons.append(Button.inline("⏪ صفحه قبل", data=f"page_{page - 1}"))
    if end_index < len(referalls):
        navigation_buttons.append(Button.inline("⏩ صفحه بعد", data=f"page_{page + 1}"))

    if navigation_buttons:
        key.append(navigation_buttons)

    key.append([Button.inline("بازگشت 🔙", data="back")])

    return key
