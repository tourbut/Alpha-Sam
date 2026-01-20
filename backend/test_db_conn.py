import asyncpg
import asyncio

async def test():
    try:
        conn = await asyncpg.connect('postgresql://postgres:postgres@db:5432/alpha_sam')
        print('Connected from backend to db!')
        await conn.close()
    except Exception as e:
        print(f'Failed: {e}')

if __name__ == "__main__":
    asyncio.run(test())
