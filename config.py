import os


# url = 'https://studentinfo.bdu.edu.et/login.aspx?ReturnUrl=%2f'
# db = 'mongodb+srv://jdlix:0lnTxEJ4nHMC1BQW@cluster0.t55x8bv.mongodb.net/?retryWrites=true&w=majority'

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
DB_URL = os.environ.get("DB_URL", "")
SITE_URL = os.environ.get("SITE_URL", "")