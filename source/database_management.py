from supabase import create_client
from tools import getSecret

URL = 'https://bizxorgumhvaklsooapa.supabase.co'
KEY = getSecret('DATABASE_KEY')

database = create_client(URL, KEY)