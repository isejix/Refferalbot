from telethon import TelegramClient, events
import keys
import db
import ConstText
from socks import SOCKS5, SOCKS4, HTTP
import os
from asyncio import sleep
import pay
import  re
import zipfile
import shutil
import account
import random
import string
from datetime import date
from telethon.tl.types import SendMessageTypingAction
import asyncio
import sqlite3
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import jdatetime


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
user_cach={}

async def is_user_in_channel(user_id):
    channel_link = 'https://t.me/refferall_bo'
    offset = 0
    limit = 200
    my_filter = ChannelParticipantsSearch('')
    try:
        while True:
            participants = await client(
                GetParticipantsRequest(
                    channel=channel_link,
                    filter=my_filter,
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )
            for user in participants.users:
                if user.id == user_id:
                    return True
            if not participants.users:
                break
            offset += limit
        return False
    except Exception as e:
        return False

async def log_to_channel(event, action=None):
    try:
        log_channel_id = 'https://t.me/log_reffelalbot'   
        user_id = event.sender_id
        username = f"@{event.sender.username}" if event.sender.username else "بدون نام کاربری"
        message = f"📝 **ثبت لاگ**\n"
        message += f"- کاربر: [{user_id}](tg://user?id={user_id})\n"
        message += f"- نام کاربری: {username}\n"
        if action:
            message += f"- اکشن: {action}\n"
        if event.text:
            message += f"- پیام: {event.text}\n"
        await client.send_message(log_channel_id, message)
        
        pass
    
    except Exception as e:
        print(f"خطا در ارسال لاگ: {e}")

def generate_discount_code():
    length = 10
    characters = string.ascii_letters + string.digits
    discount_code = "".join(random.choices(characters, k=length))
    return discount_code

def get_persian_date():
    today = jdatetime.date.today()
    return today.strftime("%Y/%m/%d") 

def check_date(user_date):

    today = jdatetime.date.today()
    try:
        year, month, day = map(int, user_date.split('/'))
        user_date_obj = jdatetime.date(year, month, day)
    except ValueError:
        return "فرمت تاریخ ارسالی صحیح نیست. لطفاً از فرمت YYYY/MM/DD استفاده کنید."

    days_difference = (user_date_obj - today).days

    if days_difference == 0:
        return True
    else:
        return False
    
def apply_discount(price, discount_percentage):
    try:
        # اطمینان از اینکه قیمت و درصد تخفیف معتبر هستند
        if price <= 0 or discount_percentage < 0:
            return "قیمت باید مثبت و درصد تخفیف نباید منفی باشد."
        if discount_percentage > 100:
            return "درصد تخفیف نمی‌تواند بیشتر از 100 باشد."
        
        # محاسبه قیمت تخفیف‌یافته
        discounted_price = price - (price * discount_percentage / 100)
        return int(discounted_price)  # تبدیل به عدد صحیح (بدون اعشار)
    except Exception as e:
        return f"خطایی رخ داده است: {e}"



# -------------------------------  start -------------------------------

@client.on(events.NewMessage(pattern="/start"))
async def start_bot(event):
    user_id = event.sender_id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    anyadmin = await db.ReadAdmin(user_id)
    if anyadmin is None:
        isany = await db.ReadUserByUserId(user_id)
        if isany is None:
            await db.create_user(user_id,event.sender.first_name,event.sender.username,0,0,10,0)
            isany = await db.ReadUserByUserId(user_id)
        try:    
            if isany[7] == 0:
                try:
                    user = await is_user_in_channel(user_id)
                    if user:
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply(
                                ConstText.StartMsg.format(event.sender.first_name),
                                buttons=keys.key_start_user()
                            )
                        await log_to_channel(event, action="کاربر در کانال عضو است و پیام خوش‌آمد ارسال شد.")
                        return True
                    else:
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await client.send_message(
                                user_id,
                                ConstText.join_channel,
                                buttons=keys.key_join_ejbar(),
                                parse_mode="HTML"
                            )
                        await log_to_channel(event, action="کاربر در کانال عضو نیست و پیام عضویت اجباری ارسال شد.")
                        return False
                except Exception as e:
                    await log_to_channel(event, action=f"خطا در بررسی عضویت کاربر: {e}")
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await client.send_message(
                            user_id,
                            ConstText.join_channel,
                            buttons=keys.key_join_ejbar(),
                            parse_mode="HTML"
                        )
                    return False
            else:
                await event.reply("شما از دسترسی به ربات محدود شده اید 🚫",buttons=keys.key_id_suppoort())
        except Exception as e:
            await log_to_channel(event, action=f"خطای کلی: {e}")

    else:
        rolle = anyadmin[2]
        if rolle == 1: 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply(
                    ConstText.StartMsg_sudo.format(event.sender.first_name),
                    buttons=keys.key_start_sudo()
                )

# -------------------------------  on meessege -------------------------------

async def move_file(src_file, dest_folder):
    if os.path.exists(src_file):
        os.makedirs(dest_folder, exist_ok=True)  # اگر پوشه مقصد وجود نداشت، ایجاد می‌شود
        dest_file = os.path.join(dest_folder, os.path.basename(src_file))
        shutil.move(src_file, dest_file)
    else:
        print(f"فایل {src_file} وجود ندارد.")
        
@client.on(events.NewMessage())
async def process(event):
    global user_cach,user_step

    try:
        user_id = event.sender_id
        
        if user_id not in user_step:
            return

        current_step = user_step[user_id]
        
        if event.text == "منو قبل 🔙":
            if user_id in user_step:
                admin = db.ReadAdmin(user_id)
                if admin:
                    key = keys.refferal_key()
                    await event.reply(buttons = key)
                user_cach.pop(user_id)
                user_step.pop(user_id)
        
        if event.text == "انصراف ❌":
            admin = db.ReadAdmin(user_id)
            if admin:
                key = keys.key_start_sudo()
                await event.reply(buttons = key)
            else:
                key = keys.key_start_user()
                await event.reply(buttons = key)
            user_cach.pop(user_id)
            user_step.pop(user_id)
            
        if event.text == "/start":
            admin = db.ReadAdmin(user_id)
            if admin:
                key = keys.key_start_sudo()
                await event.reply("منو اصلی ✔️",buttons = key)
            else:
                key = keys.key_start_user()
                await event.reply("منو اصلی ✔️",buttons = key)
            user_cach.pop(user_id)
            user_step.pop(user_id)

        if current_step == "discount_":
            nama = user_cach[user_id]["read_balance_"]
            
            x = event.text
            try:
                
                if x:
                    discount_ = await db.read_discount(x)
                    balanc = int(user_cach[user_id]['lastbalance'])
                    
                    toda = get_persian_date()
                    if discount_:
                            dates = discount_[2]
                            if  dates != toda:
                                di = discount_[5]
                                dis = apply_discount(balanc,di)
                                name = user_cach[user_id]["name"]
                                usname = user_cach[user_id]["usname"]
                                ref = user_cach[user_id]["ref"]
                                price = user_cach[user_id]["price"]
                                key = keys.key_order_ref(balance=dis,namee=nama,count=int(user_cach[user_id]['i'].replace("do_",'').replace("neg_","").replace("plus_","")))
                                await client.send_message(user_id,ConstText.neworder.format(name, usname, ref, None,price ),buttons=key,parse_mode="HTML")
                                user_cach.pop(user_id)
                                user_step.pop(user_id)
                                user_cach[user_id] = {"discount_balance":dis}
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")
           
        if current_step == "cash":
            try:
                if event.text.isdigit():
                    cash = float(event.text)
                    user_cach[user_id]["cash"] = cash
                    
                    if 1000 <= user_cach[user_id]["cash"] <= 5000000:
                        payment_url = pay.link_payment(user_cach[user_id]["cash"])
                        match = re.search(r'/StartPay/([^/]+)', payment_url)
                        await event.respond("⏳", buttons=keys.key_start_user())
                        
                        if match:
                            code = match.group(1)
                            async with client.action(event.chat_id, 'typing'):
                                await asyncio.sleep(0.3)
                                await event.reply(
                                    f"💳 فاکتور افزایش موجودی به مبلغ {user_cach[user_id]['cash']} تومان صادر گردید.\n"
                                    "👈 درصورتی که مورد تاییدتان است با انتخاب یکی از گزینه های زیر پرداخت خود را انجام دهید",
                                    buttons=keys.pay_dargah(payment_url, code, user_cach[user_id]['cash'])
                                )
                                await event.respond("🛍 فاکتور شما با موفقیت ایجاد شد.", buttons=keys.cancel())
                                await log_to_channel(
                                    event, 
                                    action=f"فاکتور پرداخت به مبلغ {user_cach[user_id]['cash']} تومان صادر شد. کد پرداخت: {code}"
                                )
                                user_step.pop(user_id)
                                user_cach.pop(user_id)
                        else:
                            await log_to_channel(
                                event, 
                                action=f"خطا در استخراج کد پرداخت از لینک: {payment_url}"
                            )
                    else:
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await client.send_message(
                                user_id, 
                                "مبلغ شما کمتر از میزان تعیین شده برای پرداخت است لطفا مبلغ درخواست را افزایش دهید و دوباره تلاش کنید 🌹"
                            )
                            await log_to_channel(
                                event, 
                                action=f"مبلغ واردشده نامعتبر: {user_cach[user_id]['cash']}. (باید بین 1000 تا 5000000 باشد)"
                            )
                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
                        await log_to_channel(
                            event, 
                            action="کاربر مقدار غیرعددی وارد کرد.")
        
            except Exception as e:
                await log_to_channel(event,str(e))
                
        nam = event.text

        if current_step == "nam" and nam != "➖ حذف کلید 🔑":
            try:
                await log_to_channel(
                            event,
                            action="کاربر روی دکمه ➖ حذف کلید 🔑 کلیک کرد "
                        )
                user_cach[user_id]["nam"] = nam
                is_valid = await db.read_referrabot_name(user_cach[user_id]["nam"])
                if is_valid:
                    if user_cach[user_id]["nam"] == "منو قبل 🔙":
                        user_step.pop(user_id)
                        user_cach.pop(user_id)
                        keyboard = keys.refferal_key()
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                        await log_to_channel(
                            event,
                            action="کاربر به منوی قبلی بازگشت."
                        )
                        return
                    
                    await db.delete_referrabot(str(user_cach[user_id]["nam"]))
                    keyboard = keys.refferal_key()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("کلید با موفقیت حذف شد ✅", buttons=keyboard)
                    await log_to_channel(
                        event,
                        action=f"کلید {user_cach[user_id]['nam']} با موفقیت حذف شد."
                    )
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                else:
                    await event.respond("ربات با این یوزرنیم وجود ندارد 🔴")
                    await log_to_channel(
                        event,
                        action=f"کاربر تلاش کرد کلید ناموجود {user_cach[user_id]['nam']} را حذف کند."
                    )
            except Exception as e:
                await log_to_channel(event,str(e))
            
        namee = event.text

        if current_step == "namee" and namee != "آپدیت قیمت 📌":
            try:
                user_cach[user_id]["namee"] = namee
                if user_cach[user_id]["namee"]  == "منو قبل 🔙":
                    await log_to_channel(event, "کاربر روی دکمه منو قبل 🔙 کلیک کرد")
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                        await log_to_channel(event, "کاربر به منو قبل بازگشت")
                    return
                if namee.isdigit():
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("یوزرنیم اشتباه وارد شده است 🔴")
                        await log_to_channel(event, "کاربر یوزرنیم اشتباه وارد کرد")
                    
                    
                user_step[user_id] = "balancee"
                is_valid = await db.read_referrabot_name(user_cach[user_id]["namee"])
                if is_valid:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("لطفاً قیمت جدید را به تومان وارد کنید 🙏🏻")
                        await log_to_channel(event, "کاربر قیمت جدید رو وارد کرد")
                
                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply(" این یوزرنیم در دیتابیس وجود ندارد 🔴")
                        await log_to_channel(event, "کاربر یوزرنیم اشتباه وارد کرد")
            except Exception as e:
                await log_to_channel(event,str(e))  
                
        if current_step == "balancee":
            try:
                if event.text.isdigit():
                    try:
                        balancee = float(event.text)
                        user_cach[user_id]["balancee"] = balancee


                        user_step[user_id] = "completed"
                        await db.Updatebalancereferal(user_cach[user_id]['namee'], user_cach[user_id]['balancee'])

                        keyboard = keys.refferal_key()
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await client.send_message(user_id,
f"""<blockquote>تغییر قیمت 💰</blockquote>
قیمت ربات با موفقیت آپدیت شد ✅\n
🤖 نام: {user_cach[user_id]['namee']} 📎\n
💰 قیمت جدید: {int(float(balancee))}

"""
                                ,
                                buttons=keyboard,
                                parse_mode="HTML"
                            )

                            await log_to_channel(
                                event,
                                action=f"اطلاعات ربات ذخیره شد: نام={user_cach[user_id]['name']}\nقیمت={balance}"
                            )

                            user_step.pop(user_id)
                            user_cach.pop(user_id)
                    except ValueError as e:

                        await log_to_channel(
                            event,
                            action=f"خطا در تبدیل ورودی قیمت به عدد: {e}"
                        )

                elif event.text == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)

                    await log_to_channel(
                        event,
                        action="کاربر به منوی قبلی بازگشت."
                    )
                    return

                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("لطفاً قیمت را به‌صورت عدد وارد کنید.")


                    await log_to_channel(
                        event,
                        action="کاربر وارد عدد نامعتبر شد برای قیمت."
                    )
            except Exception as e:

                await log_to_channel(
                    event,
                    action=f"خطا در پردازش قیمت: {e}"
                ) 
        
        name = event.text
        
        if current_step == "name" and name != "➕ ساخت کلید 🔑":
            try:
                user_id = event.sender_id
                user_cach[user_id]["name"] = name
                user_step[user_id] = "username"
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await client.send_message(user_id,ConstText.n,parse_mode="HTML")
        
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")
            
        if current_step == "username":
            try:
                user_id = event.sender_id
                username = event.text
                pattern = r"(?:https://t\.me/|@)([a-zA-Z0-9_]+)"
                await log_to_channel(event, action="ثبت یوزرنیم کاربر")
                if re.match(pattern, username):
                    x = re.findall(pattern, username)
                    link = f"https://t.me/{x[0]}" 
                    user_cach[user_id]["username"] = link
                    
                    user_step[user_id] = "balance"
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("لطفاً قیمت را به تومان وارد کنید 🙏🏻")
                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await client.send_message(user_id,ConstText.x,parse_mode="HTML")
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش یوزرنیم: {e}")

        if current_step == "balance":
            try:
                if event.text.isdigit():
                    try:
                        balance = float(event.text)
                        user_cach[user_id]["balance"] = balance

                        user_step[user_id] = "completed"
                        await db.create_referrabot(user_cach[user_id]['name'], user_cach[user_id]['username'], user_cach[user_id]['balance'])

                        keyboard = keys.refferal_key()
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await client.send_message(user_id,
f"""<blockquote>ثبت ربات جدید 🤖</blockquote>
ربات با موفقیت ایجاد شد ✅\n
🤖 نام: {user_cach[user_id]['name']}\n
💰 قیمت : {int(float(balance))}\n
🆔 یوزرنیم : {user_cach[user_id]['username']}
"""
                                ,
                                buttons=keyboard,
                                parse_mode="HTML"
                            )

                        await log_to_channel(
                            event,
                            action=f"اطلاعات ربات ذخیره شد: نام={user_cach[user_id]['name']}, یوزرنیم={user_cach[user_id]['username']}, قیمت={balance}"
                        )

                        user_step.pop(user_id)
                        user_cach.pop(user_id)
                    except ValueError as e:

                        await log_to_channel(
                            event,
                            action=f"خطا در تبدیل ورودی قیمت به عدد: {e}"
                        )

                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("لطفاً قیمت را به‌صورت عدد وارد کنید.")


                    await log_to_channel(
                        event,
                        action="کاربر وارد عدد نامعتبر شد برای قیمت."
                    )
            except Exception as e:

                await log_to_channel(
                    event,
                    action=f"خطا در پردازش قیمت: {e}"
                )
                
        if current_step == "user_id":
            if event.text.isdigit():
                try:
                    user_id_input = event.text.replace('`','')
                    if user_id_input.isdigit():
                        user_cach[user_id] = {"user_id": user_id_input}
                        user_step[user_id] = "charge_amount"
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply("💶 جهت افزایش موجودی حساب مبلغ مورد نظر خود را به تومان وارد نمایید:")

                        await log_to_channel(
                            event,
                            action=f"شناسه کاربری {user_id_input} وارد شد و کاربر آماده شارژ موجودی است."
                        )

                    else:
                        await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")

                        await log_to_channel(
                            event,
                            action=f"شناسه کاربری وارد شده نامعتبر بود: {user_id_input}"
                        )
                except Exception as e:
                    await log_to_channel(
                            event,
                            action=e
                        )
                
            else:
                await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")
        
                await log_to_channel(
                    event,
                    action="شناسه کاربری وارد شده معتبر نیست."
                )
        
        if current_step == "charge_amount":
            try:
                charge_amount = event.text
                if charge_amount.isdigit():
                    charge_amount = int(charge_amount)
                    stored_user_id = user_cach[user_id]["user_id"]

                    try:
                        current_balance = await db.ReadWalletUser(stored_user_id)
                        if current_balance:
                            new_balance = current_balance[0] + charge_amount
                            await db.UpdateWalletUser(stored_user_id, new_balance)

                            keyboard = keys.key_charg_user()
                            async with client.action(event.chat_id, 'typing'):
                                await asyncio.sleep(0.3)
                                await event.reply(f"مقدار {charge_amount} تومان حساب کاربر {stored_user_id} با موفقیت  شارژ شد ✅", buttons=keyboard)
                            await client.send_message(int(stored_user_id), f"مقدار {charge_amount} حساب شما شارژ شد ✅")


                            await log_to_channel(
                                event,
                                action=f"مقدار {charge_amount} تومان به حساب کاربر {stored_user_id} اضافه شد."
                            )

                            user_step.pop(user_id)
                            user_cach.pop(user_id)
                        else:
                            await log_to_channel(
                                event,
                                action=f"خطا در دریافت موجودی برای شناسه کاربری {stored_user_id}."
                            )
                    except Exception as e:
                        await log_to_channel(
                            event,
                            action=f"خطا در بروزرسانی موجودی حساب کاربر {stored_user_id}: {str(e)}"
                        )
                else:
                    await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")

                    await log_to_channel(
                        event,
                        action=f"کاربر مقدار نامعتبری برای شارژ وارد کرد: {charge_amount}"
                    )

            except Exception as e:

                await log_to_channel(
                    event,
                    action=f"خطای کلی: {str(e)}"
                )

        if current_step == "get_session":
            try:
                file_name = event.document.mime_type
                if "zip" in file_name:
                    folder_path = "./newfile"
                    os.makedirs(folder_path, exist_ok=True)
                    path = await event.download_media(folder_path)
                    
                    try:
                        with zipfile.ZipFile(path, 'r') as zip_ref:
                            zip_files = zip_ref.namelist()
                            session_files = [file for file in zip_files if file.endswith('.session')]

                            if not session_files:
                                await event.reply("هیچ فایل سشن (.session) درون فایل zip یافت نشد.")

                                await log_to_channel(event, action="هیچ فایل سشن در فایل zip یافت نشد.")
                                return

                            i = 0
                            dest_folder = "./session"
                            os.makedirs(dest_folder, exist_ok=True)

                            for file in session_files:
                                zip_ref.extract(file, folder_path)
                                src_file = os.path.join(folder_path, file)

                                try:
                                    await move_file(src_file, dest_folder)
                                    i += 1
                                except Exception as e:
                                    await log_to_channel(event, action=f"خطا در جابجایی فایل {file}: {e}")
                                    continue

                            if i > 0:
                                dest_folder = "./session"
                                if os.path.exists(dest_folder):
                                    files = os.listdir(dest_folder)
                                    if files:
                                        healthy_count = 0 
                                        broken_count = 0  

                                        for file in files:
                                            file_b = os.path.join(dest_folder, file) 
                                            check_stat = await account.check_status_sessions(file) 

                                            if check_stat: 
                                                healthy_count += 1
                                                today = date.today()
                                                to_day = today.strftime("%Y/%m/%d")
                                                phone_number = file.replace(".session", "") 

                                                try:
                                                    await db.create_account(int(phone_number), to_day)
                                                except sqlite3.OperationalError as e:
                                                    await log_to_channel(event, action=f"خطای پایگاه داده هنگام ثبت حساب برای {phone_number}: {e}")
                                                    async with client.action(event.chat_id, 'typing'):
                                                        await asyncio.sleep(0.3)
                                                    continue
                                            else:  
                                                broken_count += 1
                                                os.remove(file_b)  

                                        async with client.action(event.chat_id, 'typing'):
                                            await asyncio.sleep(0.3)
                                            await event.reply(
                                                f"تعداد {healthy_count} سشن سالم به اکانت‌ها اضافه شد ⭐️\n"
                                                f"تعداد {broken_count} سشن خراب است."
                                                ,buttons = keys.key_start_sudo()
                                            )
                                            user_cach.pop(user_id)
                                            user_step.pop(user_id)
                                        await log_to_channel(
                                            event, 
                                            action=f"{healthy_count} سشن سالم و {broken_count} سشن خراب."
                                        )
                                    else:
                                        async with client.action(event.chat_id, 'typing'):
                                            await asyncio.sleep(0.3)
                                        await log_to_channel(event, action="پوشه سشن خالی است.")
                                else:
                                    async with client.action(event.chat_id, 'typing'):
                                        await asyncio.sleep(0.3)
                                    await log_to_channel(event, action=f"مسیر '{folder_path}' وجود ندارد.")
                            else:
                                await log_to_channel(event, action="هیچ فایلی از فایل zip استخراج نشد.")
                        
                    except zipfile.BadZipFile:
                        await log_to_channel(event, action="فایل zip خراب است.")
                    
                    finally:
           
                        if os.path.exists(path):
                            os.remove(path)
                        if os.path.exists(folder_path):
                            shutil.rmtree(folder_path)
                        user_cach.pop(user_id)
                        user_step.pop(user_id)

                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("فرمت فایل اشتباه است. لطفاً یک فایل zip ارسال نمایید.")
                    await log_to_channel(event, action="فرمت فایل ارسال شده اشتباه است. (نبودن zip)")

            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش فایل سشن: {str(e)}")

        if current_step == "user_id_neg":
            if event.text.isdigit():
                user_id_input = event.text.replace('`','')
                try:
                    if user_id_input.isdigit(): 
                        user_cach[user_id] = {"user_id": user_id_input}
                        user_step[user_id] = "kasr_charge_amount" 
                        await log_to_channel(
                            event,
                            action=f"شناسه کاربری {user_id_input} وارد شد."
                        )

                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply("چقدر می‌خواهید از حساب کاربر را کسر کنید؟")
                    else:
                        await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")
            
                        await log_to_channel(
                            event,
                            action="شناسه کاربری وارد شده معتبر نیست."
                        )
                except Exception as e:
                    await log_to_channel(
                        event,
                        action=f"خطا در وارد کردن شناسه کاربری: {str(e)}"
                    )
            else:
                        await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")
            
                        await log_to_channel(
                            event,
                            action="شناسه کاربری وارد شده معتبر نیست."
                        )
            
        if current_step == "kasr_charge_amount" and not current_step == "user_id_neg" : 
            if event.text.isdigit(): 
                try:
                    charge_amount = event.text.replace('`','')
                    if charge_amount.isdigit():
                        charge_amount = int(charge_amount)
                        stored_user_id = user_cach[user_id]["user_id"]
                        stored_user_id = stored_user_id.replace('`','')
                        current_balance = await db.ReadWalletUser(stored_user_id)
                        if current_balance:
                            new_balance = current_balance[0] - charge_amount
                            if new_balance < 0:
                                await event.reply("موجودی کافی برای کسر این مبلغ وجود ندارد.")
            
                                await log_to_channel(
                                    event,
                                    action=f"موجودی ناکافی برای کسر {charge_amount} از حساب کاربر {stored_user_id}."
                                )
                                user_cach.pop(user_id)
                                user_step.pop(user_id)
                                return
                            await db.UpdateWalletUser(stored_user_id, new_balance)
                            keyboard = keys.key_charg_user()
                            async with client.action(event.chat_id, 'typing'):
                                await asyncio.sleep(0.3)
                                await event.reply(f"مقدار {charge_amount} تومان حساب کاربر {stored_user_id} با موفقیت  کسر شد ✅", buttons=keyboard)
                            
            
                            await client.send_message(int(stored_user_id), f"مقدار {charge_amount} از حساب شما کسر شد ✅")

                    
                            await log_to_channel(
                                event,
                                action=f"مقدار {charge_amount} از حساب کاربر {stored_user_id} با موفقیت کسر شد."
                            )

                            user_step.pop(user_id)
                            user_cach.pop(user_id)
                        else:
                            await event.reply("خطا در دریافت موجودی کاربر. لطفا دوباره تلاش کنید.")
                    
                            await log_to_channel(
                                event,
                                action=f"خطا در دریافت موجودی برای کاربر {stored_user_id}."
                            )
                    else:
                        await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")
                        
                        await log_to_channel(
                            event,
                            action="کاربر مقدار غیر عددی وارد کرد."
                        )
                except Exception as e:
                    await log_to_channel(
                        event,
                        action=f"خطا در پردازش کسر مبلغ: {str(e)}"
                    )
            else:
                        await log_to_channel(
                            event,
                            action="شناسه کاربری وارد شده معتبر نیست."
                        )

        if current_step == "user_delete":
            user_id_input = event.text
            
            try:
                
                if user_id_input.isdigit():
                    user_cach[user_id] = {"user": user_id_input}
                    await db.delete_user(user_cach[user_id]["user"])
                    keyboard = keys.key_charg_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond(f"حساب کاربری {user_cach[user_id]['user']} با موفقیت حذف شد✅", buttons=keyboard)
                    
                    await log_to_channel(
                        event,
                        action=f"حساب کاربری {user_cach[user_id]['user']} با موفقیت حذف شد."
                    )
                    user_step.pop(user_id)
                    user_cach.pop(user_id)

                else:
               
                    await event.respond("شناسه کاربری وارد شده معتبر نیست. لطفاً یک شناسه عددی وارد کنید.")
                    
             
                    await log_to_channel(
                        event,
                        action="کاربر شناسه غیر عددی وارد کرد."
                    )

            except Exception as e:
                await log_to_channel(
                    event,
                    action=f"خطا در حذف حساب کاربری {user_cach[user_id]['user']}: {str(e)}"
                )

        if current_step == "user_wallet_delete":
            user_id_input = event.text
            try:
                
                if user_id_input.isdigit():
                    user_cach[user_id] = {"user": user_id_input}
                    await db.delete_wallet_user(user_cach[user_id]["user"])
                    keyboard = keys.key_charg_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("حساب شارژ کاربر با موفقیت حذف شد✅", buttons=keyboard)
                
                    await log_to_channel(
                        event,
                        action=f"حساب شارژ کاربر با شناسه {user_cach[user_id]['user']} با موفقیت حذف شد."
                    )
             
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                else:
                    await event.respond("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")

            except Exception as e:
                await log_to_channel(
                    event,
                    action=f"خطا در حذف حساب شارژ کاربر با شناسه {user_id_input}. خطا: {e}"
                )

        if current_step == "block_user_id":
            user = event.text
            try:
                if user.isdigit():
                    user_cach[user_id]={"block_user_id" : user}
                    await db.blockN_User(user_cach[user_id]["block_user_id"], 1) 
                    keyboard = keys.key_charg_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("حساب کاربر با موفقیت مسدود شد 🔴", buttons=keyboard)   
          
                    await log_to_channel(
                        event,
                        action=f"حساب کاربر با شناسه {user} با موفقیت مسدود شد."
                    )
                    user_cach.pop(user_id)
                    user_step.pop(user_id)
                else:

                    await event.respond("شناسه کاربری وارد شده معتبر نیست. لطفا شناسه عددی وارد کنید.") 
            except Exception as e:
           
                await log_to_channel(
                    event,
                    action=f"خطا در مسدود کردن حساب کاربر با شناسه {user_id}. خطا: {str(e)}"
                )
                
        if current_step == "unblock_user_id":
            try:
                user_i = event.text
                if user_i.isdigit(): 
                    user_cach[user_id] = {"unblock_user_id" : user_i}
                    await db.blockN_User(user_cach[user_id]["unblock_user_id"], 0)    
                    keyboard = keys.key_charg_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("حساب کاربر با موفقیت رفع مسدودیت شد 🟢", buttons=keyboard) 

                    await log_to_channel(
                        event,
                        action=f"حساب کاربر با شناسه {user_id} با موفقیت رفع مسدودیت شد."
                    )
                    user_cach.pop(user_id)
                    user_step.pop(user_id)   
                else:
                    await event.respond("شناسه کاربری وارد شده معتبر نیست. لطفاً یک شناسه عددی وارد کنید.")  
            except Exception as e:

                await log_to_channel(
                    event,
                    action=f"خطا در فرآیند رفع مسدودیت کاربر با شناسه {user_i}: {str(e)}"
                ) 

        if current_step == "del_discount":
            try:
                del_discount = event.text
                user_cach[user_id]["del_discount"] = del_discount
                del_discount = user_cach[user_id]["del_discount"]
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    inus = await db.read_discount(del_discount)
                    if inus:
                        await db.delete_discount(del_discount)
                        await client.send_message(user_id,ConstText.del_discount,buttons=keys.key_discouny(),parse_mode="HTML")
                        user_cach.pop(user_id)
                        user_step.pop(user_id)
                    else:
                        await event.reply("مقدار ورودی اشتباه است ❗️")
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")

        if current_step == "discount":
            try:
                discount = event.text
                if discount.isdigit():
                    if int(discount) < 5:
                        await event.reply("درصد تخفیف باید بیشتر از ۵ درصد باشد !")
                    elif int(discount) > 90:
                        await event.reply("درصد تخفیف باید کمتر از ۹۰ درصد باشد !")

                    else:
                        user_cach[user_id]["discount"] = discount
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            toda = get_persian_date()
                            await client.send_message(user_id,ConstText.d.format(toda),parse_mode="HTML")
                        user_step[user_id] = "dateexpire"
                else:
                    await event.reply("مقدار ورودی اشتباه است لطفا عدد به عنوان مقدار وارد کنید ❗️")
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")
            
        if current_step == "dateexpire":
            try:
                dateexpire = event.text
                if dateexpire:
                    user_cach[user_id]["dateexpire"] = dateexpire
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply("تعداد استفاده کد تخفیف را وارد کنید 🙏🏻")
                    user_step[user_id] = "countallow"
                else:
                    await event.reply("مقدار ورودی اشتباه است لطفا به مقدار دهی تاریخ خود توجه کنید ❗️")
                    
            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")
        
        if current_step == "countallow":
            try:
                countallow = event.text
                if countallow.isdigit():
                    user_cach[user_id]["countallow"] = countallow
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        code = generate_discount_code()
                        discount = user_cach[user_id]["discount"]
                        dateexpire = user_cach[user_id]["dateexpire"] 
                        await db.create_discount(code,dateexpire,countallow,countallow,discount)
                        await client.send_message(user_id,ConstText.discount.format(code,dateexpire,discount,countallow),buttons=keys.key_discouny(),parse_mode="HTML")
                        user_cach.pop(user_id)
                        user_step.pop(user_id)
                        
                else:
                    await event.reply("مقدار ورودی اشتباه است لطفا عدد به عنوان مقدار وارد کنید ❗️")

            except Exception as e:
                await log_to_channel(event, action=f"خطا در پردازش مرحله: {e}")

        step = user_step[user_id]
        message_text = event.text  
         
        if step == "awaiting_message_text" and message_text != "پیام همگانی ✉️":
            try:
                user_cach[user_id]["message_text"] = message_text
                users = await db.read_users()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                Msgg = await event.respond("در حال ارسال پیام به کاربران⏳")
                for user in users:
                    try:
                        await client.send_message(int(user[1]), message_text)
                    except Exception as user_error:
                        print(f"خطا در ارسال پیام به کاربر {user[1]}: {user_error}")
                        # ارسال لاگ خطا در ارسال پیام به هر کاربر
                        await log_to_channel(
                            event, 
                            action=f"خطا در ارسال پیام به کاربر {user[1]}: {user_error}"
                        )   
                # حذف پیام "در حال ارسال"
                await Msgg.delete()
                # ارسال پیام موفقیت‌آمیز به مدیر
                keyboard = keys.key_start_sudo()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("پیام مورد نظر با موفقیت ارسال شد✅", buttons=keyboard) 
                # ارسال لاگ برای ارسال موفقیت‌آمیز پیام
                await log_to_channel(
                    event, 
                    action=f"پیام همگانی با موفقیت ارسال شد: {message_text[:50]}..."  # نمایش 50 کاراکتر اول پیام
                )   
                # پاک کردن اطلاعات از کش
                user_step.pop(user_id)
                user_cach.pop(user_id)

            except Exception as e:
                # ارسال لاگ برای هر نوع خطا که در روند اجرا پیش می‌آید
                await log_to_channel(
                    event, 
                    action=f"خطا در ارسال پیام همگانی: {str(e)}"
                )   
                
    except Exception as e:
            await log_to_channel(
                event, 
                action=f"خطا در: {str(e)}"
            )   
