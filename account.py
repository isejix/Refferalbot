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
        
        if not await client.is_user_authorized():
            print(f"Session {session} is not authorized.")
            await client.disconnect()
            return False

        else:
            if await client.is_connected():
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
    except OSError:
        print("Error occurred during disconnection.")
    
    finally:
        if client.is_connected():
            await client.disconnect()
        
        print("Client disconnected successfully.")

    


async def acc_start_ref(session, username, keyrefral):
    client = TelegramClient(session, api_id, api_hash)
    
    if not client.is_connected():
        await client.connect()

    try:

        peer = await client(ResolveUsernameRequest(username))
        print(f"Resolved Peer: {peer}")
    except Exception as e:
        print(f"Error resolving username: {e}")
        await client.disconnect()
        return False

    try:
        request = StartBotRequest(bot=peer.peer, peer=peer.peer, start_param=keyrefral)
        result = await client(request)
        
        if result:
            print("Bot started successfully!")
            return True
        else:
            print("Failed to start bot.")
            return False
    except Exception as e:
        print(f"Error starting bot: {e}")
    
    await client.disconnect()
    return False

