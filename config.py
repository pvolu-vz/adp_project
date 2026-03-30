# Configuration constants for ADP API project
import os
from dotenv import load_dotenv

load_dotenv()

ADP_TOKEN_URL = "https://accounts.adp.com/auth/oauth/v2/token"
EMPLOYEE_API_URL = "https://api.adp.com/hr/v2/workers"
CLIENT_ID = os.getenv("ADP_CLIENT_ID")
CLIENT_SECRET = os.getenv("ADP_CLIENT_SECRET")
CLIENT_CERT_FILE = os.getenv("ADP_CLIENT_CERT_FILE")
CLIENT_KEY_FILE = os.getenv("ADP_CLIENT_KEY_FILE")
PAGE_SIZE = 100
VEZA_URL = os.getenv("VEZA_URL")
VEZA_API_KEY = os.getenv("VEZA_API_KEY")
introspect_url = "https://accounts.adp.com/auth/oauth/v2/token/introspect"
status_url = "https://api.adp.com/core/v1/status"
