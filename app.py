"""
StreamPulse — FastAPI + WebSocket server for real-time AI analytics
Run with: python app.py
"""

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from stream import generate_stream_item

app = FastAPI(title="StreamPulse")
app.mount("/static", StaticFiles(directory="static"), name="static")

# track connected clients
clients: list[WebSocket] = []
stream_active = False


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "connected_clients": len(clients),
        "stream_active": stream_active
    }
stream_stats = {"total": 0, "positive": 0, "negative": 0, "neutral": 0, "anomalies": 0}


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global stream_active
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)

            if msg.get("action") == "start":
                stream_active = True
                asyncio.create_task(stream_data(ws))
            elif msg.get("action") == "stop":
                stream_active = False


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "connected_clients": len(clients),
        "stream_active": stream_active
    }
            elif msg.get("action") == "reset":
                stream_stats.update({"total": 0, "positive": 0, "negative": 0, "neutral": 0, "anomalies": 0})
                await ws.send_text(json.dumps({"type": "stats", "data": stream_stats}))

    except WebSocketDisconnect:
        clients.remove(ws)
        stream_active = False


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "connected_clients": len(clients),
        "stream_active": stream_active
    }


async def stream_data(ws: WebSocket):
    """Generate and send stream items at random intervals."""
    global stream_active

    while stream_active:
        try:
            item = await generate_stream_item()

            # update stats
            stream_stats["total"] += 1
            stream_stats[item["sentiment"]] += 1
            if item["is_anomaly"]:
                stream_stats["anomalies"] += 1

            # send item + stats
            await ws.send_text(json.dumps({"type": "item", "data": item}))
            await ws.send_text(json.dumps({"type": "stats", "data": stream_stats}))

            # random delay between 0.5-2 seconds
            await asyncio.sleep(0.5 + (hash(item["id"]) % 15) / 10)

        except Exception:
            stream_active = False


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "connected_clients": len(clients),
        "stream_active": stream_active
    }
            break


@app.get("/api/stats")
async def stats():
    return stream_stats


if __name__ == "__main__":
    print("\n📡 Starting StreamPulse Real-Time AI...")
    print("   Open http://localhost:8000 in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
