from telethon import TelegramClient, events,Button
import keys
import db
import ConstText
from socks import SOCKS5, SOCKS4, HTTP
import os

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
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.charg_acc
                        )

@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.rules
                        )
    
@client.on(events.NewMessage(pattern="سفارش استارت (زیر مجموعه) ⭐️"))
async def start_bot(event):
    userid = event.sender_id
    pass
    
@client.on(events.NewMessage(pattern="خدمات ویژه 💫"))
async def start_bot(event):
    userid = event.sender_id
    pass

@client.on(events.NewMessage(pattern="اطلاع رسانی ها 📌"))
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.channel
                        )
    
@client.on(events.NewMessage(pattern="پشتیبانی ☎️"))
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.support
                        )
    
@client.on(events.NewMessage(pattern="اطلاعات حساب 👤"))
async def start_bot(event: events.NewMessage.Event):
    userid = event.sender_id
    amount = await db.ReadWalletUser(userid)
    await client.send_message(
        userid,
        ConstText.detail.format(userid, amount[0])
    )

@client.on(events.NewMessage(pattern="انصراف"))
async def backmenohandeler(event):
    global user_cach,user_step
    userid = event.sender.id
    await client.send_message(userid,"🌹")
    keyboard = keys.key_start_sudo()
    await event.respond("تراکنش با موفقیت کنسل شد ❌", buttons=keyboard)
    user_cach.pop(userid)
    user_step.pop(userid)

# -------------------------------  admin -------------------------------

user_step = {}
user_cache = {}

@client.on(events.NewMessage(pattern="^پیام همگانی$"))
async def send_message_channel(event: events.NewMessage.Event):
    try:
        global user_step, user_cache
        userid = event.sender_id

        AnyAdmin = await db.ReadAdmin(userid)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(userid)
            if AcsessType[2] == 1:
                user_cache[userid] = {}
                await event.respond("لطفاً متن پیام همگانی را وارد کنید:")
                user_step[userid] = "awaiting_message_text"
            else:
                await event.respond(ConstText.noacsess)
        else:
            await event.respond(ConstText.noacsess)

    except Exception as e:
        print(f"Error: {e}")


@client.on(events.NewMessage())
async def handle_user_input(event: events.NewMessage.Event):
    global user_step, user_cache
    userid = event.sender_id

    if userid in user_step:
        step = user_step[userid]

        # مرحله دریافت متن پیام
        if step == "awaiting_message_text":
            message_text = event.text
            user_cache[userid]["message_text"] = message_text

            # ارسال پیام به همه کاربران
            users = await db.read_users()
            Msgg = await event.respond("در حال ارسال پیام به کاربران⏳")

            for user in users:
                try:
                    await client.send_message(int(user[1]), message_text)
                except Exception as user_error:
                    print(f"خطا در ارسال پیام به کاربر {user[1]}: {user_error}")

            await Msgg.delete()
            await event.respond("پیام مورد نظر با موفقیت ارسال شد✅")

            # پاک کردن وضعیت و اطلاعات موقت کاربر
            user_step.pop(userid, None)
            user_cache.pop(userid, None)


user_step = {}
user_cache = {}

@client.on(events.NewMessage(pattern="^شارژ حساب کاربر$"))
async def charge_account(event: events.NewMessage.Event):
    global user_step, user_cache
    userid = event.sender_id

    try:

        AnyAdmin = await db.ReadAdmin(userid)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(userid)
            if AcsessType[2] == 1:

                user_cache[userid] = {}
                keyboard = keys.cancel() 
                await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن", buttons=keyboard)
                user_step[userid] = "user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage())
async def handle_user_input(event: events.NewMessage.Event):
    global user_step, user_cache
    userid = event.sender_id


    if userid in user_step:
        step = user_step[userid]

        if step == "user_id":
            user_id = event.text
            if user_id.isdigit():
                user_cache[userid]["user_id"] = user_id
                await event.reply("چقدر می‌خواهید حساب کاربر را شارژ کنید؟")
                user_step[userid] = "charge_amount"

        elif step == "charge_amount":
            charge_amount = event.text
            if charge_amount.isdigit():
                user_cache[userid]["charge_amount"] = int(charge_amount)
                user_id = user_cache[userid]["user_id"]
                f = await db.ReadWalletUser(user_id)
                await db.UpdateWalletUser(int(user_id), int(charge_amount)+ f[0])
                keyboard = keys.key_start_sudo()
                await event.reply(f"مقدار {charge_amount} حساب کاربر {user_id} شارژ شد.",buttons=keyboard)
                await client.send_message(int(user_id), f"مقدار {charge_amount} حساب شما شارژ شد.")
                del user_step[userid]
                del user_cache[userid]
            else:
                await event.reply("لطفا یک مقدار عددی معتبر وارد کنید.")

@client.on(events.NewMessage(pattern="^مشتریان و گزارشات$"))
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
            except ValueError:
                print(f"Could not find user with ID {i}")
                continue

            await db.create_admin(i, 1, ra[0], fname)

    print("Run")
    await client.run_until_disconnected()



client.loop.run_until_complete(run())