from supabase import create_client
from secret_loader import SecretLoader

URL = 'https://bizxorgumhvaklsooapa.supabase.co'
KEY = SecretLoader.get('DATABASE_KEY')

database = create_client(URL, KEY)