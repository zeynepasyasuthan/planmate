import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE = "planmate.db"

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN bulunamadı.")