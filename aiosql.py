import aiosqlite

DB_NAME = 'quiz_bot_1.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state_2 (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER PRIMARY KEY, question_index INTEGER, status INTEGER )''')
        await db.commit()

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state_2(user_id, question_index) VALUES (?, ?)', (user_id,index))
        await db.commit()

async def update_quiz_status(user_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results(user_id, status) VALUES (?, ?)', (user_id,status))
        await db.commit()

async def get_status(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT status FROM quiz_results WHERE user_id = (?)', (user_id,)) as cursor:
            status_results = await cursor.fetchone()
            if status_results is not None:
                return status_results[0]
            else:
                return 0

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state_2 WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def start_new_quiz(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
        await db.commit()