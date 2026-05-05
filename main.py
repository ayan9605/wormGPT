from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn
from pydantic import BaseModel
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager

from config import load_config, save_config, CONFIG_FILE
from models import ChatRequest, ConfigUpdate
from prompts import get_jailbreak_prompt
from utils import banner_html, colors, typing_stream

app = FastAPI(title="WormGPT API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global config
config_cache = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global config_cache
    if not os.path.exists(CONFIG_FILE):
        config_cache = save_config(load_config())
    else:
        config_cache = load_config()
    yield
    # Shutdown

app.router.lifespan_context = lifespan

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main dashboard"""
    return HTMLResponse(content=banner_html())

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": config_cache.get("model", "deepseek/deepseek-chat-v3-0324:free")
    }

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "config": config_cache,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/config")
async def update_config(update: ConfigUpdate):
    """Update configuration"""
    global config_cache
    config_cache = load_config()
    
    if update.api_key is not None:
        config_cache["api_key"] = update.api_key
    if update.model is not None:
        config_cache["model"] = update.model
    if update.language is not None:
        config_cache["language"] = update.language
    
    save_config(config_cache)
    return {"status": "updated", "config": config_cache}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint - returns full response"""
    try:
        response = await call_api(request.message)
        return {
            "response": response,
            "model": config_cache["model"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint - real-time response"""
    async def generate():
        try:
            response = await call_api(request.message)
            # Simulate typing effect with streaming
            for chunk in typing_stream(response):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")

async def call_api(user_input: str) -> str:
    """Core API calling logic"""
    import requests
    from langdetect import detect
    
    # Auto-detect language
    try:
        detected_lang = detect(user_input[:500])
        lang_map = {'id':'Indonesian','en':'English','es':'Spanish','ar':'Arabic','th':'Thai','pt':'Portuguese'}
        detected_lang = lang_map.get(detected_lang, 'English')
        if detected_lang != config_cache["language"]:
            config_cache["language"] = detected_lang
            save_config(config_cache)
    except:
        pass
    
    headers = {
        "Authorization": f"Bearer {config_cache['api_key']}",
        "HTTP-Referer": "https://github.com/00x0kafyy/worm-ai",
        "X-Title": "WormGPT API",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": config_cache["model"],
        "messages": [
            {"role": "system", "content": get_jailbreak_prompt()},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{config_cache['base_url']}/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

@app.get("/banner")
async def get_banner():
    """Get ASCII banner for CLI-like experience"""
    return {"banner": banner_html(ascii=True)}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