# -------------------------------  user -------------------------------
                        
@client.on(events.NewMessage(pattern="افزایش موجودی 👛"))
async def update_card(event):
    global user_step,user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                keyboard = keys.how_pay()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply(ConstText.charg_acc, buttons=keyboard)

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست افزایش موجودی را ارسال کرد."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} شرایط برای افزایش موجودی را ندارد."
                )

        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست افزایش موجودی برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="خدمات ویژه! 💫"))
async def update_card(event):
    global user_cach,user_step
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("❕ این بخش در بزودی فعال خواهد شد ...")

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست خدمات ویژه را ارسال کرد."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} شرایط لازم برای استفاده از خدمات ویژه را ندارد."
                )

        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست خدمات ویژه برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="💵 درگاه بانکی"))
async def pay_dargah(event):
    global user_step,user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                user_step[user_id] = "cash"
                user_cach[user_id] = {}
                keyboard = keys.cancel()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("💶 جهت افزایش موجودی حساب مبلغ مورد نظر خود را به تومان وارد نمایید:", buttons=keyboard)

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست درگاه بانکی برای افزایش موجودی ارسال کرده است."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} شرایط لازم برای استفاده از درگاه بانکی را ندارد."
                )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست درگاه بانکی برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="پرداخت مستقیم 📥"))
