"""Centralized file extension to category mapping."""

CATEGORY_EXTENSIONS: dict[str, set[str]] = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".zst"},
    "Code": {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".yaml", ".yml", ".toml", ".sh", ".c", ".cpp", ".rs", ".go", ".java", ".sql"},
    "Installers": {".deb", ".rpm", ".appimage", ".pkg", ".iso", ".exe", ".msi", ".dmg"},
}

DEFAULT_CATEGORY = "Others"
HISTORY_FILENAME = ".tidy_history.json"
