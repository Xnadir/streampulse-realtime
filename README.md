# StreamPulse — Real-Time AI Analytics 📡

A real-time AI dashboard that processes streaming data with WebSockets. Monitors live text streams, performs instant sentiment analysis, detects anomalies, and shows the results on a live-updating dashboard.

This is the most technically challenging project in the portfolio — it demonstrates real-time AI inference at scale, something companies like Twitter, Discord, and Datadog need constantly.

## Features

- **WebSocket streaming** — real-time bidirectional communication
- **Live sentiment analysis** — AI classifies incoming text in real-time
- **Anomaly detection** — flags unusual patterns in the data stream
- **Live metrics dashboard** — updating charts and counters
- **Stream simulator** — generates realistic mock data for demo
- **Connection management** — handles reconnection gracefully

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/streampulse-realtime.git
cd streampulse-realtime

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

echo GEMINI_API_KEY=your_key_here > .env

python app.py
```

Open `http://localhost:8000`. Click "Start Stream" to begin.

## How It Works

```
Data Source → WebSocket → AI Inference → Dashboard
    ↓             ↓            ↓            ↓
 Generator    FastAPI     Gemini API    Live Charts
```

1. **Stream simulator** generates realistic messages (product reviews, social posts, alerts)
2. **WebSocket server** pushes messages to connected clients in real-time
3. **AI processor** analyzes each message for sentiment and anomalies
4. **Dashboard** updates live with counters, recent items, and distribution charts

## Tech Stack

- **Backend:** Python, FastAPI, WebSockets
- **AI:** Google Gemini API
- **Frontend:** HTML, CSS, JavaScript, Canvas API
- **Streaming:** asyncio + WebSocket protocol

## Project Structure

```
streampulse-realtime/
├── app.py              # FastAPI + WebSocket server
├── stream.py           # Data stream simulator + AI processor
├── requirements.txt
├── .env.example
├── static/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

## License

MIT
