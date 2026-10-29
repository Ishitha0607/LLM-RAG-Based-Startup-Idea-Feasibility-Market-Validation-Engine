PAGE_ICONS = {
    "Home": "🏠",
    "Dashboard": "📊",
    "Market Analysis": "📈",
    "Customer Pain": "👥",
    "Competition": "⚔️",
    "Market Gap": "🔎",
    "Technical Feasibility": "⚙️",
    "Validation Score": "🎯",
    "Final Report": "📄",
}


def get_page_icon(page_name):
    return PAGE_ICONS.get(page_name, "📌")


def get_page_title(page_name):
    icon = get_page_icon(page_name)
    return f"{icon} {page_name}"
