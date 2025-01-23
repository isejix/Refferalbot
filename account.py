from telethon import TelegramClient
from telethon.tl.functions.messages import StartBotRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors import SessionPasswordNeededError, AuthKeyError
from asyncio import run

api_id = 2631644
api_hash = '2a0dec0b80b84e501c5d9806248eb235'


proxyx = {
    'proxy_type': 'socks5',  # Can be 'socks5', 'http', or 'https'
    'proxy_host': '127.0.0.1',  # Proxy server address
    'proxy_port': 2080  # Proxy server port
}


async def check_status_sessions(session):
    client = TelegramClient(session, api_id, api_hash)
    try:
        await client.connect()
        # چک کردن اینکه سشن معتبر است یا نه
        if not await client.is_user_authorized():
            print(f"Session {session} is not authorized.")
            return False
        
        print(f"Session {session} is valid and authorized.")
        return True
    except (AuthKeyError, FileNotFoundError):
        print(f"Session {session} is invalid or corrupted.")
        return False
    except ConnectionError:
        print(f"Network error while checking session {session}.")
        return False
    except SessionPasswordNeededError:
        print(f"Session {session} requires two-factor authentication.")
        return False
    finally:
        await client.disconnect()
    
    


async def acc_start_ref(session):
    client = TelegramClient(session, api_id, api_hash)
    
    await client.connect()
    if not await client.is_user_authorized():
        print("Client is not authorized. Please log in.")
        return False
    x = await client.get_me()
    print(x)
    try:
        peer = await client(ResolveUsernameRequest("hamster_kombAt_bot"))
        print(f"Resolved Peer: {peer}")
    except Exception as e:
        print(f"Error resolving username: {e}")
        await client.disconnect()
        return False
    
    try:
        request = StartBotRequest(bot=peer.peer, peer=peer.peer, start_param="startapp=kentId6199439097")
        result = await client(request)
        print("Bot started successfully:", result)
    except Exception as e:
        print(f"Error starting bot: {e}")
    
    await client.disconnect()
    return True

