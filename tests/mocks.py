from polygon import RESTClient
import unittest
import httpretty  # type: ignore

mocks = [
    (
        "/v2/aggs/ticker/AAPL/range/1/day/2005-04-01/2005-04-04",
        '{"ticker":"AAPL","queryCount":2,"resultsCount":2,"adjusted":true,"results":[{"v":6.42646396e+08,"vw":1.469,"o":1.5032,"c":1.4604,"h":1.5064,"l":1.4489,"t":1112331600000,"n":82132},{"v":5.78172308e+08,"vw":1.4589,"o":1.4639,"c":1.4675,"h":1.4754,"l":1.4343,"t":1112587200000,"n":65543}],"status":"OK","request_id":"12afda77aab3b1936c5fb6ef4241ae42","count":2}',
    ),
    (
        "/v2/aggs/grouped/locale/us/market/stocks/2005-04-04?adjusted=True",
        '{"queryCount":1,"resultsCount":1,"adjusted": true,"results": [{"T":"GIK","v":895345,"vw":9.9979,"o":9.99,"c":10.02,"h":10.02,"l":9.9,"t":1602705600000,"n":96}],"status":"OK","request_id":"eae3ded2d6d43f978125b7a8a609fad9","count":1}',
    ),
    (
        "/v1/open-close/AAPL/2005-04-01?adjusted=True",
        '{"status": "OK","from": "2021-04-01","symbol": "AAPL","open": 123.66,"high": 124.18,"low": 122.49,"close": 123,"volume": 75089134,"afterHours": 123,"preMarket": 123.45}',
    ),
    (
        "/v2/aggs/ticker/AAPL/prev",
        '{"ticker":"AAPL","queryCount":1,"resultsCount":1,"adjusted":true,"results":[{"T":"AAPL","v":9.5595226e+07,"vw":158.6074,"o":162.25,"c":156.8,"h":162.34,"l":156.72,"t":1651003200000,"n":899965}],"status":"OK","request_id":"5e5378d5ecaf3df794bb52e45d015d2e","count":1}',
    ),
    (
        "/v3/reference/tickers",
        '{"results":[{"ticker":"A","name":"Agilent Technologies Inc.","market":"stocks","locale":"us","primary_exchange":"XNYS","type":"CS","active":true,"currency_name":"usd","cik":"0001090872","composite_figi":"BBG000C2V3D6","share_class_figi":"BBG001SCTQY4","last_updated_utc":"2022-04-27T00:00:00Z"},{"ticker":"AA","name":"Alcoa Corporation","market":"stocks","locale":"us","primary_exchange":"XNYS","type":"CS","active":true,"currency_name":"usd","cik":"0001675149","composite_figi":"BBG00B3T3HD3","share_class_figi":"BBG00B3T3HF1","last_updated_utc":"2022-04-27T00:00:00Z"}],"status":"OK","request_id":"37089bb3b4ef99a796cdc82ff971e447","count":2,"next_url":"https://api.polygon.io/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmZGF0ZT0yMDIyLTA0LTI3JmxpbWl0PTImb3JkZXI9YXNjJnBhZ2VfbWFya2VyPUFBJTdDZjEyMmJjYmY4YWQwNzRmZmJlMTZmNjkxOWQ0ZDc3NjZlMzA3MWNmNmU1Nzg3OGE0OGU1NjQ1YzQyM2U3NzJhOSZzb3J0PXRpY2tlcg"}',
    ),
    (
        "/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmZGF0ZT0yMDIyLTA0LTI3JmxpbWl0PTImb3JkZXI9YXNjJnBhZ2VfbWFya2VyPUFBJTdDZjEyMmJjYmY4YWQwNzRmZmJlMTZmNjkxOWQ0ZDc3NjZlMzA3MWNmNmU1Nzg3OGE0OGU1NjQ1YzQyM2U3NzJhOSZzb3J0PXRpY2tlcg",
        '{"results":[{"ticker":"AAA","name":"AAF First Priority CLO Bond ETF","market":"stocks","locale":"us","primary_exchange":"ARCX","type":"ETF","active":true,"currency_name":"usd","composite_figi":"BBG00X5FSP48","share_class_figi":"BBG00X5FSPZ4","last_updated_utc":"2022-04-27T00:00:00Z"},{"ticker":"AAAU","name":"Goldman Sachs Physical Gold ETF Shares","market":"stocks","locale":"us","primary_exchange":"BATS","type":"ETF","active":true,"currency_name":"usd","cik":"0001708646","composite_figi":"BBG00LPXX872","share_class_figi":"BBG00LPXX8Z1","last_updated_utc":"2022-04-27T00:00:00Z"}],"status":"OK","request_id":"40d60d83fa0628503b4d13387b7bde2a","count":2}',
    ),
    (
        "/v3/reference/tickers/AAPL",
        '{"ticker":"AAPL","name":"Apple Inc.","market":"stocks","locale":"us","primary_exchange":"XNAS","type":"CS","active":true,"currency_name":"usd","cik":"0000320193","composite_figi":"BBG000B9XRY4","share_class_figi":"BBG001S5N8V8","market_cap":2.6714924917e+12,"phone_number":"(408) 996-1010","address":{"address1":"ONE APPLE PARK WAY","city":"CUPERTINO","state":"CA","postal_code":"95014"},"description":"Apple designs a wide variety of consumer electronic devices, including smartphones (iPhone), tablets (iPad), PCs (Mac), smartwatches (Apple Watch), AirPods, and TV boxes (Apple TV), among others. The iPhone makes up the majority of Apples total revenue. In addition, Apple offers its customers a variety of services such as Apple Music, iCloud, Apple Care, Apple TV+, Apple Arcade, Apple Card, and Apple Pay, among others. Apples products run internally developed software and semiconductors, and the firm is well known for its integration of hardware, software and services. Apples products are distributed online as well as through company-owned stores and third-party retailers. The company generates roughly 40 of its revenue from the Americas, with the remainder earned internationally.","sic_code":"3571","sic_description":"ELECTRONIC COMPUTERS","ticker_root":"AAPL","homepage_url":"https://www.apple.com","total_employees":154000,"list_date":"1980-12-12","branding":{"logo_url":"https://api.polygon.io/v1/reference/company-branding/d3d3LmFwcGxlLmNvbQ/images/2022-02-01_logo.svg","icon_url":"https://api.polygon.io/v1/reference/company-branding/d3d3LmFwcGxlLmNvbQ/images/2022-02-01_icon.png"},"share_class_shares_outstanding":16319440000,"weighted_shares_outstanding":16319441000}',
    ),
    (
        "/v2/reference/news?ticker=NFLX",
        '{"results":[{"id":"JeJEhAVoKaqJ2zF9nzQYMg07UlEeWlis6Dsop33TPQY","publisher":{"name":"MarketWatch","homepage_url":"https://www.marketwatch.com/","logo_url":"https://s3.polygon.io/public/assets/news/logos/marketwatch.svg","favicon_url":"https://s3.polygon.io/public/assets/news/favicons/marketwatch.ico"},"title":"Theres a big hole in the Feds theory of inflation—incomes are falling at a record 10.9 rate","author":"MarketWatch","published_utc":"2022-04-28T17:08:00Z","article_url":"https://www.marketwatch.com/story/theres-a-big-hole-in-the-feds-theory-of-inflationincomes-are-falling-at-a-record-10-9-rate-11651165705","tickers":["MSFT","TSN","NFLX","AMZN"],"amp_url":"https://www.marketwatch.com/amp/story/theres-a-big-hole-in-the-feds-theory-of-inflationincomes-are-falling-at-a-record-10-9-rate-11651165705","image_url":"https://images.mktw.net/im-533637/social","description":"If inflation is all due to an overly generous federal government giving its people too much money, then our inflation problem is about to go away."}],"status":"OK","request_id":"f5248459196e12f27520afd41cee5126","count":10}',
    ),
    (
        "/v3/reference/tickers/types",
        '{"results":[{"code":"CS","description":"Common Stock","asset_class":"stocks","locale":"us"},{"code":"PFD","description":"Preferred Stock","asset_class":"stocks","locale":"us"},{"code":"WARRANT","description":"Warrant","asset_class":"stocks","locale":"us"},{"code":"RIGHT","description":"Rights","asset_class":"stocks","locale":"us"},{"code":"BOND","description":"Corporate Bond","asset_class":"stocks","locale":"us"},{"code":"ETF","description":"Exchange Traded Fund","asset_class":"stocks","locale":"us"},{"code":"ETN","description":"Exchange Traded Note","asset_class":"stocks","locale":"us"},{"code":"SP","description":"Structured Product","asset_class":"stocks","locale":"us"},{"code":"ADRC","description":"American Depository Receipt Common","asset_class":"stocks","locale":"us"},{"code":"ADRW","description":"American Depository Receipt Warrants","asset_class":"stocks","locale":"us"},{"code":"ADRR","description":"American Depository Receipt Rights","asset_class":"stocks","locale":"us"},{"code":"FUND","description":"Fund","asset_class":"stocks","locale":"us"},{"code":"BASKET","description":"Basket","asset_class":"stocks","locale":"us"},{"code":"UNIT","description":"Unit","asset_class":"stocks","locale":"us"},{"code":"LT","description":"Liquidating Trust","asset_class":"stocks","locale":"us"}],"status":"OK","request_id":"efbfc7c2304bba6c2f19a2567f568134","count":15}',
    ),
    (
        "/v2/last/trade/AAPL",
        '{"results":{"c":[12,37],"i":"237688","p":166.25,"s":2,"x":4,"r":202,"z":3,"T":"AAPL","t":1651179319310617300,"y":1651179319308000000,"f":1651179319310588400,"q":7084210},"status":"OK","request_id":"d4bafa50e72cf9ed19ac538ae1a3185a"}',
    ),
    (
        "/v1/last/crypto/BTC/USD",
        '{"last":{"conditions":[2],"exchange":2,"price":39976.89682331,"size":0.005,"timestamp":1651180409688},"request_id":"d67c9bfe1fa0c29db9177d78b3ab713c","status":"success","symbol":"BTC-USD"}',
    ),
    (
        "/v3/trades/AAPL?limit=2",
        '{"results":[{"conditions":[12,37],"correction":1,"exchange":11,"id":"183276","participant_timestamp":1651181822461636600,"price":156.43,"sequence_number":7179341,"sip_timestamp":1651181822461979400,"size":10,"tape":3,"trf_id":3,"trf_timestamp":1651181557090806500},{"conditions":[12,37],"correction":1,"exchange":12,"id":"183276","participant_timestamp":1651181822461636600,"price":157.43,"sequence_number":7179341,"sip_timestamp":1651181822461979400,"size":10,"tape":3,"trf_id":3,"trf_timestamp":1651181557090806500}],"status":"OK","request_id":"756f9910624b35a47eb07f21a7a373bb"}',
    ),
    (
        "/v1/marketstatus/upcoming",
        '[{"exchange":"NYSE","name":"Memorial Day","date":"2022-05-30","status":"closed"},{"exchange":"NASDAQ","name":"Memorial Day","date":"2022-05-30","status":"closed"},{"exchange":"NASDAQ","name":"Juneteenth","date":"2022-06-20","status":"closed"},{"exchange":"NYSE","name":"Juneteenth","date":"2022-06-20","status":"closed"},{"exchange":"NYSE","name":"Independence Day","date":"2022-07-04","status":"closed"},{"exchange":"NASDAQ","name":"Independence Day","date":"2022-07-04","status":"closed"},{"exchange":"NYSE","name":"Labor Day","date":"2022-09-05","status":"closed"},{"exchange":"NASDAQ","name":"Labor Day","date":"2022-09-05","status":"closed"},{"exchange":"NYSE","name":"Thanksgiving","date":"2022-11-24","status":"closed"},{"exchange":"NASDAQ","name":"Thanksgiving","date":"2022-11-24","status":"closed"},{"exchange":"NYSE","name":"Thanksgiving","date":"2022-11-25","status":"early-close","open":"2022-11-25T14:30:00.000Z","close":"2022-11-25T18:00:00.000Z"},{"exchange":"NASDAQ","name":"Thanksgiving","date":"2022-11-25","status":"early-close","open":"2022-11-25T14:30:00.000Z","close":"2022-11-25T18:00:00.000Z"},{"exchange":"NYSE","name":"Christmas","date":"2022-12-26","status":"closed"},{"exchange":"NASDAQ","name":"Christmas","date":"2022-12-26","status":"closed"}]',
    ),
    (
        "/v1/marketstatus/now",
        '{"market":"extended-hours","earlyHours":false,"afterHours":true,"serverTime":"2022-04-28T16:48:08-04:00","exchanges":{"nyse":"extended-hours","nasdaq":"extended-hours","otc":"extended-hours"},"currencies":{"fx":"open","crypto":"open"}}',
    ),
    (
        "/v3/reference/splits",
        '{"results":[{"execution_date":"2022-07-18","split_from":1,"split_to":20,"ticker":"GOOGL"},{"execution_date":"2022-07-18","split_from":1,"split_to":20,"ticker":"GOOG"},{"execution_date":"2022-07-01","split_from":1,"split_to":3,"ticker":"CTO"},{"execution_date":"2022-06-29","split_from":1,"split_to":10,"ticker":"SHOP"},{"execution_date":"2022-06-22","split_from":1,"split_to":10,"ticker":"SHOP"},{"execution_date":"2022-06-10","split_from":1,"split_to":4,"ticker":"DXCM"},{"execution_date":"2022-06-06","split_from":1,"split_to":20,"ticker":"AMZN"},{"execution_date":"2022-05-20","split_from":2,"split_to":1,"ticker":"BRW"},{"execution_date":"2022-05-16","split_from":1,"split_to":2,"ticker":"CM"},{"execution_date":"2022-05-02","split_from":3,"split_to":4,"ticker":"CIG.C"}],"status":"OK","request_id":"b52de486daf5491e6b9ebdf5e0bf65bc"}',
    ),
    (
        "/v3/reference/dividends",
        '{"results":[{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2025-06-12","frequency":4,"pay_date":"2025-06-30","record_date":"2025-06-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2025-03-13","frequency":4,"pay_date":"2025-03-31","record_date":"2025-03-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2024-12-12","frequency":4,"pay_date":"2024-12-31","record_date":"2024-12-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2024-09-12","frequency":4,"pay_date":"2024-09-30","record_date":"2024-09-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2024-06-13","frequency":4,"pay_date":"2024-06-30","record_date":"2024-06-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2024-03-14","frequency":4,"pay_date":"2024-03-31","record_date":"2024-03-15","ticker":"CSSEN"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2023-12-14","frequency":4,"pay_date":"2023-12-31","record_date":"2023-12-15","ticker":"CSSEN"},{"cash_amount":0.5,"declaration_date":"2022-02-10","dividend_type":"CD","ex_dividend_date":"2023-11-13","frequency":4,"pay_date":"2023-11-15","record_date":"2023-11-14","ticker":"AIRTP"},{"cash_amount":0.59375,"declaration_date":"2020-09-09","dividend_type":"CD","ex_dividend_date":"2023-09-14","frequency":4,"pay_date":"2023-09-30","record_date":"2023-09-15","ticker":"CSSEN"},{"cash_amount":0.5,"declaration_date":"2022-02-10","dividend_type":"CD","ex_dividend_date":"2023-08-11","frequency":4,"pay_date":"2023-08-15","record_date":"2023-08-14","ticker":"AIRTP"}],"status":"OK","request_id":"0326f1f88a2867a7184c116f5b1edd00"}',
    ),
    (
        "/v3/reference/conditions?asset.class=stocks",
        '{"results":[{"id":1,"type":"sale_condition","name":"Acquisition","asset_class":"stocks","sip_mapping":{"UTP":"A"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"]},{"id":2,"type":"sale_condition","name":"Average Price Trade","asset_class":"stocks","sip_mapping":{"CTA":"B","UTP":"W"},"update_rules":{"consolidated":{"updates_high_low":false,"updates_open_close":false,"updates_volume":true},"market_center":{"updates_high_low":false,"updates_open_close":false,"updates_volume":true}},"data_types":["trade"]},{"id":3,"type":"sale_condition","name":"Automatic Execution","asset_class":"stocks","sip_mapping":{"CTA":"E"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"]},{"id":4,"type":"sale_condition","name":"Bunched Trade","asset_class":"stocks","sip_mapping":{"UTP":"B"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"]},{"id":5,"type":"sale_condition","name":"Bunched Sold Trade","asset_class":"stocks","sip_mapping":{"UTP":"G"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":false,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":false,"updates_volume":true}},"data_types":["trade"]},{"id":6,"type":"sale_condition","name":"CAP Election","asset_class":"stocks","sip_mapping":{"CTA":"I"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"],"legacy":true},{"id":7,"type":"sale_condition","name":"Cash Sale","asset_class":"stocks","sip_mapping":{"CTA":"C","UTP":"C"},"update_rules":{"consolidated":{"updates_high_low":false,"updates_open_close":false,"updates_volume":true},"market_center":{"updates_high_low":false,"updates_open_close":false,"updates_volume":true}},"data_types":["trade"]},{"id":8,"type":"sale_condition","name":"Closing Prints","asset_class":"stocks","sip_mapping":{"UTP":"6"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"]},{"id":9,"type":"sale_condition","name":"Cross Trade","asset_class":"stocks","sip_mapping":{"CTA":"X","UTP":"X"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":true,"updates_volume":true}},"data_types":["trade"]},{"id":10,"type":"sale_condition","name":"Derivatively Priced","asset_class":"stocks","sip_mapping":{"CTA":"4","UTP":"4"},"update_rules":{"consolidated":{"updates_high_low":true,"updates_open_close":false,"updates_volume":true},"market_center":{"updates_high_low":true,"updates_open_close":false,"updates_volume":true}},"data_types":["trade"]}],"status":"OK","request_id":"4c915a9cb249e40d08d031d70567d615","count":10}',
    ),
    (
        "/v3/reference/exchanges",
        '{"results":[{"id":1,"type":"exchange","asset_class":"stocks","locale":"us","name":"NYSE American, LLC","acronym":"AMEX","mic":"XASE","operating_mic":"XNYS","participant_id":"A","url":"https://www.nyse.com/markets/nyse-american"},{"id":2,"type":"exchange","asset_class":"stocks","locale":"us","name":"Nasdaq OMX BX, Inc.","mic":"XBOS","operating_mic":"XNAS","participant_id":"B","url":"https://www.nasdaq.com/solutions/nasdaq-bx-stock-market"},{"id":3,"type":"exchange","asset_class":"stocks","locale":"us","name":"NYSE National, Inc.","acronym":"NSX","mic":"XCIS","operating_mic":"XNYS","participant_id":"C","url":"https://www.nyse.com/markets/nyse-national"},{"id":4,"type":"TRF","asset_class":"stocks","locale":"us","name":"FINRA NYSE TRF","mic":"FINY","operating_mic":"XNYS","participant_id":"D","url":"https://www.finra.org"},{"id":4,"type":"TRF","asset_class":"stocks","locale":"us","name":"FINRA Nasdaq TRF Carteret","mic":"FINN","operating_mic":"FINR","participant_id":"D","url":"https://www.finra.org"},{"id":4,"type":"TRF","asset_class":"stocks","locale":"us","name":"FINRA Nasdaq TRF Chicago","mic":"FINC","operating_mic":"FINR","participant_id":"D","url":"https://www.finra.org"},{"id":4,"type":"TRF","asset_class":"stocks","locale":"us","name":"FINRA Alternative Display Facility","mic":"XADF","operating_mic":"FINR","participant_id":"D","url":"https://www.finra.org"},{"id":5,"type":"SIP","asset_class":"stocks","locale":"us","name":"Unlisted Trading Privileges","operating_mic":"XNAS","participant_id":"E","url":"https://www.utpplan.com"},{"id":6,"type":"TRF","asset_class":"stocks","locale":"us","name":"International Securities Exchange, LLC - Stocks","mic":"XISE","operating_mic":"XNAS","participant_id":"I","url":"https://nasdaq.com/solutions/nasdaq-ise"},{"id":7,"type":"exchange","asset_class":"stocks","locale":"us","name":"Cboe EDGA","mic":"EDGA","operating_mic":"XCBO","participant_id":"J","url":"https://www.cboe.com/us/equities"},{"id":8,"type":"exchange","asset_class":"stocks","locale":"us","name":"Cboe EDGX","mic":"EDGX","operating_mic":"XCBO","participant_id":"K","url":"https://www.cboe.com/us/equities"},{"id":9,"type":"exchange","asset_class":"stocks","locale":"us","name":"NYSE Chicago, Inc.","mic":"XCHI","operating_mic":"XNYS","participant_id":"M","url":"https://www.nyse.com/markets/nyse-chicago"},{"id":10,"type":"exchange","asset_class":"stocks","locale":"us","name":"New York Stock Exchange","mic":"XNYS","operating_mic":"XNYS","participant_id":"N","url":"https://www.nyse.com"},{"id":11,"type":"exchange","asset_class":"stocks","locale":"us","name":"NYSE Arca, Inc.","mic":"ARCX","operating_mic":"XNYS","participant_id":"P","url":"https://www.nyse.com/markets/nyse-arca"},{"id":12,"type":"exchange","asset_class":"stocks","locale":"us","name":"Nasdaq","mic":"XNAS","operating_mic":"XNAS","participant_id":"T","url":"https://www.nasdaq.com"},{"id":13,"type":"SIP","asset_class":"stocks","locale":"us","name":"Consolidated Tape Association","operating_mic":"XNYS","participant_id":"S","url":"https://www.nyse.com/data/cta"},{"id":14,"type":"exchange","asset_class":"stocks","locale":"us","name":"Long-Term Stock Exchange","mic":"LTSE","operating_mic":"LTSE","participant_id":"L","url":"https://www.ltse.com"},{"id":15,"type":"exchange","asset_class":"stocks","locale":"us","name":"Investors Exchange","mic":"IEXG","operating_mic":"IEXG","participant_id":"V","url":"https://www.iextrading.com"},{"id":16,"type":"TRF","asset_class":"stocks","locale":"us","name":"Cboe Stock Exchange","mic":"CBSX","operating_mic":"XCBO","participant_id":"W","url":"https://www.cboe.com"},{"id":17,"type":"exchange","asset_class":"stocks","locale":"us","name":"Nasdaq Philadelphia Exchange LLC","mic":"XPHL","operating_mic":"XNAS","participant_id":"X","url":"https://www.nasdaq.com/solutions/nasdaq-phlx"},{"id":18,"type":"exchange","asset_class":"stocks","locale":"us","name":"Cboe BYX","mic":"BATY","operating_mic":"XCBO","participant_id":"Y","url":"https://www.cboe.com/us/equities"},{"id":19,"type":"exchange","asset_class":"stocks","locale":"us","name":"Cboe BZX","mic":"BATS","operating_mic":"XCBO","participant_id":"Z","url":"https://www.cboe.com/us/equities"},{"id":20,"type":"exchange","asset_class":"stocks","locale":"us","name":"MIAX Pearl","mic":"EPRL","operating_mic":"MIHI","participant_id":"H","url":"https://www.miaxoptions.com/alerts/pearl-equities"},{"id":21,"type":"exchange","asset_class":"stocks","locale":"us","name":"Members Exchange","mic":"MEMX","operating_mic":"MEMX","participant_id":"U","url":"https://www.memx.com"}],"status":"OK","request_id":"c0109b8a70a931efe47cef085c7a7f5e","count":24}',
    ),
    (
        "/v3/quotes/AAPL?limit=1",
        '{"results":[{"ask_exchange":12,"ask_price":159.66,"ask_size":4,"bid_exchange":12,"bid_price":159.65,"bid_size":3,"participant_timestamp":1651258089126196693,"sequence_number":85374772,"sip_timestamp":1651258089126211647,"tape":3}],"status":"OK","request_id":"72eb1a815a1775544b4d280f44166992"}',
    ),
    (
        "/v2/last/nbbo/AAPL",
        '{"results":{"p":159.5,"s":16,"x":11,"P":159.51,"S":2,"X":12,"z":3,"T":"AAPL","t":1651258489041139455,"y":1651258489040965640,"q":86710587},"status":"OK","request_id":"329b67a5d8cf8ea89c407fdd947722dc"}',
    ),
    (
        "/v1/last_quote/currencies/AUD/USD",
        '{"last":{"ask":0.7085,"bid":0.7081,"exchange":48,"timestamp":1651258681000},"request_id":"94bf8f7d904c04e1fadc6293907a4fe7","status":"success","symbol":"AUD/USD"}',
    ),
    (
        "/v1/conversion/AUD/USD?amount=100",
        '{"converted":70.85,"from":"AUD","initialAmount":100,"last":{"ask":1.4116318,"bid":1.4115123,"exchange":48,"timestamp":1651259043000},"request_id":"fac0cbd15f33070754880ace220d12b9","status":"success","symbol":"USD/AUD","to":"USD"}',
        "/v2/snapshot/locale/us/markets/stocks/tickers?market.type=stocks",
        '{"count": 1,"status": "OK","tickers": [{"day": {"c": 20.506,"h": 20.64,"l": 20.506,"o": 20.64,"v": 37216,"vw": 20.616},"lastQuote": {"P": 20.6,"S": 22,"p": 20.5,"s": 13,"t": 1605192959994246100},"lastTrade": {"c": [14,41],"i": "71675577320245","p": 20.506,"s": 2416,"t": 1605192894630916600,"x": 4},"min": {"av": 37216,"c": 20.506,"h": 20.506,"l": 20.506,"o": 20.506,"v": 5000,"vw": 20.5105},"prevDay": {"c": 20.63,"h": 21,"l": 20.5,"o": 20.79,"v": 292738,"vw": 20.6939},"ticker": "BCAT","todaysChange": -0.124,"todaysChangePerc": -0.601,"updated": 1605192894630916600}]}',
    ),
    (
        "/v2/snapshot/locale/us/markets/stocks/gainers?market.type=stocks",
        '{"status":"OK","tickers":[{"day":{"c":6.42,"h":6.99,"l":6.4,"o":6.81,"v":115782,"vw":6.656},"lastQuote":{"P":6.43,"S":1,"p":6.4,"s":1,"t":1651251738312628478},"lastTrade":{"c":[14,41],"i":"100","p":6.42,"s":200,"t":1651251334045891221,"x":8},"min":{"av":115689,"c":6.42,"h":6.542,"l":6.42,"o":6.49,"v":2671,"vw":6.4604},"prevDay":{"c":0.29,"h":0.348,"l":0.29,"o":0.3443,"v":1488660,"vw":0.317},"ticker":"NVCN","todaysChange":6.13,"todaysChangePerc":2113.793,"updated":1651251360000000000},{"day":{"c":4.2107,"h":4.95,"l":4.21,"o":4.31,"v":453199,"vw":4.4181},"lastQuote":{"P":4.22,"S":9,"p":4.21,"s":11,"t":1651251781709136903},"lastTrade":{"c":null,"i":"1084","p":4.2116,"s":241,"t":1651251789345841015,"x":4},"min":{"av":453189,"c":4.2107,"h":4.2107,"l":4.2107,"o":4.2107,"v":1012,"vw":4.2107},"prevDay":{"c":0.1953,"h":0.2966,"l":0.195,"o":0.29,"v":8784033,"vw":0.2278},"ticker":"BIOL","todaysChange":4.016,"todaysChangePerc":2056.477,"updated":1651251789345841015}]}',
    ),
    (
        "/v2/snapshot/locale/us/markets/stocks/tickers/AAPL?market.type=stocks",
        '{"request_id":"957db942cab2d6b0633b9b4820db0cb2","status":"OK","ticker":{"day":{"c":160.315,"h":166.2,"l":159.8,"o":161.84,"v":68840127,"vw":162.7124},"lastQuote":{"P":159.99,"S":5,"p":159.98,"s":3,"t":1651251948407646487},"lastTrade":{"c":null,"i":"121351","p":159.99,"s":200,"t":1651251948294080343,"x":12},"min":{"av":68834255,"c":160.3,"h":160.71,"l":160.3,"o":160.71,"v":197226,"vw":160.5259},"prevDay":{"c":163.64,"h":164.515,"l":158.93,"o":159.25,"v":130149192,"vw":161.8622},"ticker":"AAPL","todaysChange":-3.65,"todaysChangePerc":-2.231,"updated":1651251948294080343}}',
    ),
    (
        "/v2/snapshot/locale/global/markets/crypto/tickers/X:BTCUSD/book",
        '{"data": {"askCount": 593.1412981600005,"asks": [{"p": 11454,"x": {"2": 1}},{"p": 11455,"x": {"2": 1}}],"bidCount": 694.951789670001,"bids": [{"p": 16303.17,"x": {"1": 2}},{"p": 16302.94,"x": {"1": 0.02859424,"6": 0.023455}}],"spread": -4849.17,"ticker": "X:BTCUSD","updated": 1605295074162},"status": "OK"}',
    ),
    (
        "/v3/snapshot/options/AAPL/O:AAPL230616C00150000",
        '{"request_id":"104d9b901d0c9e81d284cb8b41c5cdd3","results":{"break_even_price":179.075,"day":{"change":-2.3999999999999986,"change_percent":-7.643312101910824,"close":29,"high":32.25,"last_updated":1651204800000000000,"low":29,"open":29.99,"previous_close":31.4,"volume":8,"vwap":30.7738},"details":{"contract_type":"call","exercise_style":"american","expiration_date":"2023-06-16","shares_per_contract":100,"strike_price":150,"ticker":"O:AAPL230616C00150000"},"greeks":{"delta":0.6436614934293701,"gamma":0.0061735291012820675,"theta":-0.028227189324641973,"vega":0.6381159723175714},"implied_volatility":0.3570277203465058,"last_quote":{"ask":29.25,"ask_size":209,"bid":28.9,"bid_size":294,"last_updated":1651254260800059648,"midpoint":29.075,"timeframe":"REAL-TIME"},"open_interest":8133,"underlying_asset":{"change_to_break_even":19.11439999999999,"last_updated":1651254263172073152,"price":159.9606,"ticker":"AAPL","timeframe":"REAL-TIME"}},"status":"OK"}',
    ),
]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.c = RESTClient("", verbose=True)
        httpretty.enable(verbose=True, allow_net_connect=False)
        for m in mocks:
            httpretty.register_uri(
                httpretty.GET, cls.c.BASE + m[0], m[1], match_querystring=True
            )