async def update_card(event):
    global user_cach,user_step
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                keyboard = keys.key_id_suppoort()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply(ConstText.pay_card, buttons=keyboard)

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست پرداخت مستقیم کرده است."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} شرایط لازم برای استفاده از پرداخت مستقیم را ندارد."
                )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست پرداخت مستقیم برای کاربر {user_id}: {str(e)}"
        )
               
@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def rule_bot(event):
    global user_step,user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await client.send_message(
                        user_id,
                        ConstText.rules,
                        parse_mode="HTML"
                    )

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست مشاهده قوانین و راهنما را داشت."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} شرایط لازم برای مشاهده قوانین و راهنما را ندارد."
                )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست قوانین و راهنما برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="سفارش استارت \\(زیر مجموعه\\) ⭐️"))
async def order_bot(event):
    global user_cach,user_step
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:
                referal_list = await db.read_referrabots()
                if not referal_list:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("هیچ رباتی در لیست وجود ندارد.")
                    await log_to_channel(
                        event,
                        action=f"کاربر {user_id} درخواست لیست ربات‌ها را داشت، اما لیست خالی بود."
                    )
                    return

                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    key = keys.key_read_button_refferalbot(referal_list, page=1)
                    await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)

                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} لیست ربات‌ها را درخواست کرد و صفحه اول نمایش داده شد."
                )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def pagination_handler(event):
    page = int(event.pattern_match.group(1))
    try:
        referal_list = await db.read_referrabots()
        if not referal_list:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.answer("هیچ داده‌ای برای نمایش وجود ندارد.", alert=True)

            await log_to_channel(
                event,
                action=f"کاربر {event.sender_id} صفحه {page} از لیست ربات‌ها را درخواست کرد، اما لیست خالی بود."
            )
            return

        key = keys.key_read_button_refferalbot(referal_list, page=page)
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(0.3)
            await event.edit(f"لیست ربات‌ها (صفحه {page})", buttons=key)

        await log_to_channel(
            event,
            action=f"کاربر {event.sender_id} صفحه {page} از لیست ربات‌ها را با موفقیت دریافت کرد."
        )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست صفحه {page} از لیست ربات‌ها برای کاربر {event.sender_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="اطلاع رسانی ها 📌"))
