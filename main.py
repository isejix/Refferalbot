from telethon import TelegramClient, events,Button
import keys
import db
import ConstText
from socks import SOCKS5, SOCKS4, HTTP
import os
from asyncio import sleep


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
    keyboard = keys.how_pay()
    await event.respond(ConstText.charg_acc,buttons=keyboard)

@client.on(events.NewMessage(pattern="💵 درگاه بانکی"))
async def pay_dargah(event):
    userid = event.sender_id
    global user_cach, user_step
    user_step[userid] = "cash"
    
    # Ensure user_cach[userid] is a dictionary
    user_cach[userid] = {}
    
    keyboard = keys.cancel()
    await event.respond("💶 جهت افزایش موجودی حساب مبلغ مورد نظرخود را به تومان وارد نمایید:", buttons=keyboard)

@client.on(events.NewMessage())
async def process_pay_dargah(event):
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]
    cash = float(event.text)

    if current_step == "cash":
        if user_id not in user_cach:
            user_cach[user_id] = {}
        user_cach[user_id]["cash"] = cash
        
        await event.reply(
            f"💳 فاکتور افزایش موجودی به مبلغ {user_cach[user_id]['cash']} تومان صادر گردید.\n"
            "👈 درصورتی که مورد تاییدتان است با انتخاب یکی از گزینه های زیر پرداخت خود را انجام دهید",
            buttons=keys.pay_dargah(user_cach[user_id]["cash"])
        )

    
@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.rules
                        )
    
@client.on(events.NewMessage(pattern="سفارش استارت \\(زیر مجموعه\\) ⭐️"))
async def start_bot(event):
    
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.respond("هیچ رباتی در لیست وجود ندارد.")
        return
    key = keys.key_read_button_refferalbot(referal_list, page=1)
    await event.respond("لیست ربات‌ها (صفحه ۱):", buttons=key)

@client.on(events.CallbackQuery(pattern=r"page_(\d+)"))
async def pagination_handler(event):
    page = int(event.pattern_match.group(1))
    referal_list = await db.read_referrabots()
    if not referal_list:
        await event.answer("هیچ داده‌ای برای نمایش وجود ندارد.", alert=True)
        return
    key = keys.key_read_button_refferalbot(referal_list, page=page)
    await event.edit("لیست ربات‌ها (صفحه {page}):".format(page=page), buttons=key)

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

@client.on(events.NewMessage(pattern="^پیام همگانی$"))
async def send_message_channel(event: events.NewMessage.Event):
    try:
        global user_step, user_cach
        userid = event.sender_id

        AnyAdmin = await db.ReadAdmin(userid)
        if AnyAdmin:
            AcsessType = await db.ReadAccessTypesByUserId(userid)
            if AcsessType[2] == 1:
                user_cach[userid] = {}
                await event.respond("لطفاً متن پیام همگانی را وارد کنید:")
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
        if step == "awaiting_message_text" and message_text != "پیام همگانی":
            
            user_cach[userid]["message_text"] = message_text
            users = await db.read_users()
            Msgg = await event.respond("در حال ارسال پیام به کاربران⏳")
            for user in users:
                try:
                    await client.send_message(int(user[1]), message_text)
                except Exception as user_error:
                    print(f"خطا در ارسال پیام به کاربر {user[1]}: {user_error}")

            await Msgg.delete()
            await event.respond("پیام مورد نظر با موفقیت ارسال شد✅")
            user_step.pop(userid, None)
            user_cach.pop(userid, None)
            
@client.on(events.NewMessage(pattern="^ساخت کلید🔑$"))
async def start_create_referrabot(event):
    user_id = event.sender_id
    global user_step,user_cach
    if user_id in user_step:
        await event.respond("شما در حال حاضر در فرآیند ساخت ربات هستید.")
        return
    user_step[user_id] = "name" 
    user_cach[user_id] = {}
    await event.respond("لطفاً نام ربات را وارد کنید:")

