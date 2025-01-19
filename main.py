from telethon import TelegramClient, events
import keys
import db
import ConstText
from socks import SOCKS5, SOCKS4, HTTP
import os
from asyncio import sleep
import pay
import  re
import schedule


api_id = 2631644
api_hash = '2a0dec0b80b84e501c5d9806248eb235'

proxyx = {
    'proxy_type': 'socks5',  # Can be 'socks5', 'http', or 'https'
    'proxy_host': '127.0.0.1',  # Proxy server address
    'proxy_port': 2080  # Proxy server port
}

client = TelegramClient(
    'anon', api_id, api_hash,
    proxy=(proxyx['proxy_type'], proxyx['proxy_host'], proxyx['proxy_port'])
).start(bot_token="7675469785:AAH9eU50e5AxM-iWuHdjZn04e3em_m3HZzk")

global user_step,user_cach

user_step = {}
user_cach ={}


@client.on(events.NewMessage())
async def process_pay_dargah(event):
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]

    if current_step == "cash":
        if event.text.isdigit():
            cash = float(event.text)
            user_cach[user_id]["cash"] = cash
            if user_cach[user_id]["cash"] >= 1000:
                payment_url = pay.link_payment(user_cach[user_id]["cash"])
                match = re.search(r'/StartPay/([^/]+)', payment_url)
                await event.respond("⏳",buttons=keys.key_start_user())
                if match:
                    code = match.group(1)
                    await event.reply(
                        f"💳 فاکتور افزایش موجودی به مبلغ {user_cach[user_id]['cash']} تومان صادر گردید.\n"
                        "👈 درصورتی که مورد تاییدتان است با انتخاب یکی از گزینه های زیر پرداخت خود را انجام دهید",
                        buttons=keys.pay_dargah(payment_url,code,user_cach[user_id]['cash'])
                    )
                    user_cach.pop(user_id)
                    user_step.pop(user_id)
                    
            else:
                await client.send_message(user_id,"مبلغ شما کمتر از میزان تعیین شده برای پرداخت است لطفا مبلغ درخواست را افزایش دهید و دوباره تلاش کنید 🌹")
        else:
            await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
            
    nam = event.text

    if current_step == "nam" and nam != "➖ حذف کلید 🔑":
        user_cach[user_id]["nam"] = nam
        is_valid = await db.read_referrabot_name(user_cach[user_id]["nam"])
        if is_valid:
            if user_cach[user_id]["nam"]  == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
            await db.delete_referrabot(str(user_cach[user_id]["nam"]))
            keyboard = keys.refferal_key()
            await event.respond("کلید با موفقیت حذف شد ✅",buttons=keyboard)
            user_step.pop(user_id)
            user_cach.pop(user_id)
        
        else:
            await event.respond("ربات با این اسم وجود ندارد 🔴")
            
    namee = event.text

    if current_step == "namee" and namee != "آپدیت قیمت 📌":
        user_cach[user_id]["namee"] = namee
        if user_cach[user_id]["namee"]  == "منو قبل 🔙":
            user_step.pop(user_id)
            user_cach.pop(user_id)
            keyboard = keys.refferal_key()
            await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
            return
        if namee.isdigit():
            if user_cach[user_id]["namee"]  == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
            user_step[user_id] = "balancee"
            is_valid = await db.read_referrabot_name(user_cach[user_id]["namee"])
            if is_valid:
                await event.respond("لطفاً قیمت جدید را به تومان وارد کنید 🙏🏻")
            else:
                await event.respond("نام اشتباه وارد شده است 🔴")
        else:
            await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
    
    name = event.text
    
    if user_step[user_id] == "منو قبل 🔙":
        keyboard = keys.refferal_key()
        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
        return
    
    if current_step == "name" and name != "➕ ساخت کلید 🔑":
 
            user_cach[user_id]["name"] = name
            if user_cach[user_id]["name"]  == "منو قبل 🔙":
                user_step.pop(user_id)
                user_cach.pop(user_id)
                keyboard = keys.refferal_key()
                await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                return
            user_step[user_id] = "username"
            await event.respond("لطفاً یوزرنیم ربات را وارد کنید 🙏🏻")
            
    if current_step == "username":
        
        username = event.text
        pattern = r"https://t\.me/([a-zA-Z0-9_]+)"

        if re.match(pattern, username):
            user_cach[user_id]["username"] = username
            if user_cach[user_id]["username"] == "منو قبل 🔙":
                user_step.pop(user_id)
                user_cach.pop(user_id)
                keyboard = keys.refferal_key()
                await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                return
            user_step[user_id] = "balance"
            await event.respond("لطفاً قیمت را به تومان وارد کنید 🙏🏻")
        else:
            await event.respond("لطفاً لینک به عنوان یوزنیم وارد کنید 🙏🏻")
            
        
    if current_step == "balance":
        if event.text.isdigit():
            try:
                balance = float(event.text) 
                user_cach[user_id]["balance"] = balance  
                if user_cach[user_id]["balance"] == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
                user_step[user_id] = "completed" 
                await db.create_referrabot(user_cach[user_id]['name'], user_cach[user_id]['username'], user_cach[user_id]['balance'])
                keyboard = keys.refferal_key()
                await event.respond(f"اطلاعات ربات ذخیره شد:\nنام: {user_cach[user_id]['name']}\nیوزرنیم: {user_cach[user_id]['username']}\nقیمت: {balance}",buttons=keyboard)
                user_step.pop(user_id)
                user_cach.pop(user_id)
            except ValueError:
                if event.text == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
                await event.respond("لطفاً قیمت را به‌صورت عدد وارد کنید.")
        else:
            await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
            
        if current_step == "user_id":
            user_id = event.text
            if user_id.isdigit():
                user_cach[user_id]["user_id"] = user_id
                await event.reply("چقدر می‌خواهید حساب کاربر را شارژ کنید؟")
                user_step[user_id] = "charge_amount"

        elif current_step == "charge_amount":
            charge_amount = event.text
            if charge_amount.isdigit():
                user_cach[user_id]["charge_amount"] = int(charge_amount)
                user_id = user_cach[user_id]["user_id"]
                f = await db.ReadWalletUser(user_id)
                await db.UpdateWalletUser(int(user_id), int(charge_amount)+ f[0])
                keyboard = keys.key_start_sudo()
                await event.reply(f"مقدار {charge_amount} حساب کاربر {user_id} شارژ شد.",buttons=keyboard)
                await client.send_message(int(user_id), f"مقدار {charge_amount} حساب شما شارژ شد.")
                user_step.pop(user_id)
                user_cach.pop(user_id)
            else:
                await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")