async def news_bot(event):
    global user_step,user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            b = await db.ReadUserByUserId(user_id)
            if b[7] == 0:    
                keyboard = keys.key_chanell_notif()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply(ConstText.channel, buttons=keyboard)
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} درخواست اطلاع رسانی‌ها را داد."
                )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست برای کاربر {user_id}: {str(e)}"
        )
      
@client.on(events.NewMessage(pattern="پشتیبانی ☎️"))
async def support_bot(event):
    global user_cach,user_step
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    try:
        user = await is_user_in_channel(user_id)
        if user:
            key = keys.key_id_suppoort()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await client.send_message(
                    user_id,
                    ConstText.support,
                    buttons=key
                )
            await log_to_channel(
                event,
                action=f"کاربر {user_id} درخواست پشتیبانی را داده است."
            )
        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست برای کاربر {user_id}: {str(e)}"
        )
    
@client.on(events.NewMessage(pattern="اطلاعات حساب 👤"))
async def user_detail_bot(event: events.NewMessage.Event):
    global user_step,user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        user = await is_user_in_channel(user_id)
        if user:
            amount = await db.ReadWalletUser(user_id)
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await client.send_message(
                    user_id,
                    ConstText.detail.format(user_id, amount[0]),
                    parse_mode="HTML"
                )
            
            await log_to_channel(
                event,
                action=f"اطلاعات حساب کاربر {user_id} ارسال شد. موجودی: {amount[0]} تومان"
            )

        else:
            await log_to_channel(
                event,
                action=f"کاربر {user_id} در کانال نیست."
            )
            await event.respond("برای دسترسی به اطلاعات حساب باید در کانال عضو باشید.")

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست اطلاعات حساب برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="انصراف ❌"))
async def backmenohandeler(event):
    global user_cach, user_step
    user_id = event.sender.id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        await client.send_message(user_id, "🌹")
        sudo = await db.ReadAdmin(user_id)
        if sudo:
            keyboard = keys.key_start_sudo()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)
            
            await log_to_channel(
                event,
                action=f"عملیات کنسل شد توسط ادمین {user_id}."
            )
        else:
            keyboard = keys.key_start_user()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)
            
            await log_to_channel(
                event,
                action=f"عملیات کنسل شد توسط کاربر {user_id}."
            )
        
        user_cach.pop(user_id)
        user_step.pop(user_id)

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در انصراف عملیات توسط کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="بازگشت 🔙"))
async def backmenotexthandeler(event):
    global user_cach,user_step
    user_id = event.sender.id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    await client.send_message(user_id,"🌹")
    sudo = await db.ReadAdmin(user_id)
    if sudo:
        keyboard = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    user_step.pop(user_id)
    user_cach.pop(user_id)

