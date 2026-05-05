import json
from typing import Iterator
import pyfiglet
from datetime import datetime

class colors:
    reset = "\033[0m"
    bright_red = "\033[1;31m"
    bright_cyan = "\033[1;36m"
    bright_green = "\033[1;32m"
    bright_yellow = "\033[1;33m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"

def banner_html(ascii: bool = False) -> str:
    """Generate HTML banner"""
    if ascii:
        try:
            figlet = pyfiglet.Figlet(font="big")
            banner = figlet.renderText('WormGPT')
        except:
            banner = "WormGPT"
        return f"""
{colors.bright_red}{banner}{colors.reset}
{colors.bright_red}WormGPT API{colors.reset}
{colors.bright_cyan}OpenRouter API | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{colors.reset}
"""
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>WormGPT API</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; padding: 2rem; }}
        .banner {{ font-size: 2rem; color: #ff4444; font-weight: bold; }}
        .info {{ color: #44ff44; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        pre {{ background: #1a1a1a; padding: 1rem; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="banner">🐛 WORMGPT API</div>
        <div class="info">
            <p>🚀 FastAPI Server | <span id="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></p>
            <p>🔗 <a href="/docs" style="color: #44ffff;">Swagger UI</a> | <a href="/redoc" style="color: #44ffff;">ReDoc</a></p>
        </div>
        <pre>
POST /chat          - Regular chat
POST /chat/stream   - Streaming response  
GET  /config        - Get config
POST /config        - Update config
GET  /health        - Health check
        </pre>
    </div>
    <script>
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
"""

def typing_stream(text: str) -> Iterator[str]:
    """Generate streaming chunks with typing effect"""
    chunk_size = 1
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
