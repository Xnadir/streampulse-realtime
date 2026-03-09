# WebSocket Protocol

## Connection

Connect to `ws://localhost:8000/ws`

## Messages (Server to Client)

```json
{"type": "stream_item", "data": {"id": "uuid", "text": "...", "sentiment": "positive", "score": 0.85}}
```

## Commands (Client to Server)

| Command | Action |
|---------|--------|
| `start` | Begin streaming |
| `stop`  | Pause stream |