@client.on(events.NewMessage(pattern="منو قبل 🔙"))
async def backmeno(event):
    global user_cach,user_step
    user_id = event.sender.id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    await client.send_message(user_id,"🌹")
    sudo = await db.ReadAdmin(user_id)
    if sudo:
        keyboard = keys.refferal_key()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
    user_cach.pop(user_id)
    user_step.pop(user_id)
    
pattern = r'https://t\.me/([\w\d_]+)/[\w\d_]+\?startapp=([\w\d=%_]+)'

@client.on(events.NewMessage(pattern=pattern))
async def handler(event):
    global user_step,user_cach
    user_id = event.sender.id
    message = event.message.text
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    try:
        user = await db.ReadUserByUserId(user_id)
        
        match = re.search(r'(https://t\.me/[\w\d_]+)/[\w\d_]+\?startapp=([\w\d=%_]+)', message)
        
        if user:
            if match:
                username = match.group(1)
                ref = match.group(2)
                x = await db.read_referrabotbyname(username)

                if x:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        namaaa = x[0]
                        price = int(float(x[2]))
                        
                        user_cach[user_id] = dict()
                        user_cach[user_id].update({"name": namaaa})
                        user_cach[user_id].update({"ref":ref})
                        user_cach[user_id].update({"usname":username})
                        user_cach[user_id].update({"price":price})
                        user_step[user_id] = "read_balance_" + namaaa
                        
                        key = keys.key_order_ref(price, namaaa, count=1)
                        
                        await event.reply(
                            ConstText.order.format(x[0], username, ref, None, price),
                            buttons=key, parse_mode="HTML"
                        )
                        
                        await log_to_channel(
                            event, 
                            action=f"کاربر {user_id} به ربات {username} ارجاع داده شد. ref: {ref}"
                        )
                else:
                    await log_to_channel(
                        event, 
                        action=f"ربات با نام کاربری {username} پیدا نشد. (کاربر: {user_id})"
                    )
            else:
                await event.reply("لینک وارد شده معتبر نیست.")
                
                await log_to_channel(
                    event, 
                    action=f"لینک وارد شده توسط کاربر {user_id} معتبر نیست."
                )
        else:
            await event.reply("شما در سیستم ثبت نشده‌اید.")
            
            await log_to_channel(
                event, 
                action=f"کاربر {user_id} در سیستم ثبت نشده است."
            )

    except Exception as e:
        await log_to_channel(
            event, 
            action=f"خطا در پردازش درخواست کاربر {user_id}: {str(e)}"
        )

