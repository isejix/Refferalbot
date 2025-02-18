import aiosqlite

async def create_database():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER,
                role INTEGER DEFAULT 0,
                accesstypeid INTEGER DEFAULT 0,
                fname varchar
            );
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS accesstype (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid BIGINT NOT NULL,
                addadmin BIT DEFAULT 0,
                deleteadmin BIT DEFAULT 0,
                wallet BIT DEFAULT 0,
                uploadsession BIGINT BIT DEFAULT 0,
                updatebalance BIT DEFAULT 0
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid BIGINT NOT NULL,
                fname varchar,
                username varchar,
                walletus INTEGER DEFAULT 0,
                referralid BIGINT,
                score INTEGER DEFAULT 10,
                block BIT DEFAULT 0
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessions BIGINT NOT NULL UNIQUE,
                date DATETIME,
                api_id BIGINT NOT NULL,
                api_hash VARCHAR NOT NULL
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS referrabots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                botname BIGINT NOT NULL,
                username VARCHAR NOT NULL UNIQUE,
                balance FLOAT NOT NULL
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS account_referral (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id VARCHAR NOT NULL,
                bot_id VARCHAR NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts (id),
                FOREIGN KEY (bot_id) REFERENCES referrabots (id),
                UNIQUE (account_id, bot_id)
            );
        """)
   
        await db.execute("""
            CREATE TABLE IF NOT EXISTS discount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code varchar ,
                dateexpire varchar,
                countallow INT,
                countuse INT,
                percentdis INT
                
            );
        """)

        await db.commit()

# ------------------------------- CRUD for 'admin' Table -------------------------------

async def create_admin(userid, role, accesstypeid, fname):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO admin (userid, role, accesstypeid, fname)
            VALUES (?, ?, ?, ?);
            """,
            (userid, role, accesstypeid, fname),
        )
        await db.commit()

async def read_admins():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM admin") as cursor:
            return await cursor.fetchall()
        
async def ReadAdmin(AdminId):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT * FROM admin
            WHERE UserId = ?
            """, (AdminId,))
        return await Cursor.fetchone()
    
async def UpdateScoreUser(UserId: int, Score : int):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute(
            f"""
                UPDATE user SET Score = ? WHERE UserId = ?
            """,
            (Score,str(UserId)),
        )
        await conn.commit()
        
async def update_admin(id, role=None, accesstypeid=None, fname=None):
    async with aiosqlite.connect("database.db") as db:
        if role:
            await db.execute("UPDATE admin SET role = ? WHERE id = ?;", (role, id))
        if accesstypeid:
            await db.execute("UPDATE admin SET accesstypeid = ? WHERE id = ?;", (accesstypeid, id))
        if fname:
            await db.execute("UPDATE admin SET fname = ? WHERE id = ?;", (fname, id))
        await db.commit()

async def delete_admin(id):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM admin WHERE id = ?;", (id,))
        await db.commit()

# ------------------------------- CRUD for 'accesstype' Table -------------------------------

async def create_accesstype(userid, addadmin, deleteadmin, wallet, uploadsession, updatebalance):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO accesstype (userid, addadmin, deleteadmin, wallet, uploadsession, updatebalance)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (userid, addadmin, deleteadmin, wallet, uploadsession, updatebalance),
        )
        await db.commit()

async def read_accesstypes():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM accesstype;") as cursor:
            return await cursor.fetchall()
        
async def ReadAccessTypesByUserId(UserId):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT * FROM accesstype
            WHERE UserId = ?
            """, (UserId,))
        return await Cursor.fetchone()
    
async def update_accesstype(id, addadmin=None, deleteadmin=None, wallet=None, uploadsession=None, updatebalance=None):
    async with aiosqlite.connect("database.db") as db:
        if addadmin is not None:
            await db.execute("UPDATE accesstype SET addadmin = ? WHERE id = ?;", (addadmin, id))
        if deleteadmin is not None:
            await db.execute("UPDATE accesstype SET deleteadmin = ? WHERE id = ?;", (deleteadmin, id))
        if wallet is not None:
            await db.execute("UPDATE accesstype SET wallet = ? WHERE id = ?;", (wallet, id))
        if uploadsession is not None:
            await db.execute("UPDATE accesstype SET uploadsession = ? WHERE id = ?;", (uploadsession, id))
        if updatebalance is not None:
            await db.execute("UPDATE accesstype SET updatebalance = ? WHERE id = ?;", (updatebalance, id))
        await db.commit()

async def delete_accesstype(id):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM accesstype WHERE id = ?;", (id,))
        await db.commit()

# ------------------------------- CRUD for 'user' Table -------------------------------

async def create_user(userid, fname, username ,walletus, referralid, score, block):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO user (userid, fname, username, walletus, referralid, score, block)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (userid, fname, username, walletus, referralid, score, block),
        )
        await db.commit()

async def read_users():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM user;") as cursor:
            return await cursor.fetchall()
        
async def ReadUserByUserId(UserId):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT * FROM user
            WHERE UserId = ?
            """, (str(UserId),))
        return await Cursor.fetchone()
    
async def ReadWalletUser(UserId):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT walletus FROM user
            WHERE UserId = ?
            """, (UserId,))
        result =  await Cursor.fetchall()
        if result:
                return result[0]
    
async def UpdateWalletUser(UserId: int, walletus : int):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute(
            f"""
                UPDATE user SET walletus = ? WHERE UserId = ?
            """,
            (walletus,str(UserId)),
        )
        await conn.commit()

async def blockN_User(UserId: int, block : int):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute(
            f"""
                UPDATE user SET block = ? WHERE UserId = ?
            """,
            (block,str(UserId)),
        )
        await conn.commit()
               
