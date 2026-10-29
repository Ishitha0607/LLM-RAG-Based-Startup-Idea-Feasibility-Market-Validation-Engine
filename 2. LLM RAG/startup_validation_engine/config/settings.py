import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Startup AI"
APP_TITLE = "Startup Validation Engine"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# RAG configuration
TOP_K = 5

# Validation categories
VALIDATION_CATEGORIES = [
    "Market Evidence",
    "Customer Pain",
    "Competition",
    "Market Gap",
    "Technical Feasibility",
]

# Application pages
PAGES = [
    "Home",
    "Dashboard",
    "Market Analysis",
    "Customer Pain",
    "Competition",
    "Market Gap",
    "Technical Feasibility",
    "Validation Score",
    "Final Report",
]
