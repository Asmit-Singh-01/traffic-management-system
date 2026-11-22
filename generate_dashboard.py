 import json
from metrics import load_telemetry, compute_latency_reduction


def generate_dashboard() -> None:
    telemetry = load_telemetry("telemetry.json")
    avg_delay = telemetry["avg_queue_delay"]
    peak_flow = telemetry["peak_throughput"]
    recovery_ticks = telemetry["recovery_ticks"]
    latest_delays = telemetry["latest_delays"]
    reduction_pct = compute_latency_reduction(42.8, avg_delay)

    labels = [f"T-{len(latest_delays) - i - 1}" if i < len(latest_delays) - 1 else "Live"
              for i in range(len(latest_delays))]
    legacy_series = [44.0, 43.0, 46.0, 42.0, 45.0, 41.0, 42.8][-len(latest_delays):]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DATG - Decentralized Autonomous Traffic Grid</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --accent-green: #2ea043;
            --accent-blue: #58a6ff;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --border: #30363d;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 30px;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 30px;
            gap: 12px;
            flex-wrap: wrap;
        }}
        h1 {{ margin: 0; font-size: 24px; color: #fff; font-weight: 800; }}
        .badge {{
            background: rgba(46, 160, 67, 0.15);
            color: var(--accent-green);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid var(--accent-green);
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 22px;
        }}
        .card h3 {{ margin: 0 0 10px 0; color: var(--text-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric-val {{ font-size: 32px; font-weight: 800; color: #fff; }}
        .chart-box {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>DATG: Decentralized Autonomous Traffic Grid</h1>
        <div class="badge">Mesh + YOLO + SUMO + RL Active</div>
    </header>

    <div class="metrics-grid">
        <div class="card">
            <h3>Peak Flow Throughput</h3>
            <div class="metric-val">{peak_flow} <span style="font-size:15px; color:var(--accent-green);">veh/cycle</span></div>
        </div>
        <div class="card">
            <h3>Average Queue Delay</h3>
            <div class="metric-val">{avg_delay} <span style="font-size:15px; color:var(--accent-blue);">sec ({reduction_pct}% vs baseline)</span></div>
        </div>
        <div class="card">
            <h3>System Resilience</h3>
            <div class="metric-val" style="color: var(--accent-green);">{recovery_ticks} Ticks</div>
        </div>
    </div>

    <div class="chart-box">
        <h3 style="color:#fff; margin-top:0; margin-bottom:20px;">Queue Delay Trend: Legacy vs DATG Agent</h3>
        <canvas id="mainChart" height="110"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('mainChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Legacy Static Signal Delay (s)',
                    data: {json.dumps(legacy_series)},
                    borderColor: '#f85149',
                    backgroundColor: 'rgba(248, 81, 73, 0.08)',
                    borderWidth: 2,
                    tension: 0.35
                }}, {{
                    label: 'DATG Autonomous Agent (s)',
                    data: {json.dumps(latest_delays)},
                    borderColor: '#2ea043',
                    backgroundColor: 'rgba(46, 160, 67, 0.08)',
                    borderWidth: 2,
                    tension: 0.35
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: '#c9d1d9' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#30363d' }} }},
                    y: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#30363d' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard HTML generated with live telemetry.")


if __name__ == "__main__":
    generate_dashboard()
    
