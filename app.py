import os
import requests
from flask import Flask, jsonify, render_template
from strategy import calculate_signal

app = Flask(__name__)

API_KEY = os.environ.get("TWELVE_DATA_API_KEY", "")


def get_candles(interval, outputsize=250):
    if not API_KEY:
        return None, "API key is not configured"

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": "USD/JPY",
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        if "values" not in data:
            return None, data.get("message", "Market data unavailable")

        values = data["values"]
        values.reverse()

        closes = [float(item["close"]) for item in values]

        return closes, None

    except Exception as error:
        return None, str(error)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    candles_15m, error_15m = get_candles("15min")
    candles_1h, error_1h = get_candles("1h")

    if error_15m or error_1h:
        return jsonify({
            "status": "error",
            "message": error_15m or error_1h
        }), 503

    signal_15m = calculate_signal(candles_15m)
    signal_1h = calculate_signal(candles_1h)

    return jsonify({
        "status": "live",
        "symbol": "USD/JPY",
        "timeframe_15m": signal_15m,
        "timeframe_1h": signal_1h
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