async def delete_user(id : int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM user WHERE userid = ?;", (id,))
        await db.commit()
        
async def delete_wallet_user(id):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("UPDATE user SET walletus = ? WHERE userid = ?;", (0, id))
        await db.commit()



# ------------------------------- CRUD for 'wallet' Table -------------------------------

async def create_wallet(userid, balance):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO wallet (userid, balance)
            VALUES (?, ?);
            """,
            (userid, balance),
        )
        await db.commit()

async def read_wallets():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM wallet;") as cursor:
            return await cursor.fetchall()

async def update_wallet(id, balance):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("UPDATE wallet SET balance = ? WHERE id = ?;", (balance, id))
        await db.commit()

async def delete_wallet(id):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM wallet WHERE id = ?;", (id,))
        await db.commit()

# ------------------------------- CRUD for 'referrabots' Table -------------------------------

async def create_referrabot(botname:str, username:str, balance: float ):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO referrabots (botname, username, balance)
            VALUES (?, ?, ?);
            """,
            (str(botname), str(username), int(float(balance))),
        )
        await db.commit()

async def read_referrabots():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM referrabots;") as cursor:
            return await cursor.fetchall()

async def read_referrabot_name(botname : str):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT botname FROM referrabots
            WHERE username = ?
            """, (str(botname),))
        return await Cursor.fetchone()

async def read_referrabotbyname(botname : str):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT botname , username , balance FROM referrabots
            WHERE username = ?
            """, (str(botname),))
        return await Cursor.fetchone()

async def read_balance_referrabotbyname(botname : str):
    async with aiosqlite.connect("database.db") as conn:
        Cursor = await conn.execute("""
            SELECT balance FROM referrabots
            WHERE botname = ?
            """, (str(botname),))
        return await Cursor.fetchone()
    
async def Updatebalancereferal(botname: str, balance : float):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute(
            f"""
                UPDATE referrabots SET balance = ? WHERE username = ?
            """,
            (float(balance),botname),
        )
        await conn.commit()
        
async def delete_referrabot(botname: str):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM referrabots WHERE username = ?;", (botname,))
        await db.commit()

# ------------------------------- CRUD for 'accounts' Table -------------------------------

async def create_account(phone: int, date):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT INTO accounts (sessions, date)
            VALUES (?, ?);
        """, (int(phone),date))
        await db.commit()

async def read_account(date):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM accounts WHERE date = ?", (date,)) as cursor:
            await cursor.fetchone()

async def read_accounts(sessions):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT sessions FROM accounts WHERE sessions = ?", (sessions,)) as cursor:
            await cursor.fetchone()
            
async def read_accounts_api(sessions):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT api_id , api_hash  FROM accounts WHERE sessions = ?", (sessions,)) as cursor:
            await cursor.fetchone()
            
# ------------------------------- CRUD for 'dicount' Table -------------------------------

async def create_discount(code: str, dateexpire:str, countallow:int,countuse:int, percentdis:int):
    """ایجاد کد تخفیف جدید."""
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            INSERT INTO discount (code, dateexpire, countallow, countuse, percentdis)
            VALUES (?, ?, ?, ?, ?);
            """,
            (code, dateexpire, countallow,countuse, percentdis),
        )
        await db.commit()
        
async def update_discount(code: str):
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT countuse FROM discount WHERE code = ?", (code,))
        result = await cursor.fetchone()
        
        if result:
            current_count = result[0] if result[0] else 0
            if current_count > 0:
                new_count = current_count - 1
                await db.execute(
                    """
                    UPDATE discount SET countuse = ? WHERE code = ?
                    """,
                    (new_count, code),
                )
                await db.commit()

async def read_discounts():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM discount;") as cursor:
            return await cursor.fetchall()

async def read_discount(code):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM discount WHERE code = ?;", (code,)) as cursor:
            return await cursor.fetchone()

async def delete_discount(code):
    """حذف کد تخفیف بر اساس `code`."""
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM discount WHERE code = ?;", (code,))
        await db.commit()

async def delete_expired_discounts(datee):
    """حذف کدهای تخفیف منقضی‌شده."""
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM discount WHERE dateexpire < ?;", (datee,))
        await db.commit()

async def is_bot_already_started(session_id, bot_username):
    query = """
    SELECT 1
    FROM account_referral
    WHERE account_id = (SELECT id FROM accounts WHERE sessions = ?)
      AND bot_id = (SELECT id FROM referrabots WHERE username = ?)
    """
    async with aiosqlite.connect("database.db") as db:
        async with db.execute(query, (session_id, bot_username)) as cursor:
            result = await cursor.fetchone()
    return result is not None

async def add_start(session_id, bot_username):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO accounts (sessions) VALUES (?)
        """, (session_id,))
        
        account_id = await db.execute("SELECT id FROM accounts WHERE sessions = ?", (session_id,))
        account_id = await account_id.fetchone()
        account_id = account_id[0] if account_id else None
        
        await db.execute("""
            INSERT OR IGNORE INTO referrabots (botname, username, balance) VALUES (?, ?, 0)
        """, ("Bot Name", bot_username))
        
        bot_id = await db.execute("SELECT id FROM referrabots WHERE username = ?", (bot_username,))
        bot_id = await bot_id.fetchone()
        bot_id = bot_id[0] if bot_id else None
        
        try:
            if account_id and bot_id:
                await db.execute("""
                    INSERT INTO account_referral (account_id, bot_id) VALUES (?, ?)
                """, (account_id, bot_id))
            else:
                print("خطا در یافتن account_id یا bot_id")
        except Exception as e:
            print("این سشن قبلاً این ربات را استارت کرده:", e)

