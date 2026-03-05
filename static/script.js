let ws = null;
let isStreaming = false;

const feed = document.getElementById('feed');
const status = document.getElementById('status');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');

function connect() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${location.host}/ws`);

    ws.onopen = () => {
        status.textContent = '🟢 Connected';
        status.className = 'status connected';
    };

    ws.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        if (msg.type === 'item') renderItem(msg.data);
        if (msg.type === 'stats') updateStats(msg.data);
    };

    ws.onclose = () => {
        status.textContent = '⚪ Disconnected';
        status.className = 'status';
        isStreaming = false;
        startBtn.classList.remove('hidden');
        stopBtn.classList.add('hidden');
        // reconnect after 2s
        setTimeout(connect, 2000);
    };

    ws.onerror = () => ws.close();
}

function startStream() {
    if (!ws || ws.readyState !== WebSocket.OPEN) { connect(); setTimeout(startStream, 500); return; }
    ws.send(JSON.stringify({ action: 'start' }));
    isStreaming = true;
    startBtn.classList.add('hidden');
    stopBtn.classList.remove('hidden');
    status.textContent = '🟢 Streaming';
    status.className = 'status streaming';
}

function stopStream() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'stop' }));
    }
    isStreaming = false;
    startBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');
    status.textContent = '🟢 Connected';
    status.className = 'status connected';
}

function resetStats() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'reset' }));
    }
    feed.innerHTML = '';
    document.getElementById('total').textContent = '0';
    document.getElementById('positive').textContent = '0';
    document.getElementById('negative').textContent = '0';
    document.getElementById('anomalies').textContent = '0';
}

function renderItem(item) {
    const div = document.createElement('div');
    div.className = 'feed-item';
    div.innerHTML = `
        <div class="feed-msg">${escapeHtml(item.message)}</div>
        <div class="feed-meta">
            <span class="feed-badge bg-${item.sentiment}">${item.sentiment}</span>
            ${item.is_anomaly ? '<span class="feed-badge bg-anomaly">⚠ anomaly</span>' : ''}
            <span class="feed-src">${item.source} · ${item.confidence}</span>
        </div>
    `;

    feed.insertBefore(div, feed.firstChild);
    // keep max 50 items
    while (feed.children.length > 50) feed.removeChild(feed.lastChild);
}

function updateStats(stats) {
    animateValue('total', stats.total);
    animateValue('positive', stats.positive);
    animateValue('negative', stats.negative);
    animateValue('anomalies', stats.anomalies);
    drawChart(stats);
}

function animateValue(id, val) {
    document.getElementById(id).textContent = val;
}

function drawChart(stats) {
    const canvas = document.getElementById('distChart');
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const total = stats.positive + stats.negative + stats.neutral;
    if (total === 0) return;

    const bars = [
        { label: 'Positive', value: stats.positive, color: '#22c55e' },
        { label: 'Neutral', value: stats.neutral || 0, color: '#6b7280' },
        { label: 'Negative', value: stats.negative, color: '#ef4444' },
    ];

    const barW = 80, gap = 40, startX = (w - (bars.length * barW + (bars.length - 1) * gap)) / 2;
    const maxVal = Math.max(...bars.map(b => b.value), 1);

    bars.forEach((bar, i) => {
        const x = startX + i * (barW + gap);
        const barH = (bar.value / maxVal) * (h - 60);
        const y = h - 30 - barH;

        // bar
        ctx.fillStyle = bar.color;
        ctx.beginPath();
        ctx.roundRect(x, y, barW, barH, 4);
        ctx.fill();

        // value
        ctx.fillStyle = '#e8e8f0';
        ctx.font = 'bold 14px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(bar.value, x + barW / 2, y - 8);

        // label
        ctx.fillStyle = '#888';
        ctx.font = '11px Inter';
        ctx.fillText(bar.label, x + barW / 2, h - 10);
    });
}

function escapeHtml(t) { return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// auto-connect
connect();
