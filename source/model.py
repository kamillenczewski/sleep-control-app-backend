from google.generativeai import configure, GenerativeModel
from tools import readFile, createPath
from secret_loader import SecretLoader

KEY = SecretLoader.get('MODEL_KEY')

MODEL_NAME = 'gemini-1.5-flash'

configure(api_key=KEY)

model = GenerativeModel(MODEL_NAME)
data = readFile(createPath('data.json'))


