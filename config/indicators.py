indicators_by_category = {
    "株価指数": {
        "S&P 500（SPY）": {"ticker": "SPY", "default": True, "description": "アメリカの代表的な株価指数で、米国主要500社の株価動向を示します。市場全体の動向を把握するためのベンチマークとされています。"},
        "ナスダック100（QQQ）": {"ticker": "QQQ", "default": False, "description": "NASDAQ市場に上場する主要な非金融系100銘柄の株価指数。特にハイテク企業の動向を反映します。"},
        "NYダウ（DIA）": {"ticker": "DIA", "default": False, "description": "米国の代表的な株価指数で、工業株30銘柄の平均株価をもとに構成されます。長期トレンドの分析に利用されます。"},
        "日経平均（日本）": {"ticker": "^N225", "default": True, "description": "日本の代表的な株価指数で、東証プライム上場銘柄の中から選ばれた225銘柄で構成されます。"},
        "DAX（ドイツ）": {"ticker": "^GDAXI", "default": True, "description": "ドイツの主要企業30社で構成される株価指数で、欧州の経済指標として注目されます。"},
        "FTSE 100（イギリス）": {"ticker": "^FTSE", "default": False, "description": "ロンドン証券取引所に上場する時価総額上位100社の株式から構成される英国の代表的な株価指数です。"},
        "CAC 40（フランス）": {"ticker": "^FCHI", "default": False, "description": "フランスの代表的な株価指数で、ユーロ圏の経済動向を示す重要な指標です。"},
        "上海総合指数（中国）": {"ticker": "000001.SS", "default": False, "description": "中国の上海証券取引所に上場するすべてのA株とB株を対象とした総合株価指数です。"},
        "MSCI新興国（EEM）": {"ticker": "EEM", "default": False, "description": "新興国市場の株式を対象にした指数で、グローバルな投資のリスクとリターンを把握するために利用されます。"},
        "SENSEX（インド）": {"ticker": "^BSESN", "default": False, "description": "インドのボンベイ証券取引所に上場する代表的な30社の株式で構成される株価指数です。"},
        "KOSPI（韓国）": {"ticker": "^KS11", "default": False, "description": "韓国証券取引所に上場するすべての普通株を対象とした株価指数です。"},
        "IBOVESPA（ブラジル）": {"ticker": "^BVSP", "default": False, "description": "ブラジル・サンパウロ証券取引所の主要株で構成される株価指数で、ラテンアメリカ市場の動向を示します。"}
    },
    "国債": {
        "米国2年債利回り（^IRX）": {"ticker": "^IRX", "default": False, "description": "米国財務省が発行する2年満期の国債の利回りを示します。短期金利の代表的な指標とされます。"},
        "米国5年債利回り（^FVX）": {"ticker": "^FVX", "default": False, "description": "米国政府が発行する5年満期の国債の利回り。中期的な金利動向の判断材料として使われます。"},
        "米国10年債利回り（^TNX）": {"ticker": "^TNX", "default": True, "description": "米国政府が発行する10年満期の国債の利回りを示します。金融市場で最も注目される長期金利の指標です。"},
        "米国30年債利回り（^TYX）": {"ticker": "^TYX", "default": False, "description": "米国政府が発行する30年満期の長期国債の利回り。超長期の金利動向を把握するために用いられます。"},
        "日本2年国債利回り": {"is_mof": True, "term": "2年", "default": False, "description": "日本政府が発行する2年満期の国債の利回り。日本の短期金利の指標の一つです。"},
        "日本5年国債利回り": {"is_mof": True, "term": "5年", "default": False, "description": "日本政府が発行する5年満期の国債の利回りで、中期的な金融政策への期待を反映します。"},
        "日本10年国債利回り": {"is_mof": True, "term": "10年", "default": True, "description": "日本の長期金利の代表的指標であり、日本銀行の金融政策や経済の見通しに大きな影響を与えます。"},
        "日本30年国債利回り": {"is_mof": True, "term": "30年", "default": False, "description": "日本政府が発行する30年満期の国債の利回り。年金基金など長期投資家にとって重要な指標です。"}
    },
    "為替": {
        "USD/JPY（ドル円）": {"ticker": "JPY=X", "default": True, "description": "米ドルと日本円の為替レートを表します。日本の輸出入や金融政策に大きく影響します。"},
        "EUR/USD（ユーロドル）": {"ticker": "EURUSD=X", "default": True, "description": "ユーロと米ドルの為替レートで、世界で最も取引量の多い通貨ペアです。"},
        "GBP/USD（ポンドドル）": {"ticker": "GBPUSD=X", "default": False, "description": "イギリスのポンドと米ドルの為替レート。英国経済や政策に関連する動向が影響します。"},
        "AUD/USD（豪ドル米ドル）": {"ticker": "AUDUSD=X", "default": False, "description": "豪ドルと米ドルの為替レートで、コモディティ価格や中国経済の影響を受けやすいです。"},
        "USD/CAD（カナダドル）": {"ticker": "CAD=X", "default": False, "description": "米ドルとカナダドルの為替レート。原油価格の動向と密接に関連します。"},
        "USD/CHF（スイスフラン）": {"ticker": "CHF=X", "default": False, "description": "米ドルとスイスフランの為替レート。安全資産とされるスイスフランの需要に左右されます。"},
        "EUR/JPY（ユーロ円）": {"ticker": "EURJPY=X", "default": False, "description": "ユーロと日本円の為替レート。欧州および日本の経済状況が影響を与えます。"},
        "USD/CNY（米ドル人民元）": {"ticker": "CNY=X", "default": False, "description": "米ドルと中国人民元の為替レートで、中国政府の為替政策の影響を強く受けます。"}
    },
    "コモディティ": {
        "金（Gold）": {"ticker": "GC=F", "default": True, "description": "安全資産として知られる金の先物価格。インフレ懸念や金融不安時に注目されます。"},
        "銀（Silver）": {"ticker": "SI=F", "default": False, "description": "工業用途と資産保全の両面で需要がある金属。価格変動が大きい特徴があります。"},
        "原油（WTI）": {"ticker": "CL=F", "default": True, "description": "米国産の原油の先物価格。エネルギー市場と世界経済に大きな影響を与える指標です。"},
        "ブレント原油": {"ticker": "BZ=F", "default": False, "description": "欧州を中心に取引される原油の国際指標。中東情勢の影響も受けやすいです。"},
        "天然ガス（Henry Hub）": {"ticker": "NG=F", "default": False, "description": "米国で取引される天然ガスの先物価格。冬場の需要や供給状況が影響します。"},
        "銅（Copper）": {"ticker": "HG=F", "default": False, "description": "景気敏感資源の代表格で、建設や製造業の需要を反映します。"},
        "小麦（Wheat）": {"ticker": "ZW=F", "default": False, "description": "世界的な農産物の指標で、天候や地政学的リスクが価格に影響します。"},
        "大豆（Soybeans）": {"ticker": "ZS=F", "default": False, "description": "食料および飼料として需要が高い農産物。米中貿易動向にも左右されます。"}
    },
    "仮想通貨": {
        "Bitcoin（BTC/USD）": {"ticker": "BTC-USD", "default": True, "description": "最も有名な仮想通貨。供給量が限られており、インフレヘッジやデジタル資産として注目されています。"},
        "Ethereum（ETH/USD）": {"ticker": "ETH-USD", "default": False, "description": "スマートコントラクト機能を持つ仮想通貨で、DeFiやNFTの基盤として利用されます。"},
        "BinanceCoin（BNB/USD）": {"ticker": "BNB-USD", "default": False, "description": "大手仮想通貨取引所Binanceが発行するトークンで、手数料割引などの用途があります。"},
        "Solana（SOL/USD）": {"ticker": "SOL-USD", "default": False, "description": "高速処理が可能なブロックチェーンを基盤とする仮想通貨で、分散型アプリケーションに用いられます。"}
    }
}

category_order = [
    "株価指数",
    "国債",
    "コモディティ",
    "仮想通貨",
    "為替"
]

__all__ = ["indicators_by_category", "category_order"]