def check_function():
    print("Checking...")
    condition = True  # شرط دلخواه

    if condition:
        with client:  # اجرا در داخل کلاینت
            client.loop.run_until_complete(
                client.send_message('me', 'شرط برقرار شد!')
            )

# زمان‌بندی اجرای تابع
schedule.every(5).seconds.do(check_function)         

@client.on(events.NewMessage(pattern="/start"))
async def start_bot(event):
    userid = event.sender_id
    text = event.raw_text

    if text == "/start":
        anyadmin = await db.ReadAdmin(userid)
        if anyadmin is None:
            isany = await db.ReadUserByUserId(userid)
            if isany is None:
                await db.create_user(userid,event.sender.first_name,event.sender.username,0,0,10,0)
                isany = await db.ReadUserByUserId(userid)
                
            if isany[7] == 0:
                # try:
                #     user_obj = await client.get_participants('refferall_bo', filter=event.sender_id)
                #     if user_obj:
                        await event.respond(
                            ConstText.StartMsg.format(event.sender.first_name),
                            buttons=keys.key_start_user()
                        )
                        # return True
                # except Exception:
                #     await event.respond(
                #         "⚠️لطفا برای استفاده از خدمات ربات اول جوین چنل بشید",
                #         buttons=keys.key_join_ejbar())
                #     await event.delete()
                #     return False
        else:
            rolle = anyadmin[2]
            if rolle == 1: 
                await event.respond(
                    ConstText.StartMsg_sudo.format(event.sender.first_name),
                    buttons=keys.key_start_sudo()
                )
            elif rolle == 0:
                await event.respond(
                    ConstText.StartMsg_admin.format(event.sender.first_name),
                    buttons=keys.key_start_admin()
                )

    elif "/start" in text and text.replace("/start ", "").isdigit():
        uid = int(text.replace("/start ", ""))
        if uid != userid:
            await event.respond(
                ConstText.StartMsg.format(event.sender.first_name),
                buttons=keys.key_start_user()
            )
            isany = await db.ReadUserByUserId(userid)
            if isany is None:
                await db.create_user(userid,event.sender.first_name,event.sender.username,0,0,10,0)
                referrer = await db.ReadUserByUserId(uid)
                if referrer:
                    score = referrer[4] - 1
                    await db.UpdateScoreUser(uid, score)
                    referrer = await db.ReadUserByUserId(uid)

                    if referrer[5] == 0:
                        await client.send_message(
                            uid,
                            "هوووووورا شما 10نفر رو به ربات اضاف کردید🤩\n با ارسال این پیام به ادمین هدیه خود را دریافت کنید😎"
                        )
                    else:
                        await client.send_message(
                            uid,
                            ConstText.add_zir.format(referrer[5])
                        )
                        
