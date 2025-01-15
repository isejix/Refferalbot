from telethon import TelegramClient, events,Button
import keys
import db
import ConstText
from socks import SOCKS5, SOCKS4, HTTP

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

@client.on(events.NewMessage(pattern="/start"))
async def start_bot(event):
    userid = event.sender_id
    text = event.raw_text

    if text == "/start":
        anyadmin = await db.ReadAdmin(userid)
        if anyadmin is None:
            isany = await db.ReadUserByUserId(userid)
            if isany is None:
                await db.create_user(userid,0,0,10,event.sender.first_name,0)
                isany = await db.ReadUserByUserId(userid)

            if isany[6] == 0:
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
                await db.create_user(userid,0,0,10,event.sender.first_name,0)

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
@client.on(events.NewMessage(pattern="قوانین و راهنما 💡"))
async def start_bot(event):
    userid = event.sender_id
    await client.send_message(
                            userid,
                            ConstText.rules
                        )
    
    
def is_sudo(userid:int):
    sudo = [6785692975]
    if userid in sudo:
        return True
    return False

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