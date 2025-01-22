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
from datetime import date
from telethon.tl.types import SendMessageTypingAction
import asyncio
import sqlite3
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

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

# -------------------------------  start -------------------------------

@client.on(events.NewMessage(pattern="/start"))
async def start_bot(event):
    user_id = event.sender_id
    anyadmin = await db.ReadAdmin(user_id)
    if anyadmin is None:
        isany = await db.ReadUserByUserId(user_id)
        if isany is None:
            await db.create_user(user_id,event.sender.first_name,event.sender.username,0,0,10,0)
            isany = await db.ReadUserByUserId(user_id)
            
        if isany[7] == 0:
            try:
                user = await is_user_in_channel(user_id)
                if user:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond(
                            ConstText.StartMsg.format(event.sender.first_name),
                            buttons=keys.key_start_user()
                        )
                        return True
                else:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await client.send_message(user_id,
                            ConstText.join_channel,
                            buttons=keys.key_join_ejbar(),parse_mode="HTML"
                        )
                        return False
            except Exception:
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await client.send_message(user_id,
                            ConstText.join_channel,
                            buttons=keys.key_join_ejbar(),parse_mode="HTML"
                        )
                        return False
        else:
            pass
    else:
        rolle = anyadmin[2]
        if rolle == 1: 
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond(
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
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]

    if current_step == "cash":
        if event.text.isdigit():
            cash = float(event.text)
            user_cach[user_id]["cash"] = cash
            if user_cach[user_id]["cash"] >= 1000 and user_cach[user_id]["cash"] <= 5000000:
                payment_url = pay.link_payment(user_cach[user_id]["cash"])
                match = re.search(r'/StartPay/([^/]+)', payment_url)
                await event.respond("⏳",buttons=keys.key_start_user())
                if match:
                    code = match.group(1)
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply(
                            f"💳 فاکتور افزایش موجودی به مبلغ {user_cach[user_id]['cash']} تومان صادر گردید.\n"
                        "👈 درصورتی که مورد تاییدتان است با انتخاب یکی از گزینه های زیر پرداخت خود را انجام دهید",
                        buttons=keys.pay_dargah(payment_url,code,user_cach[user_id]['cash'])
                    )
                        await event.respond("🛍 فاکتور شما با موفقیت ایجاد شد.",buttons=keys.cancel())
                        user_step.pop(user_id)
                        user_cach.pop(user_id)
                    
            else:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await client.send_message(user_id,"مبلغ شما کمتر از میزان تعیین شده برای پرداخت است لطفا مبلغ درخواست را افزایش دهید و دوباره تلاش کنید 🌹")
        else:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
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
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
            await db.delete_referrabot(str(user_cach[user_id]["nam"]))
            keyboard = keys.refferal_key()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
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
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
            return
        if namee.isdigit():
            if user_cach[user_id]["namee"]  == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
            user_step[user_id] = "balancee"
            is_valid = await db.read_referrabot_name(user_cach[user_id]["namee"])
            if is_valid:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("لطفاً قیمت جدید را به تومان وارد کنید 🙏🏻")
            else:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("نام اشتباه وارد شده است 🔴")
        else:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
    
    name = event.text
    
    if user_step[user_id] == "منو قبل 🔙":
        keyboard = keys.refferal_key()
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(0.3)
            await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
        return
    
    if current_step == "name" and name != "➕ ساخت کلید 🔑":
 
            user_cach[user_id]["name"] = name
            if user_cach[user_id]["name"]  == "منو قبل 🔙":
                user_step.pop(user_id)
                user_cach.pop(user_id)
                keyboard = keys.refferal_key()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                return
            user_step[user_id] = "username"
            async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
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
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                return
            user_step[user_id] = "balance"
            async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("لطفاً قیمت را به تومان وارد کنید 🙏🏻")
        else:
            async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
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
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
                user_step[user_id] = "completed" 
                await db.create_referrabot(user_cach[user_id]['name'], user_cach[user_id]['username'], user_cach[user_id]['balance'])
                keyboard = keys.refferal_key()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond(f"اطلاعات ربات ذخیره شد:\nنام: {user_cach[user_id]['name']}\nیوزرنیم: {user_cach[user_id]['username']}\nقیمت: {balance}",buttons=keyboard)
                user_step.pop(user_id)
                user_cach.pop(user_id)
            except ValueError:
                if event.text == "منو قبل 🔙":
                    user_step.pop(user_id)
                    user_cach.pop(user_id)
                    keyboard = keys.refferal_key()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("به منو قبلی بازگشتید 🔙", buttons=keyboard)
                    return
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("لطفاً قیمت را به‌صورت عدد وارد کنید.")
        else:
            async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("مقدار ورودی شما اشتباه میباشد لطفا عدد وارد کنید 🙏🏻")
            
    if current_step == "user_id":
            user_id_input = event.text
            if user_id_input.isdigit():
                user_cach[user_id] = {"user_id": user_id_input}
                user_step[user_id] = "charge_amount"
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("💶 جهت افزایش موجودی حساب مبلغ مورد نظر خود را به تومان وارد نمایید:")
            else:
                await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")
                
    elif current_step == "charge_amount":
            charge_amount = event.text
            if charge_amount.isdigit():
                charge_amount = int(charge_amount) 
                stored_user_id = user_cach[user_id]["user_id"]

                current_balance = await db.ReadWalletUser(stored_user_id)
                if current_balance:
                    new_balance = current_balance[0] + charge_amount
                    await db.UpdateWalletUser(stored_user_id, new_balance)


                    keyboard = keys.key_start_sudo()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply(f"مقدار {charge_amount} حساب کاربر {stored_user_id} با موفقیت  شارژ شد ✅", buttons=keyboard)
                    await client.send_message(int(stored_user_id), f"مقدار {charge_amount} حساب شما شارژ شد ✅")

                    user_step.pop(user_id, None)
                    user_cach.pop(user_id, None)
                else:
                    await event.reply("خطا در دریافت موجودی کاربر. لطفا دوباره تلاش کنید.")
            else:
                await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")

    if current_step == "get_session":
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
                        await event.respond("هیچ فایل سشن (.session) درون فایل zip یافت نشد.")
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
                            print(f"Error moving file {src_file}: {e}")
                            continue

                    if i > 0:
                        folder_path = "./session"
                        if os.path.exists(folder_path):
                            files = os.listdir(folder_path)
                            if files:
                                healthy_count = 0 
                                broken_count = 0  

                                for file in files:
                                    file_path = os.path.join(folder_path, file) 
                                    check_stat = await account.check_status_sessions(file_path) 

                                    if check_stat: 
                                        healthy_count += 1
                                        today = date.today()
                                        to_day = today.strftime("%Y/%m/%d")
                                        phone_number = file.replace(".session", "") 

                                        try:
                                            await db.create_account(int(phone_number), to_day)
                                        except sqlite3.OperationalError as e:
                                            print(f"Database error: {e}")
                                            async with client.action(event.chat_id, 'typing'):
                                                await asyncio.sleep(0.3)
                                                await event.respond("خطایی در دیتابیس رخ داده است.")
                                            continue
                                    else:  
                                        broken_count += 1
                                        # os.remove(file_path)  

                                async with client.action(event.chat_id, 'typing'):
                                    await asyncio.sleep(0.3)
                                    await event.respond(
                                        f"تعداد {healthy_count} سشن سالم به اکانت‌ها اضافه شد ⭐️\n"
                                        f"تعداد {broken_count} سشن خراب است."
                                    )
                            else:
                
                                async with client.action(event.chat_id, 'typing'):
                                    await asyncio.sleep(0.3)
                                    await event.respond("پوشه سشن خالی است.")
                    else:
         
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond(f"مسیر '{folder_path}' وجود ندارد.")

            except zipfile.BadZipFile:
                await event.respond("فایل zip خراب است. لطفاً یک فایل معتبر آپلود کنید.")
            finally:
         
                if os.path.exists(path):
                    os.remove(path)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
        else:
                    async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond("فرمت فایل اشتباه است. لطفاً یک فایل zip ارسال نمایید.")

    if current_step == "user_id_neg":
        user_id_input = event.text
        if user_id_input.isdigit(): 
            user_cach[user_id] = {"user_id": user_id_input}
            user_step[user_id] = "kasr_charge_amount" 
            
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.reply("چقدر می‌خواهید از حساب کاربر را کسر کنید؟")
        else:
            await event.reply("شناسه کاربری وارد شده معتبر نیست. لطفا یک شناسه عددی وارد کنید.")

    elif current_step == "kasr_charge_amount":
            charge_amount = event.text
            if charge_amount.isdigit():
                charge_amount = int(charge_amount) 
                stored_user_id = user_cach[user_id]["user_id"]

                current_balance = await db.ReadWalletUser(stored_user_id)
                if current_balance:
                    new_balance = current_balance[0] - charge_amount
                    if new_balance < 0:
                        await event.reply("موجودی کافی برای کسر این مبلغ وجود ندارد.")
                        return
                    await db.UpdateWalletUser(stored_user_id, new_balance)


                    keyboard = keys.key_start_sudo()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.reply(f"مقدار {charge_amount} حساب کاربر {stored_user_id} با موفقیت  کسر شد ✅", buttons=keyboard)
                    await client.send_message(int(stored_user_id), f"مقدار {charge_amount} از حساب شما کسر شد ✅")

                    user_step.pop(user_id, None)
                    user_cach.pop(user_id, None)
                else:
                    await event.reply("خطا در دریافت موجودی کاربر. لطفا دوباره تلاش کنید.")
            else:
                await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")

    if current_step == "user_delete":
        user_id_input = event.text
        if user_id_input.isdigit():
            user_cach[user_id] = {"user": user_id_input}
            await db.delete_user(user_cach[user_id]["user"])
            keyboard = keys.key_start_sudo()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond(f"حساب کاربری {user_cach[user_id]["user"]} با موفقیت حذف شد✅",buttons=keyboard)
    
    if current_step == "user_wallet_delete":
        user_id_input = event.text
        if user_id_input.isdigit():
            user_cach[user_id] = {"user": user_id_input}
            await db.delete_wallet_user(user_cach[user_id]["user"])
            keyboard = keys.key_start_sudo()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("حساب شارژ کاربر با موفقیت حذف شد✅",buttons=keyboard)        
    
    if current_step == "block_user_id":
        user_id = event.text
        if user_id.isdigit():
            user_cach[user_id]["user_id"] = user
            await db.blockN_User(user,1)
            keyboard = keys.key_start_sudo()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("حساب کاربر با موفقیت مسدود شد 🔴",buttons=keyboard)
    
    if current_step == "unblock_user_id":
        user_id = event.text
        if user_id.isdigit():
            user_cach[user_id]["user_id"] = user
            await db.blockN_User(user,0)
            keyboard = keys.key_start_sudo()
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("حساب کاربر با موفقیت رفع مسدودیت شد 🟢",buttons=keyboard)
                
    step = user_step[user_id]
    message_text = event.text
    
    if step == "awaiting_message_text" and message_text != "پیام همگانی ✉️":
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
        await Msgg.delete()
        keyboard = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(0.3)
                await event.respond("پیام مورد نظر با موفقیت ارسال شد✅",buttons=keyboard)
        user_step.pop(user_id, None)
        user_cach.pop(user_id, None)                     
            
