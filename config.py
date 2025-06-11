# Configuration for OCR Camera App

# DeepSeek API Configuration
# Sign up at https://platform.deepseek.com to get your API key
# For the free tier, you can use any string as the API key
DEEPSEEK_API_KEY = "sk-xxx"
DEEPSEEK_BASE_URL = "https://openrouter.ai/api/v1"

# OCR Configuration
OCR_LANGUAGES = ['en', 'id']  # English and Indonesian
OCR_CONFIDENCE_THRESHOLD = 0.3

# Flask Configuration
SECRET_KEY = 'your-secret-key-here-change-this-in-production'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
