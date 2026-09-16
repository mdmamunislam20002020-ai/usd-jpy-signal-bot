def ema(values, period):
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)
    result = sum(values[:period]) / period

    for price in values[period:]:
        result = (price - result) * multiplier + result

    return result


def rsi(values, period=14):
    if len(values) <= period:
        return 50.0

    gains = []
    losses = []

    for i in range(1, len(values)):
        change = values[i] - values[i - 1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_signal(closes):
    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    ema50 = ema(closes, 50)
    ema200 = ema(closes, 200)
    current_rsi = rsi(closes)

    if ema50 and ema200:
        trend = "BULLISH" if ema50 > ema200 else "BEARISH"
    else:
        trend = "NEUTRAL"

    if ema9 and ema21:
        if ema9 > ema21 and current_rsi > 50:
            signal = "UP"
        elif ema9 < ema21 and current_rsi < 50:
            signal = "DOWN"
        else:
            signal = "WAIT"
    else:
        signal = "WAIT"

    return {
        "signal": signal,
        "trend": trend,
        "rsi": round(current_rsi, 2),
        "ema9": round(ema9, 3) if ema9 else None,
        "ema21": round(ema21, 3) if ema21 else None,
        "ema50": round(ema50, 3) if ema50 else None,
        "ema200": round(ema200, 3) if ema200 else None
    }