# -------------------------------  user -------------------------------
                        
@client.on(events.NewMessage(pattern="افزایش موجودی 👛"))
async def update_card(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:
            keyboard = keys.how_pay()
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply(ConstText.charg_acc,buttons=keyboard)

@client.on(events.NewMessage(pattern="خدمات ویژه! 💫"))
async def update_card(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply("❕ این بخش در بزودی فعال خواهد شد ...")

@client.on(events.NewMessage(pattern="💵 درگاه بانکی"))
async def pay_dargah(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:
            global user_cach, user_step
            user_step[user_id] = "cash"
            user_cach[user_id] = {}
            
            keyboard = keys.cancel()
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond("💶 جهت افزایش موجودی حساب مبلغ مورد نظرخود را به تومان وارد نمایید:", buttons=keyboard)

@client.on(events.NewMessage(pattern="پرداخت مستقیم 📥"))
async def update_card(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:
            keyboard = keys.how_pay()
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond(ConstText.pay_card,buttons=keyboard)    
                  
@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def rule_bot(event):
    user_id = event.sender_id
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
  
@client.on(events.NewMessage(pattern="سفارش استارت \\(زیر مجموعه\\) ⭐️"))
async def order_bot(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:
            referal_list = await db.read_referrabots()
            if not referal_list:
                async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond("هیچ رباتی در لیست وجود ندارد.")
                return
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            key = keys.key_read_button_refferalbot(referal_list, page=1)
                            await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)
    
@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def pagination_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.answer("هیچ داده‌ای برای نمایش وجود ندارد.", alert=True)
        return
    key = keys.key_read_button_refferalbot(referal_list, page=page)
    async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.edit("لیست ربات‌ها (صفحه {page})".format(page=page), buttons=key)

@client.on(events.NewMessage(pattern="اطلاع رسانی ها 📌"))
async def news_bot(event):
    user_id = event.sender_id
    user = await is_user_in_channel(user_id)
    if user:
        b = await db.ReadUserByUserId(user_id)
        if b[7] == 0:    
            keyboard = keys.key_chanell_notif()
            async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.reply(ConstText.channel,buttons=keyboard)
        
@client.on(events.NewMessage(pattern="پشتیبانی ☎️"))
async def support_bot(event):
    user_id = event.sender_id
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
    
@client.on(events.NewMessage(pattern="اطلاعات حساب 👤"))
async def user_detail_bot(event: events.NewMessage.Event):
    user_id = event.sender_id       
    user = await is_user_in_channel(user_id)
    if user: 
        amount = await db.ReadWalletUser(user_id)
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await client.send_message(
            user_id,
            ConstText.detail.format(user_id, amount[0]),parse_mode="HTML"
        )

@client.on(events.NewMessage(pattern="انصراف ❌"))
async def backmenohandeler(event):
    global user_cach,user_step
    user_id = event.sender.id
    await client.send_message(user_id,"🌹")
    sudo = await db.ReadAdmin(user_id)
    if sudo:
        keyboard = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reply("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.reoly("عملیات با موفقیت کنسل شد ❌", buttons=keyboard)  
    user_cach.pop(user_id)
    user_step.pop(user_id)
    
@client.on(events.NewMessage(pattern="بازگشت 🔙"))
async def backmenotexthandeler(event):
    global user_cach,user_step
    user_id = event.sender.id
    await client.send_message(user_id,"🌹")
    sudo = await db.ReadAdmin(user_id)
    if sudo:
        keyboard = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    else:
        keyboard = keys.key_start_user()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("به منو اصلی بازگشتید 🔙", buttons=keyboard)
    user_cach.pop(user_id)
    user_step.pop(user_id)

client.on(events.NewMessage(pattern="منو قبل 🔙"))
async def backmeno(event):
    global user_cach,user_step
    user_id = event.sender.id
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
    
PATTERN = r'https://t\.me/([a-zA-Z0-9_-]+)/app\?startapp=(ref_[\w\d]+)'
@client.on(events.NewMessage(pattern=PATTERN))
async def handler(event):
    user_id = event.sender.id
    user = await db.ReadUserByUserId(user_id)
    message = event.message.text
    match = re.search(r'https://t\.me/([\w\d_]+)/app\?startapp=(ref_[\w\d]+)', message)
    if user:
        if match:
            username = match.group(1)
            ref = match.group(2)
            x = await db.read_referrabotbyname(username)
            if x:
                async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        namee = x[0]
                        user_cach[user_id] = {"name": namee}
                        user_step[user_id] = "read_balance_"+namee
                        key = keys.key_order_ref(int(float(x[2])),namee,count=1)
                        await event.reply(ConstText.order.format(x[0],f"a{username}",ref,{None},int(float(x[2]))),buttons=key,parse_mode="HTML")
        
# -------------------------------  admin -------------------------------

@client.on(events.NewMessage(pattern="مدیریت ربات ها📍"))
async def update_card(event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        keyboard = keys.refferal_key()
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("یکی از موارد زیر را انتخاب کنید 🙏🏻",buttons=keyboard)

@client.on(events.NewMessage(pattern="آپلود سشن 📤"))
async def update_card(event):
    global user_step, user_cach
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        keyboard = keys.cancel()
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("فایل سشن تلتون خود را ارسال نمایید 🙏🏻",buttons=keyboard)
                        user_step[user_id] = "get_session"

@client.on(events.NewMessage(pattern="^پیام همگانی ✉️$"))
async def send_message_channel(event: events.NewMessage.Event):
    try:
        global user_step, user_cach
        user_id = event.sender_id
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(user_id)
            if AcsessType[2] == 1:
                user_cach[user_id] = {}
                keyboard = keys.Back_Reply()
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("لطفاً متن پیام همگانی را وارد کنید 🙏🏻",buttons=keyboard)
                user_step[user_id] = "awaiting_message_text"
            else:
                await event.respond(ConstText.noacsess)
        else:
            await event.respond(ConstText.noacsess)

    except Exception as e:
        print(f"Error: {e}")
            
@client.on(events.NewMessage(pattern="➕ ساخت کلید 🔑"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step,user_cach
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        if user_id in user_step:
            user_step.pop(user_id)
            user_cach.pop(user_id)
            return
        user_step[user_id] = "name" 
        user_cach[user_id] = {}
        keyboard = keys.Back_menu()
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("لطفاً نام ربات را وارد کنید 🙏🏻",buttons=keyboard)

@client.on(events.NewMessage(pattern="حذف حساب کاربر 🗑"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:

                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "user_delete" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="حذف حساب شارژ 🗑"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:

                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "user_wallet_delete" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="کسر حساب ➖"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:

                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "user_id_neg" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="شارژ حساب ➕"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:
                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")
        
@client.on(events.NewMessage(pattern="حساب کاربر 👤"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:
        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    keyboard = keys.key_charg_user()
                    await client.send_message(user_id,"<blockquote>حساب کاربران 👥</blockquote>پنل مدیریت حساب کاربران خوش آمدید 🤗",buttons=keyboard,parse_mode="HTML")
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="مسدود کردن 🔴"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:

                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "block_user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="رفع مسدودیت 🟢"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    user_id = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(user_id)
        if AnyAdmin:
            # AcsessType = await db.ReadAccessTypesByUserId(user_id)
            # if AcsessType[2] == 1:
                user_cach[user_id] = {}
                keyboard = keys.cancel() 
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن 🙏🏻", buttons=keyboard)
                user_step[user_id] = "unblock_user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern="^مشتریان و گزارشات 📎$"))
async def log(event: events.NewMessage.Event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
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
                        caption="لیست گزارشات"
                    )
                os.remove("log.txt")
            else:
                await event.respond("فایل گزارشات پیدا نشد.")
        
        except Exception as e:
            print(f"خطایی رخ داده است: {e}")
            await event.respond("خطایی رخ داد. لطفاً دوباره تلاش کنید.")

@client.on(events.NewMessage(pattern="^آپدیت قیمت 📌$"))
async def update_balnce(event):
    global user_step, user_cach
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        
        if user_id in user_step:
            user_step.pop(user_id)
            user_cach.pop(user_id)
            return
        
        user_step[user_id] = "namee" 
        user_cach[user_id] = {}
        keyboard = keys.Back_menu()
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("لطفاً نام ربات را وارد کنید 😊",buttons=keyboard)

@client.on(events.NewMessage(pattern="➖ حذف کلید 🔑"))
async def delete_refferal_bot(event):
    user_id = event.sender_id
    global user_step, user_cach
    admin = await db.ReadAdmin(user_id)
    if admin:
        if user_id in user_step:
            user_step.pop(user_id)
            user_cach.pop(user_id)
            return
        
        user_step[user_id] = "nam" 
        user_cach[user_id] = {}
        keyboard = keys.Back_menu()
        async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond("لطفاً نام ربات را وارد کنید 😊",buttons=keyboard)
        
@client.on(events.NewMessage(pattern="♾️ نمایش کلید ها 🔑"))
async def show_ref_bot(event):
    user_id = event.sender_id
    admin = await db.ReadAdmin(user_id)
    if admin:
        referal_list = await db.read_referrabots()
        if not referal_list:
            async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("هیچ رباتی در لیست وجود ندارد 🔴")
            return
        key = keys.key_read_button_refferalbot(referal_list, page=1)
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("لیست ربات‌ها (صفحه ۱) 👇🏻", buttons=key)
    else:
        key = keys.key_start_sudo()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.respond("شما به این بخش دسترسی ندارید ⚠️", buttons=key)
    
@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def show_ref_bot_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.answer("هیچ داده‌ای برای نمایش وجود ندارد ❗️", alert=True)
        return
    key = keys.key_read_button_refferalbot(referal_list, page=page)
    async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.edit("لیست ربات‌ها (صفحه {page}) 👇🏻".format(page=page), buttons=key)
    
# -------------------------------  callback -------------------------------
            
user_cach = {}
@client.on(events.CallbackQuery)
async def callback_handler(event):
    user_id = event.sender.id
    global user_step, user_cach
    data = event.data.decode()
    
    if "at_" in data:
        separated = data.split(',')
        at=separated[0].replace("at_","")
        amount = separated[1].replace("am_","")
        try: 
            if at and amount: 
                response = pay.check_status_payment(amount,at)
                if response == 100 or response == 101:
                    
                    f = await db.ReadWalletUser(user_id)
                    await db.UpdateWalletUser(int(user_id), int(float(amount))+ f[0])
                    buttons = keys.key_start_user()
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.edit("پرداخت با موفقیت انجام شد ✅", buttons=buttons)
                    async with client.action(event.chat_id, 'typing'):
                        await asyncio.sleep(0.3)
                        await event.respond(f"مقدار {int(float(amount))} به کیف پول شما اضاف شد 🤑")
                    user_cach.pop(user_id)
                    user_step.pop(user_id)
                
                    if "error not active" in response:
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.respond("هنوز پرداخت انجام نشده است ❗️") 
                
                    
                    else:
                        buttons=keys.key_start_user()
                        async with client.action(event.chat_id, 'typing'):
                            await asyncio.sleep(0.3)
                            await event.edit("پرداخت انجام نشد ❌",buttons=buttons)
        except TypeError:
                pass
    
    order_step = user_step[user_id]
    
    if "read_balance_" in order_step:
        name = order_step.replace("read_balance_","")
        
        if "plus_" in data:
            i = int(data.replace("plus_",""))
            balanc = await db.read_balance_referrabotbyname(name)
            i = i + 1
            user_cach[user_id] = {"i": i}
            balanc = int(float(balanc[0]))
            
            keyboard = keys.key_order_ref(balanc,name,i)
            await event.edit(buttons=keyboard)
        
    order_step = user_step[user_id]
    
    if "read_balance_" in order_step:
        name = order_step.replace("read_balance_","")
        if "neg_" in data:
            balanc = await db.read_balance_referrabotbyname(name)
            balanc = int(float(balanc[0]))
            
            i = int(data.replace("neg_",""))
            i = i - 1
            if i >= 1:
                balanc = balanc * i
                keyboard = keys.key_order_ref(balanc,name,i)
                await event.edit(buttons=keyboard)
            else:
                if i == 1:
                    i = 1
                    balanc = balanc * i
                    balanc = int(float(balanc[0]))
                    keyboard = keys.key_order_ref(balanc,name,i)
                    await event.edit(buttons=keyboard)
    
    order_step = user_step[user_id]
    
    if "read_balance_" in order_step:
        name = order_step.replace("read_balance_","")
        if "do_" in data:
            i = int(data.replace("do_",""))
            balanc = await db.read_balance_referrabotbyname(name)
            balanc = int(float(balanc[0]))
            balanc = balanc * i
            keyboard = keys.key_order_ref(balanc,name,i)
            await event.edit(buttons=keyboard)
            
    order_step = user_step[user_id]
        
    if "read_balance_" in order_step:
        name = order_step.replace("read_balance_","")

        if "accept_order" in data:
            balanc = await db.read_balance_referrabotbyname(name)
            balanc = int(float(balanc[0]))
            incach = await db.ReadUserByUserId(user_id)
            incach = incach[4]
            if incach >= balanc:
                pass
            else:
                await event.edit("💰 اعتبار شما کافی نیست بعد از شارژ اعتبار دوباره اقدام کنید")
                user_step.pop(user_id)
                user_cach.pop(user_id)
        
    if "back" in data:
        keyboard=keys.Back_Reply()
        async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(0.3)
                    await event.edit("به منو اصلی بازگشتید 🔙", buttons=keyboard)
      
# -------------------------------  run -------------------------------

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