# -------------------------------  user -------------------------------
                        
@client.on(events.NewMessage(pattern="افزایش موجودی 👛"))
async def update_card(event):
    userid = event.sender_id
    keyboard = keys.how_pay()
    await event.respond(ConstText.charg_acc,buttons=keyboard)

@client.on(events.NewMessage(pattern="💵 درگاه بانکی"))
async def pay_dargah(event):
    userid = event.sender_id
    global user_cach, user_step
    user_step[userid] = "cash"
    user_cach[userid] = {}
    
    keyboard = keys.cancel()
    await event.respond("💶 جهت افزایش موجودی حساب مبلغ مورد نظرخود را به تومان وارد نمایید:", buttons=keyboard)

@client.on(events.NewMessage(pattern="پرداخت مستقیم 📥"))
async def update_card(event):
    keyboard = keys.how_pay()
    await event.respond(ConstText.pay_card,buttons=keyboard)    
                  
@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def rule_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.rules
                        )
    
@client.on(events.NewMessage(pattern="سفارش استارت \\(زیر مجموعه\\) ⭐️"))
async def order_bot(event):
    
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.respond("هیچ رباتی در لیست وجود ندارد.")
        return
    key = keys.key_read_button_refferalbot(referal_list, page=1)
    await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)
    
@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def pagination_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.answer("هیچ داده‌ای برای نمایش وجود ندارد.", alert=True)
        return
    key = keys.key_read_button_refferalbot(referal_list, page=page)
    await event.edit("لیست ربات‌ها (صفحه {page})".format(page=page), buttons=key)

@client.on(events.NewMessage(pattern="اطلاع رسانی ها 📌"))
async def news_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.channel
                        )
    
@client.on(events.NewMessage(pattern="پشتیبانی ☎️"))
async def support_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.support
                        )
    
@client.on(events.NewMessage(pattern="اطلاعات حساب 👤"))
async def user_detail_bot(event: events.NewMessage.Event):
    userid = event.sender_id
    amount = await db.ReadWalletUser(userid)
    await client.send_message(
        userid,
        ConstText.detail.format(userid, amount[0])
    )