@client.on(events.NewMessage())
async def process_create_bot(event):
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]
    name = event.text

    if current_step == "name" and name != "ساخت کلید🔑":
        user_cach[user_id]["name"] = name
        user_step[user_id] = "username"
        await event.respond("لطفاً یوزرنیم ربات را وارد کنید:")
        
    if current_step == "username":
        username = event.text
        user_cach[user_id]["username"] = username
        user_step[user_id] = "balance"
        await event.respond("لطفاً قیمت را وارد کنید:")
        
    if current_step == "balance":
        try:
            balance = float(event.text) 
            user_cach[user_id]["balance"] = balance  
            user_step[user_id] = "completed" 
            await db.create_referrabot(user_cach[user_id]['name'], user_cach[user_id]['username'], user_cach[user_id]['balance'])
            await event.respond(f"اطلاعات ربات ذخیره شد:\nنام: {user_cach[user_id]['name']}\nیوزرنیم: {user_cach[user_id]['username']}\nقیمت: {balance}")
            user_step.pop(user_id)
            user_cach.pop(user_id)
        except ValueError:
            await event.respond("لطفاً قیمت را به‌صورت عدد وارد کنید.")

@client.on(events.NewMessage(pattern="^شارژ حساب کاربر$"))
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
                await event.respond("یوزر آیدی شخص مورد نظر رو ارسال کن", buttons=keyboard)
                user_step[userid] = "user_id" 
        else:
            await event.reply(ConstText.noacsess)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage())
async def handle_charge_account(event: events.NewMessage.Event):
    global user_step, user_cach
    userid = event.sender_id

    if userid in user_step:
        step = user_step[userid]

        if step == "user_id":
            user_id = event.text
            if user_id.isdigit():
                user_cach[userid]["user_id"] = user_id
                await event.reply("چقدر می‌خواهید حساب کاربر را شارژ کنید؟")
                user_step[userid] = "charge_amount"

        elif step == "charge_amount":
            charge_amount = event.text
            if charge_amount.isdigit():
                user_cach[userid]["charge_amount"] = int(charge_amount)
                user_id = user_cach[userid]["user_id"]
                f = await db.ReadWalletUser(user_id)
                await db.UpdateWalletUser(int(user_id), int(charge_amount)+ f[0])
                keyboard = keys.key_start_sudo()
                await event.reply(f"مقدار {charge_amount} حساب کاربر {user_id} شارژ شد.",buttons=keyboard)
                await client.send_message(int(user_id), f"مقدار {charge_amount} حساب شما شارژ شد.")
                user_step.pop(userid)
                user_cach.pop(userid)
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

@client.on(events.NewMessage(pattern="^اپدیت قیمت$"))
async def update_balnce(event):
    user_id = event.sender_id
    global user_step, user_cach
    
    if user_id in user_step:
        await event.respond("شما در حال حاضر در فرآیند ساخت ربات هستید.")
        return
    user_step[user_id] = "namee" 
    user_cach[user_id] = {}
    await event.respond("لطفاً نام ربات را وارد کنید:")
    
@client.on(events.NewMessage())
async def process_update_balance(event):
    user_id = event.sender_id
    if user_id not in user_step:
        return

    current_step = user_step[user_id]
    name = event.text

    if current_step == "namee" and name != "اپدیت قیمت":
        user_cach[user_id]["namee"] = name
        user_step[user_id] = "balancee"
        await event.respond("لطفاً قیمت جدید را وارد کنید:")
        
    if current_step == "balancee":
        balancee = float(event.text) 
        user_cach[user_id]["balancee"] = balancee
        balancee = user_cach[user_id]["balancee"]
        await db.Updatebalancereferal(user_cach[user_id]["namee"],user_cach[user_id]["balancee"])
        await event.respond(f"اطلاعات ربات ذخیره شد:\nنام: {user_cach[user_id]["namee"]}\nقیمت جدید: {balancee}")
        user_step.pop(user_id)
        user_cach.pop(user_id)
            
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