# -------------------------------  admin -------------------------------

@client.on(events.NewMessage(pattern="مدیریت ربات ها📍"))
async def update_card(event):
    user_id = event.sender_id
    global user_step,user_cach
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    try:
        admin = await db.ReadAdmin(user_id)
        
        if admin:
            keyboard = keys.refferal_key()
            
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("یکی از موارد زیر را انتخاب کنید 🙏🏻", buttons=keyboard)
            
            await log_to_channel(
                event,
                action=f"ادمین {user_id} به منوی مدیریت ربات‌ها دسترسی پیدا کرد."
            )
        else:
            await event.respond("شما دسترسی به این بخش ندارید. تنها ادمین‌ها قادر به دسترسی به این قسمت هستند.")
            await log_to_channel(
                event,
                action=f"کاربر {user_id} سعی کرده به بخش مدیریت ربات‌ها دسترسی پیدا کند، اما دسترسی نداشته است."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست برای کاربر {user_id}: {str(e)}"
        )



@client.on(events.NewMessage(pattern="آپلود سشن 📤"))
async def update_card(event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        # بررسی دسترسی ادمین
        admin = await db.ReadAdmin(user_id)
        
        if admin:
            # ارسال پیام برای آپلود سشن
            keyboard = keys.cancel()
            
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("فایل سشن تلتون خود را ارسال نمایید 🙏🏻", buttons=keyboard)
            
            # تنظیم وضعیت کاربر
            user_step[user_id] = "get_session"
            
            # ارسال لاگ موفقیت‌آمیز برای دسترسی ادمین
            await log_to_channel(
                event,
                action=f"ادمین {user_id} درخواست آپلود سشن را ارسال کرده است."
            )
        else:
            # ارسال پیام در صورتی که کاربر ادمین نباشد
            await event.respond("شما دسترسی به این بخش ندارید. تنها ادمین‌ها قادر به دسترسی به این قسمت هستند.")
            
            # ارسال لاگ خطا در صورتی که کاربر ادمین نباشد
            await log_to_channel(
                event,
                action=f"کاربر {user_id} سعی کرده به بخش آپلود سشن دسترسی پیدا کند، اما دسترسی نداشته است."
            )
    except Exception as e:
        # در صورت بروز خطا، لاگ خطا ارسال می‌شود
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست برای کاربر {user_id}: {str(e)}"
        )
        print(f"خطا: {e}")
        await event.respond("خطا در پردازش درخواست شما پیش آمد. لطفا دوباره تلاش کنید.")

@client.on(events.NewMessage(pattern="^پیام همگانی ✉️$"))
async def send_message_channel(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    try:
        # بررسی اینکه آیا کاربر ادمین است
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # بررسی دسترسی‌های ادمین
            AcsessType = await db.ReadAccessTypesByUserId(user_id)
            if AcsessType[2] == 1:
                user_cach[user_id] = {}  # پاکسازی اطلاعات موقت کاربر
                
                keyboard = keys.Back_Reply()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("لطفاً متن پیام همگانی را وارد کنید 🙏🏻", buttons=keyboard)
                
                # تغییر وضعیت کاربر به حالت انتظار برای دریافت پیام
                user_step[user_id] = "awaiting_message_text"
                
                # ارسال لاگ برای موفقیت درخواست
                await log_to_channel(
                    event,
                    action=f"ادمین {user_id} درخواست ارسال پیام همگانی کرده است."
                )
            else:
                # ارسال پیام در صورتی که دسترسی کافی نداشته باشد
                await event.respond(ConstText.noacsess)
                
                # ارسال لاگ در صورتی که کاربر دسترسی نداشته باشد
                await log_to_channel(
                    event,
                    action=f"کاربر {user_id} دسترسی لازم برای ارسال پیام همگانی ندارد."
                )
        else:
            # ارسال پیام در صورتی که کاربر ادمین نباشد
            await event.respond(ConstText.noacsess)
            
            # ارسال لاگ در صورتی که کاربر ادمین نباشد
            await log_to_channel(
                event,
                action=f"کاربر {user_id} سعی کرده به بخش ارسال پیام همگانی دسترسی پیدا کند اما ادمین نبوده است."
            )
    
    except Exception as e:
        # ثبت لاگ خطا در صورت بروز مشکل
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست ارسال پیام همگانی برای کاربر {user_id}: {str(e)}"
        )
        await event.respond("خطا در پردازش درخواست شما پیش آمد. لطفاً دوباره تلاش کنید.")