@client.on(events.NewMessage(pattern="انصراف ❌"))
async def backmenohandeler(event):
    global user_cach,user_step
    userid = event.sender.id
    await client.send_message(userid,"🌹")
    sudo = await db.ReadAdmin(userid)
    if sudo:
        keyboard = keys.key_start_sudo()
        await event.respond("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)
    user_cach.pop(userid)
    user_step.pop(userid)
    
@client.on(events.NewMessage(pattern="کنسل ❌"))
async def backmenohandeler(event):
    global user_cach,user_step
    userid = event.sender.id
    keyboard = keys.key_start_user()
    await event.respond("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)  
    user_cach.pop(userid)
    user_step.pop(userid)
    
@client.on(events.NewMessage(pattern="بازگشت 🔙"))
async def backmenotexthandeler(event):
    global user_cach,user_step
    userid = event.sender.id
    await client.send_message(userid,"🌹")
    sudo = await db.ReadAdmin(userid)
    if sudo:
        keyboard = keys.key_start_sudo()
        await event.respond("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        await event.respond("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    user_cach.pop(userid)
    user_step.pop(userid)

client.on(events.NewMessage(pattern="منو قبل 🔙"))
async def backmeno(event):
    global user_cach,user_step
    userid = event.sender.id
    await client.send_message(userid,"🌹")
    sudo = await db.ReadAdmin(userid)
    if sudo:
        keyboard = keys.refferal_key()
        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
    user_cach.pop(userid)
    user_step.pop(userid)
  
# -------------------------------  admin -------------------------------

@client.on(events.NewMessage(pattern="کلید رفرال 📍"))
async def update_card(event):
    keyboard = keys.refferal_key()
    await event.respond("یکی از موارد زیر را انتخاب کنید 🙏🏻",buttons=keyboard)

@client.on(events.NewMessage(pattern="^پیام همگانی ✉️$"))
async def send_message_channel(event: events.NewMessage.Event):
    try:
        global user_step, user_cach
        userid = event.sender_id

        AnyAdmin = await db.ReadAdmin(userid)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(userid)
            if AcsessType[2] == 1:
                user_cach[userid] = {}
                keyboard = keys.Back_Reply()
                await event.respond("لطفاً متن پیام همگانی را وارد کنید 🙏🏻",buttons=keyboard)
                user_step[userid] = "awaiting_message_text"
            else:
                await event.respond(ConstText.noacsess)
        else:
            await event.respond(ConstText.noacsess)

    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage())
async def handle_send_messege(event: events.NewMessage.Event):
    global user_step, user_cach
    userid = event.sender_id
    if userid in user_step:
        step = user_step[userid]
        message_text = event.text
        if step == "awaiting_message_text" and message_text != "پیام همگانی ✉️":
            user_cach[userid]["message_text"] = message_text
            users = await db.read_users()
            Msgg = await event.respond("در حال ارسال پیام به کاربران⏳")
            for user in users:
                try:
                    await client.send_message(int(user[1]), message_text)
                except Exception as user_error:
                    print(f"خطا در ارسال پیام به کاربر {user[1]}: {user_error}")

            await Msgg.delete()
            keyboard = keys.key_start_sudo()
            await event.respond("پیام مورد نظر با موفقیت ارسال شد✅",buttons=keyboard)
            user_step.pop(userid, None)
            user_cach.pop(userid, None)
            
@client.on(events.NewMessage(pattern="➕ ساخت کلید 🔑"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step,user_cach
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    user_step[user_id] = "name" 
    user_cach[user_id] = {}
    keyboard = keys.Back_menu()
    await event.respond("لطفاً نام ربات را وارد کنید 🙏🏻",buttons=keyboard)

@client.on(events.NewMessage(pattern="^شارژ حساب کاربر ➕$"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    userid = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(userid)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(userid)
            if AcsessType[2] == 1:

                user_cach[userid] = {}
                keyboard = keys.cancel() 
                await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[userid] = "user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="^مشتریان و گزارشات 📎$"))
async def log(event: events.NewMessage.Event):
    try:
        log = await db.read_users()

        # باز کردن فایل با encoding 'utf-8'
        with open("log.txt", "a", encoding="utf-8") as wp:
            for i in log:
                if len(i) >= 8:
                    wp.write(f"ID: {i[0]} \\ USERID: {i[1]} \\ Name: {i[2]} \\ Username: {i[3]} \\ WALLET: {i[4]}\n")
                    wp.write(f"REFFERAL: {i[5]} \\ Score: {i[6]} \\ BLOCK: {i[7]}\n\n")
                else:
                    print(f"Error: Tuple has fewer than 8 elements: {i}")

        if os.path.exists("log.txt"):
            await client.send_file(
                event.chat_id,
                "log.txt",
                caption="لیست گزارشات"
            )
            os.remove("log.txt")
        else:
            await event.respond("فایل گزارشات پیدا نشد.")
    
    except Exception as e:
        print(f"Error: {e}")
        await event.respond("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

@client.on(events.NewMessage(pattern="^آپدیت قیمت 📌$"))
async def update_balnce(event):
    user_id = event.sender_id
    global user_step, user_cach
    
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    
    user_step[user_id] = "namee" 
    user_cach[user_id] = {}
    keyboard = keys.Back_menu()
    await event.respond("لطفاً نام ربات را وارد کنید 😊",buttons=keyboard)

@client.on(events.NewMessage(pattern="➖ حذف کلید 🔑"))
async def delete_refferal_bot(event):
    user_id = event.sender_id
    global user_step, user_cach
    
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    
    user_step[user_id] = "nam" 
    user_cach[user_id] = {}
    keyboard = keys.Back_menu()
    await event.respond("لطفاً نام ربات را وارد کنید 😊",buttons=keyboard)
    
# @client.on(events.NewMessage())
# async def delete_refferal_bot(event):
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]
    nam = event.text

    if current_step == "nam" and nam != "➖ حذف کلید 🔑":
        user_cach[user_id]["nam"] = nam
        is_valid = await db.read_referrabot_name(user_cach[user_id]["nam"])
        if is_valid:
            if user_cach[user_id]["nam"]  == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
            await db.delete_referrabot(str(user_cach[user_id]["nam"]))
            keyboard = keys.refferal_key()
            await event.respond("کلید با موفقیت حذف شد ✅",buttons=keyboard)
            user_step.pop(user_id)
            user_cach.pop(user_id)
        
        else:
            await event.respond("ربات با این اسم وجود ندارد 🔴")
        
@client.on(events.NewMessage(pattern="♾️ نمایش کلید ها 🔑"))
async def show_ref_bot(event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        referal_list = await db.read_referrabots()
        if not referal_list:
            await event.respond("هیچ رباتی در لیست وجود ندارد 🔴")
            return
        key = keys.key_read_button_refferalbot(referal_list, page=1)
        await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)
    else:
        key = keys.key_start_sudo()
        await event.respond("شما به این بخش دسترسی ندارید ⚠️", buttons=key)
    
@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def show_ref_bot_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.answer("هیچ داده‌ای برای نمایش وجود ندارد ❗️", alert=True)
        return
    key = keys.key_read_button_refferalbot(referal_list, page=page)
    await event.edit("لیست ربات‌ها (صفحه {page}) 👇🏻".format(page=page), buttons=key)
    
# -------------------------------  callback -------------------------------
            
user_cach = {}
@client.on(events.CallbackQuery)
async def callback_handler(event):
    userid = event.sender.id
    global user_step, user_cach
    data = event.data.decode()
    
    if "at_" in data:
        separated = data.split(',')
        at=separated[0].replace("at_","")
        amount = separated[1].replace("am_","")
        if at and amount: 
            response = pay.check_status_payment(amount,at)
            if "error not active" in response:
                await event.respond("هنوز پرداخت انجام نشده است ❗️") 
    
            elif response == 100 or response == 101:
                
                f = await db.ReadWalletUser(userid)
                await db.UpdateWalletUser(int(userid), int(amount)+ f[0])
                buttons = keys.key_start_user()
                await event.edit("پرداخت با موفقیت انجام شد ✅", buttons=buttons)
                
            else:
                buttons=keys.key_start_user()
                await event.edit("پرداخت انجام نشد ❌",buttons=buttons)

    if "back" in data:
        keyboard=keys.Back_Reply()
        await event.edit("به منو اصلی بازگشتید 🔙", buttons=keyboard)
      
# -------------------------------  on messege -------------------------------

async def run():
    await db.create_database()
    
    for i in [6785692975, 400395713]:
        isany = await db.ReadAdmin(i)
        if isany is None:
            await db.create_accesstype(i, 1, 1, 1, 1, 1)
            ra = await db.ReadAccessTypesByUserId(i)
            try:
                user = await client.get_entity(i) 
                fname = user.first_name
                if ra:
                    await db.create_admin(i, 1, ra[0], fname)
            except ValueError:
                print(f"Could not find user with ID {i}")
                continue


    print("Run")
    await client.run_until_disconnected()

client.loop.run_until_complete(run())