from telethon import Button

def key_start_user():
    
    order = Button.text("سفارش استارت (زیر مجموعه) ⭐️", resize=True)
    detail = Button.text("اطلاعات حساب 👤", resize=True)
    inpacet =  Button.text("افزایش موجودی 👛", resize=True)
    message =  Button.text("اطلاع رسانی ها 📌", resize=True)
    rule =  Button.text("قوانین و راهنما 💡", resize=True)
    support =  Button.text("پشتیبانی ☎️", resize=True)
    superq =  Button.text("خدمات ویژه! 💫", resize=True)
    
    
    return [[order],[detail,inpacet],[message,superq],[rule,support]] 

def key_start_sudo():
    
    keyboard = [
        
        [Button.text("مدیریت ربات ها📍",resize=True), Button.text("آپلود سشن 📤",resize=True)],
        [Button.text("پیام همگانی ✉️",resize=True), Button.text("حساب کاربر 👤",resize=True)],
        [Button.text("مشتریان و گزارشات 📎",resize=True),Button.text("کد تخفیف 🏷",resize=True)]
    ]
    
    return keyboard

def key_charg_user():
    
    keyboard = [
        
        [Button.text("کسر حساب ➖",resize=True), Button.text("شارژ حساب ➕",resize=True)],
        [Button.text("حذف حساب شارژ 🗑",resize=True),Button.text("حذف حساب کاربر 🗑",resize=True)],
        [Button.text("مسدود کردن 🔴",resize=True),Button.text("رفع مسدودیت 🟢",resize=True)],
        [Button.text("بازگشت 🔙", resize=True)]
        
        
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
            [Button.url("درگاه پرداخت 🛍", url=payment_url)],
            [Button.inline("بررسی✅", data=f"at_{code},am_{amount}")
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
    
    for i in range(1,len(current_page_data)):
        key.append([
            Button.inline(f"✅ {i})", data=f"counter"),
            Button.url(f"{current_page_data[i][1]}", url=f"{current_page_data[i][2]}"),
            Button.inline(f"{current_page_data[i][3]}", data=f"price_{int(float(current_page_data[i][0]))}"),
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

def key_channel():
    keyboard = [
        
        [Button.url("کانال گزارش خرید 📊", url='https://t.me/refferall_bo')]
    ]
    return keyboard

def key_id_suppoort():
    keyboard = [
        
        [Button.url("ارتباط با پشتیبانی 🆔", url='https://t.me/sajjad_emp')]
    ]
    return keyboard

def key_order_ref(balance,namee,count=1):
    keyboard = [[
        
            Button.inline("➕", data=f"plus_{count}"),
            Button.inline(f"تعداد: {count}", data="count"),
            Button.inline("➖", data=f"neg_{count}")
                ],
                [
            Button.inline("1", data="do_1"),
            Button.inline("5", data="do_5"),
            Button.inline("10", data="do_10"),
            Button.inline("15", data="do_15"),
            Button.inline("20", data="do_20"),
            Button.inline("50", data="do_50"),
            Button.inline("100", data="do_100")
                ],
                [
            Button.inline(f"💴 قیمت کل: {balance} تومان", data=f"balance_{namee}")
                ],
                [
            Button.inline("ثبت سفارش ✅", data="accept_order"),
                    
                ]
                ,
                [
            Button.inline("کد تخفیف 🏷", data="discount_"),
                    
                ]
    ]
    return keyboard
    
def key_chanell_notif():
    keyboard = [
        
        [Button.url("کانال گزارشات 🆔", url='https://t.me/refferall_bo')]
    ]
    return keyboard    

def key_discouny():
    
    keyboard = [
        [Button.text("حذف تخفیف 🗑", resize=True),Button.text("ثبت تخفیف 🟢", resize=True)],
        [Button.text("بازگشت 🔙", resize=True)]
    ]
    return keyboard