from telethon import TelegramClient

api_id = 2631644
api_hash = '2a0dec0b80b84e501c5d9806248eb235'


proxyx = {
    'proxy_type': 'socks5',  # Can be 'socks5', 'http', or 'https'
    'proxy_host': '127.0.0.1',  # Proxy server address
    'proxy_port': 2080  # Proxy server port
}

async def check_status_sessions(session):
    client = TelegramClient(session, api_id, api_hash)
    if await client.connect():
        return True
    await client.disconnect()
    return False  

