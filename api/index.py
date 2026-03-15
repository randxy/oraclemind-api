from flask import Flask, jsonify, request

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

# --- 1. HALAMAN UTAMA (HTML) ---
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OracleMind AI Agent</title>
        <style>
            body {
                background-color: #0d1117; color: #c9d1d9;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                display: flex; justify-content: center; align-items: center;
                height: 100vh; margin: 0;
            }
            .container {
                text-align: center; padding: 50px; border: 1px solid #30363d;
                border-radius: 15px; background-color: #161b22;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5); max-width: 500px;
            }
            h1 { color: #58a6ff; margin-bottom: 10px; }
            p { font-size: 16px; line-height: 1.5; color: #8b949e; margin-bottom: 30px; }
            .status-badge {
                padding: 8px 16px; background-color: #238636; color: #ffffff;
                border-radius: 20px; font-size: 14px; font-weight: bold;
                display: inline-block; border: 1px solid #2ea043;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OracleMind AI</h1>
            <p>AI oracle specialized in prediction markets and global sentiment analysis. Aggregates data from decentralized prediction markets and social platforms to forecast outcomes and provide actionable intelligence on the Base network.</p>
            <div class="status-badge">🟢 System Online & Healthy</div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- 2. ENDPOINT MCP ---
@app.route('/mcp', methods=['GET', 'POST', 'OPTIONS'])
def mcp_endpoint():
    server_info = {
        "name": "OracleMind Agent Server",
        "version": "1.0.0",
        "website": "https://oraclemind-api.vercel.app",
        "description": "Prediction market and sentiment oracle agent"
    }
    tools = [
        {"name": "analyze_prediction_markets", "description": "Fetch and analyze odds from decentralized prediction platforms", "inputSchema": {"type": "object","properties": {}}},
        {"name": "aggregate_social_sentiment", "description": "Calculate global sentiment scores from social graphs", "inputSchema": {"type": "object","properties": {}}},
        {"name": "forecast_outcome_probability", "description": "Generate probabilistic models for real-world events", "inputSchema": {"type": "object","properties": {}}}
    ]
    prompts = [
        {"name": "sentiment_trend_report", "description": "Generate report on shifting sentiment regarding a specific protocol", "arguments": []},
        {"name": "market_probability_analysis", "description": "Cross-reference prediction market odds with on-chain data", "arguments": []}
    ]
    
    if request.method == 'GET':
        return jsonify({
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "tools": tools,
            "prompts": prompts,
            "resources": [] 
        })

    req_data = request.get_json(silent=True) or {}
    req_id = req_data.get("id", 1)
    method = req_data.get("method", "")

    if method == "tools/list":
        result = {"tools": tools}
    elif method == "prompts/list":
        result = {"prompts": prompts}
    else:
        result = {
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "capabilities": {"tools": {},"prompts": {},"resources": {}}
        }

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

# --- 3. ENDPOINT A2A (ID AKUN 14: 22381) ---
@app.route('/.well-known/agent-card.json', methods=['GET','OPTIONS'])
def a2a_endpoint():
    return jsonify({
        "id": "oraclemind",
        "name": "oraclemind",
        "version": "1.0.0",
        "description": "AI oracle specialized in prediction markets and global sentiment analysis. Aggregates data from decentralized prediction markets and social platforms to forecast outcomes and provide actionable intelligence on the Base network.",
        "website": "https://oraclemind-api.vercel.app",
        "url": "https://oraclemind-api.vercel.app",
        "documentation_url": "https://oraclemind-api.vercel.app",
        "provider": {
            "organization": "OracleMind Analytics",
            "url": "https://oraclemind-api.vercel.app"
        },
        "registrations": [
            {
                "agentId": 22381,
                "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
            }
        ],
        "supportedTrust": ["reputation", "tee-attestation"],
        "skills": [
            {"name": "Prediction Analysis", "description": "Analyze decentralized betting odds", "category": "market/prediction_analysis"},
            {"name": "Sentiment Aggregation", "description": "Process global social graph data", "category": "data/sentiment_aggregation"},
            {"name": "Probability Forecasting", "description": "Calculate event likelihood", "category": "finance/probability_forecasting"}
        ]
    })

# --- 4. ENDPOINT OASF ---
@app.route('/oasf', methods=['GET','OPTIONS'])
def oasf_endpoint():
    return jsonify({
        "id": "oraclemind",
        "name": "oraclemind",
        "version": "v0.8.0",
        "description": "Main endpoint for OracleMind AI",
        "website": "https://oraclemind-api.vercel.app",
        "protocols": ["mcp","a2a"],
        "capabilities": ["analyze_prediction_markets", "aggregate_social_sentiment", "forecast_outcome_probability"],
        "skills": [
            {"name": "market/prediction_analysis","type": "analytical"},
            {"name": "data/sentiment_aggregation","type": "analytical"},
            {"name": "finance/probability_forecasting","type": "analytical"}
        ],
        "domains": [
            "web3/prediction_markets",
            "data/sentiment",
            "finance/forecasting"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