@client.on(events.NewMessage(pattern="حذف حساب کاربر 🗑"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}

            keyboard = keys.cancel() 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            user_step[user_id] = "user_delete" 
            await log_to_channel(
                event,
                action=f"ادمین {user_id} درخواست حذف حساب کاربر را آغاز کرد."
            )
        else:
            await event.reply(ConstText.noacsess)

            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده درخواست حذف حساب کاربر را بدهد."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست حذف حساب برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="حذف حساب شارژ 🗑"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}
            keyboard = keys.cancel() 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            
            user_step[user_id] = "user_wallet_delete" 
            await log_to_channel(
                event,
                action=f"ادمین {user_id} درخواست حذف حساب شارژ کاربر را آغاز کرد."
            )
        else:
            await event.reply(ConstText.noacsess)
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده درخواست حذف حساب شارژ کاربر را بدهد."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست حذف حساب شارژ برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="کسر حساب ➖"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}
            keyboard = keys.cancel() 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            
            user_step[user_id] = "user_id_neg" 

            await log_to_channel(
                event,
                action=f"ادمین {user_id} درخواست کسر حساب برای کاربر را آغاز کرد."
            )
        else:
            await event.reply(ConstText.noacsess)

            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده درخواست کسر حساب بدهد."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست کسر حساب برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="شارژ حساب ➕"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")


    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}
            keyboard = keys.cancel() 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            user_step[user_id] = "user_id" 
            await log_to_channel(
                event,
                action=f"ادمین {user_id} درخواست شارژ حساب برای کاربر را آغاز کرد."
            )
        else:
            await event.reply(ConstText.noacsess)
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده درخواست شارژ حساب بدهد."
            )
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست شارژ حساب برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="حساب کاربر 👤"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                keyboard = keys.key_charg_user()
                await client.send_message(
                    user_id,
                    "<blockquote>حساب کاربران 👥</blockquote>پنل مدیریت حساب کاربران خوش آمدید 🤗",
                    buttons=keyboard,
                    parse_mode="HTML"
                )
            
            await log_to_channel(
                event,
                action=f"ادمین {user_id} وارد پنل مدیریت حساب کاربران شد."
            )

        else:
            await event.reply(ConstText.noacsess)
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده وارد پنل مدیریت حساب کاربران شود."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست پنل مدیریت حساب کاربران برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="مسدود کردن 🔴"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}
            keyboard = keys.cancel()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            
            user_step[user_id] = "block_user_id"
            await log_to_channel(
                event,
                action=f"ادمین {user_id} وارد بخش مسدود کردن کاربران شد."
            )
        else:
            await event.reply(ConstText.noacsess)
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده وارد بخش مسدود کردن کاربران شود."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست مسدود کردن برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="رفع مسدودیت 🟢"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            user_cach[user_id] = {}
            keyboard = keys.cancel() 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
            
            user_step[user_id] = "unblock_user_id"
            await log_to_channel(
                event,
                action=f"ادمین {user_id} وارد بخش رفع مسدودیت کاربران شد."
            )
        else:
            await event.reply(ConstText.noacsess)
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده وارد بخش رفع مسدودیت کاربران شود."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست رفع مسدودیت برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="^مشتریان و گزارشات 📎$"))
async def log(event: events.NewMessage.Event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if admin:
        try:
            log = await db.read_users()
            count_user = len(log)
            total_wallet = sum([user[4] for user in log if len(user) >= 5])
            report_content = []
            report_content.append(f"تعداد کل کاربران: {count_user}\n")
            report_content.append(f"موجودی کل ربات: {total_wallet}\n")
            report_content.append("وضعیت کاربران =>\n")
            
            for user in log:
                user_id = user[1]
                name = user[2] or "ناموجود"
                username = user[3] or "ناموجود"
                wallet = user[4]
                block_status = "بلاک شده" if user[7] else "فعال"
                
                report_content.append(f"\nآیدی عددی کاربر: {user_id} \n اسم: {name} \n یوزرنیم: {username}\n")
                report_content.append(f"موجودی کاربر: {name} = {wallet}\n")
                report_content.append(f"{name} = {block_status}\n")
                report_content.append("---------------------------------------------------\n")

            with open("log.txt", "w", encoding="utf-8") as wp:
                wp.writelines(report_content)

            if os.path.exists("log.txt"):
                async with client.action(event.chat_id, 'document'):
                    await asyncio.sleep(0.3)
                    await client.send_file(
                        event.chat_id,
                        "log.txt",
                        caption="<blockquote>📊 لیست گزارشات</blockquote>",
                        parse_mode="HTML"
                    )
                os.remove("log.txt")
                await log_to_channel(
                    event,
                    action=f"گزارشات مشتریان و موجودی‌ها به ادمین {user_id} ارسال شد."
                )
            else:
                await log_to_channel(
                    event,
                    action=f"فایل گزارشات برای ادمین {user_id} پیدا نشد."
                )
        
        except Exception as e:
            await log_to_channel(
                event,
                action=f"خطا در پردازش درخواست گزارشات از ادمین {user_id}: {str(e)}"
            )

@client.on(events.NewMessage(pattern="^آپدیت قیمت 📌$"))
async def update_balance(event):
    global user_step, user_cach
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")

    if admin:
        try:
            if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                await log_to_channel(event, action=f"وضعیت قبلی برای ادمین {user_id} پاکسازی شد.")
                return

            user_step[user_id] = "namee"
            user_cach[user_id] = {}
            
            keyboard = keys.Back_menu()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("لطفاً یوزرنیم ربات را وارد کنید 😊", buttons=keyboard)
            await log_to_channel(event, action=f"ادمین {user_id} درخواست نام ربات را وارد کرد.")

        except Exception as e:
            await log_to_channel(event, action=f"خطا در پردازش درخواست آپدیت قیمت از ادمین {user_id}: {str(e)}")

@client.on(events.NewMessage(pattern="➕ ساخت کلید 🔑"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step, user_cach
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        admin = await db.ReadAdmin(user_id)
        if admin:
            user_step[user_id] = "name"
            user_cach[user_id] = {}
            keyboard = keys.Back_menu()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("لطفاً نام ربات را وارد کنید 🙏🏻", buttons=keyboard)
            
            await log_to_channel(
                event,
                action=f"ادمین {user_id} فرآیند ساخت کلید جدید را آغاز کرده است."
            )
        else:
            await event.respond("شما دسترسی لازم برای انجام این عمل را ندارید.")
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده فرآیند ساخت کلید را آغاز کند."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست ساخت کلید برای کاربر {user_id}: {str(e)}"
        )

@client.on(events.NewMessage(pattern="➖ حذف کلید 🔑"))
async def delete_refferal_bot(event):
    user_id = event.sender_id
    global user_step, user_cach
    admin = await db.ReadAdmin(user_id)
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if admin:
        try:
            if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
            user_step[user_id] = "nam"
            user_cach[user_id] = {}
            
            keyboard = keys.Back_menu()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("لطفاً یوزرنیم ربات را وارد کنید 😊", buttons=keyboard)

            await log_to_channel(event, action=f"ادمین {user_id} درخواست وارد کردن نام ربات برای حذف کلید را داد.")

        except Exception as e:
            await log_to_channel(event, action=f"خطا در پردازش درخواست حذف کلید ربات از ادمین {user_id}: {str(e)}")
        
@client.on(events.NewMessage(pattern="♾️ نمایش کلید ها 🔑"))
async def show_ref_bot(event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if admin:
        if user_id in user_step:
                user_step.pop(user_id)
                user_cach.pop(user_id)
                return
        referal_list = await db.read_referrabots()
        if not referal_list:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("هیچ رباتی در لیست وجود ندارد 🔴")
            
            await log_to_channel(event, action=f"ادمین {user_id} درخواست نمایش ربات‌ها داد، اما هیچ رباتی در لیست وجود ندارد.")
            return

        key = keys.key_read_button_refferalbot(referal_list, page=1)
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(0.3)
            await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)
        
        await log_to_channel(event, action=f"ادمین {user_id} ربات‌ها را در صفحه ۱ مشاهده کرد.")
    
    else:
        key = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(0.3)
            await event.respond("شما به این بخش دسترسی ندارید ⚠️", buttons=key)
        
        await log_to_channel(event, action=f"کاربر {user_id} تلاش کرده به بخش نمایش ربات‌ها دسترسی پیدا کند، اما دسترسی ندارد.")

@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def show_ref_bot_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.answer("هیچ داده‌ای برای نمایش وجود ندارد ❗️", alert=True)
        await log_to_channel(event, action=f"ادمین تلاش کرده صفحه {page} را مشاهده کند، اما هیچ رباتی وجود ندارد.")
        return

    key = keys.key_read_button_refferalbot(referal_list, page=page)
    async with client.action(event.chat_id, 'typing'):
        await asyncio.sleep(0.3)
        await event.edit(f"لیست ربات‌ها (صفحه {page}) 👇🏻", buttons=key)

    await log_to_channel(event, action=f"ادمین {event.sender_id} صفحه {page} ربات‌ها را مشاهده کرد.")

@client.on(events.NewMessage(pattern="کد تخفیف 🏷"))
async def start_create_referrabot(event):
    global user_step, user_cach
    user_id = event.sender_id
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
                keyboard = keys.key_discouny()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("پنل مدیریت تخفیفات 🏷", buttons=keyboard)
        else:
            await event.respond(ConstText.noacsess)
            
            await log_to_channel(
                event,
                action=f"کاربر {user_id} سعی کرده به بخش ارسال پیام همگانی دسترسی پیدا کند اما ادمین نبوده است."
            )
    
    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست ارسال پیام همگانی برای کاربر {user_id}: {str(e)}"
        )
            
@client.on(events.NewMessage(pattern="ثبت تخفیف 🟢"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step, user_cach
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        admin = await db.ReadAdmin(user_id)
        if admin:
            user_step[user_id] = "discount"
            user_cach[user_id] = {}
            keyboard = keys.cancel()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("لطفاً درصد تخفیف را وارد کنید 🙏🏻", buttons=keyboard)
            await log_to_channel(
                event,
                action=f"ادمین {user_id} فرآیند ساخت کلید جدید را آغاز کرده است."
            )
        else:
            await event.respond("شما دسترسی لازم برای انجام این عمل را ندارید.")
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده فرآیند ساخت کلید را آغاز کند."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست ساخت کلید برای کاربر {user_id}: {str(e)}"
        )
        print(f"Error: {e}")
        await event.respond("خطا در پردازش درخواست شما پیش آمد. لطفاً دوباره تلاش کنید.")
 
@client.on(events.NewMessage(pattern="حذف تخفیف 🗑"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step, user_cach
    if user_id in user_step:
        user_step.pop(user_id)
        user_cach.pop(user_id)
        return
    await log_to_channel(event, action=f"کاربر روی دکمه {event.text}")
    try:
        admin = await db.ReadAdmin(user_id)
        if admin:
            user_step[user_id] = "del_discount"
            user_cach[user_id] = {}
            keyboard = keys.cancel()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("لطفاً برای حذف ٫ کد تخفیف را وارد کنید 🙏🏻", buttons=keyboard)
            await log_to_channel(
                event,
                action=f"ادمین {user_id} فرآیند حذف را آغاز کرده است."
            )
        else:
            await event.respond("شما دسترسی لازم برای انجام این عمل را ندارید.")
            await log_to_channel(
                event,
                action=f"کاربر {user_id} بدون دسترسی سعی کرده فرآیند ساخت کلید را آغاز کند."
            )

    except Exception as e:
        await log_to_channel(
            event,
            action=f"خطا در پردازش درخواست ساخت کلید برای کاربر {user_id}: {str(e)}"
        )
           
# -------------------------------  callback -------------------------------
            
@client.on(events.CallbackQuery)
async def callback_handler(event):
    user_id = event.sender.id
    global user_step, user_cach
    data = event.data.decode()

    await log_to_channel(event, action=f"کاربر {user_id} درخواست callback ارسال کرد: {data}")

    if "back" in data:
        keyboard = keys.Back_Reply()
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(0.3)
            await event.edit("به منو اصلی بازگشتید 🔙", buttons=keyboard)
            
        await log_to_channel(event, action=f"کاربر {user_id} به منوی اصلی بازگشت.")
        
    if "at_" in data:
        separated = data.split(',')
        at = separated[0].replace("at_", "")
        amount = separated[1].replace("am_", "")
        try:
            if at and amount:
                response = pay.check_status_payment(amount, at)
                if response == 100 or response == 101:
                    f = await db.ReadWalletUser(user_id)
                    await db.UpdateWalletUser(int(user_id), int(float(amount)) + f[0])
                    buttons = keys.key_start_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.edit("پرداخت با موفقیت انجام شد ✅", buttons=buttons)
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond(f"مقدار {int(float(amount))} به کیف پول شما اضاف شد 🤑")
                    await log_to_channel(event, action=f"پرداخت موفق برای کاربر {user_id}: مبلغ {amount} تومان اضافه شد.")
                    
                    user_cach.pop(user_id)
                    user_step.pop(user_id)

                elif "error not active" in response:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("هنوز پرداخت انجام نشده است ❗️")
                    await log_to_channel(event, action=f"پرداخت برای کاربر {user_id} در حال پردازش یا غیر فعال است.")
                
                else:
                    buttons = keys.key_start_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.edit("پرداخت انجام نشد ❌", buttons=buttons)
                    await log_to_channel(event, action=f"پرداخت برای کاربر {user_id} با شکست مواجه شد.")
        except TypeError:
            pass
    
    order_step = user_step.get(user_id)

    if "read_balance_" in order_step:
        name = order_step.replace("read_balance_", "")
        user_cach[user_id].update({"read_balance_": name})
        
        if "discount_" in data:
            user_step[user_id] = "discount_"
            await event.reply("کد تخفیف را وارد کنید 🙏🏻",buttons=keys.cancel())
          
        elif "plus_" in data:
            i = int(data.replace("plus_", ""))
            balanc = await db.read_balance_referrabotbyname(name)
            i = i + 1
            user_cach[user_id] = {"count": i}
            balanc = int(float(balanc[0]))
            balanc = balanc * i
            user_cach[user_id] ={"lastbalance":balanc}

            keyboard = keys.key_order_ref(balanc, name, i)
            await event.edit(buttons=keyboard)

            # ثبت لاگ برای افزایش مقدار
            await log_to_channel(event, action=f"کاربر {user_id} مقدار {i} را برای ربات {name} افزایش داد.")

        elif "neg_" in data:
            balanc = await db.read_balance_referrabotbyname(name)
            balanc = int(float(balanc[0]))

            i = int(data.replace("neg_", ""))
            i = i - 1
            if i >= 1:
                user_cach[user_id]={"count": i}
                balanc = balanc * i
                user_cach[user_id] ={"lastbalance":balanc}
                keyboard = keys.key_order_ref(balanc, name, i)
                await event.edit(buttons=keyboard)

                # ثبت لاگ برای کاهش مقدار
                await log_to_channel(event, action=f"کاربر {user_id} مقدار {i} را برای ربات {name} کاهش داد.")
            else:
                if i == 1:
                    i = 1
                    user_cach[user_id]={"count":i}
                    
                    balanc = balanc * i
                    user_cach[user_id] ={"lastbalance":balanc}

                    balanc = int(float(balanc[0]))
                    keyboard = keys.key_order_ref(balanc, name, i)
                    await event.edit(buttons=keyboard)
                
                    # ثبت لاگ برای تنظیم مقدار به 1
                    await log_to_channel(event, action=f"کاربر {user_id} مقدار را برای ربات {name} به 1 تنظیم کرد.")

        elif "do_" in data:
            i = int(data.replace("do_", ""))
            user_cach[user_id].update({"i":data})
            balanc = await db.read_balance_referrabotbyname(name)
            balanc = int(float(balanc[0]))
            balanc = balanc * i
            user_cach[user_id].update({"lastbalance":balanc})
            keyboard = keys.key_order_ref(balanc, name, i)
            await event.edit(buttons=keyboard)
            await log_to_channel(event, action=f"کاربر {user_id} مقدار {i} را برای ربات {name} تنظیم کرد.")
                  
        elif "accept_order" in data:
            balanc = await db.read_balance_referrabotbyname(name)
            balanc1 = user_cach[user_id]["lastbalance"]
            incach = await db.ReadWalletUser(user_id)
            
            if incach[0] <= balanc1 :
                await log_to_channel(event, action=f"کاربر {user_id} تلاش کرده برای ربات {name} پرداخت انجام دهد اما موجودی کافی ندارد.")
                await event.edit("💰 اعتبار شما کافی نیست بعد از شارژ اعتبار دوباره اقدام کنید")
                user_step.pop(user_id)
                user_cach.pop(user_id)
                
            else:
                username =user_cach[user_id]["usname"].replace("https://t.me/","")
                ref = user_cach[user_id]["ref"]
                file = "./session"
                if os.path.exists(file):
                    files = os.listdir(file)
                    
#TODO if code discount i-- tabale, 

                    limit = int(user_cach[user_id]["i"].replace("do_",""))

                    for index, i in enumerate(files):
                        if index >= limit:
                            break

                        already_started = await db.is_bot_already_started(i, username)
                        
                        if already_started:
                            await event.respond(f"❌ این سشن ({i}) قبلاً ربات {username} را استارت کرده است.")
                            continue
                        
                        respons = await account.acc_start_ref(i, username, ref)
                        
                        if respons:
                            balance = incach[0] - balanc1 
                            await db.UpdateWalletUser(user_id,balance)
                            await db.add_start(i,username)
                            await event.respond("hi")
#TODO last key to set order

                        else:
                            await event.respond("by")
                    
            

# -------------------------------  run -------------------------------

async def run(): 
    await db.create_database()
    for i in [6785692975,]:
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


