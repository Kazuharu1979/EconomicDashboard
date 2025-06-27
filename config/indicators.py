indicators_by_category = {
    "株式": {
        "S&P 500（SPY）": {"ticker": "SPY", "default": True},
        "ナスダック100（QQQ）": {"ticker": "QQQ", "default": False},
        "NYダウ（DIA）": {"ticker": "DIA", "default": False},
        "日経平均（日本）": {"ticker": "^N225", "default": True},
        "DAX（ドイツ）": {"ticker": "^GDAXI", "default": True},
    },
    "国債": {
        "米国2年債利回り（^IRX）": {"ticker": "^IRX", "default": False},
        "米国10年債利回り（^TNX）": {"ticker": "^TNX", "default": True},
        "米国30年債利回り（^TYX）": {"ticker": "^TYX", "default": False},
        "日本2年国債利回り（MOF JPY2Y）": {"is_mof": True, "term": "2年", "default": False},
        "日本10年国債利回り（MOF JPY10Y）": {"is_mof": True, "term": "10年", "default": True},
        "日本30年国債利回り（MOF JPY30Y）": {"is_mof": True, "term": "30年", "default": False},
    },
    "為替": {
        "USD/JPY（ドル円）": {"ticker": "JPY=X", "default": True},
        "EUR/USD（ユーロドル）": {"ticker": "EURUSD=X", "default": False},
        "GBP/USD（ポンドドル）": {"ticker": "GBPUSD=X", "default": False},
    },
    "商品": {
        "金（Gold）": {"ticker": "GC=F", "default": True},
        "銀（Silver）": {"ticker": "SI=F", "default": False},
        "原油（WTI）": {"ticker": "CL=F", "default": True},
        "ブレント原油": {"ticker": "BZ=F", "default": False},
    },
    "仮想通貨": {
        "ビットコイン（BTC/USD）": {"ticker": "BTC-USD", "default": False},
        "イーサリアム（ETH/USD）": {"ticker": "ETH-USD", "default": False},
    }
}
