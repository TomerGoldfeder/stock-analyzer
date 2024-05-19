import datetime
from algo.moving_avg import MovingAVG
from stock_fetcher.stock_fetcher import StockFetcher


def get_ma_pos(symbol, org_start, org_end):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=2000)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')

    short_window = 30
    long_window = 200
    feature = f'{short_window}-{long_window}-day MA'

    fetcher = StockFetcher(stock_symbol=symbol)
    data = fetcher.fetch_raw_data(start_date=start_date, end_date=end_date)
    ma = MovingAVG.get_moving_avg(data, short_window, long_window, feature)

    org_start_obj = datetime.datetime.strptime(org_start, '%Y-%m-%d')
    org_end_obj = datetime.datetime.strptime(org_end, '%Y-%m-%d')
    relative_ma = ma[(ma.index >= org_start_obj) & (ma.index <= org_end_obj)]
    pos = MovingAVG.get_positive_percentage(ma, feature)
    pos_relative = MovingAVG.get_positive_percentage(relative_ma, feature)

    positivity = {
        'pos': [pos],
        'pos_dates': [pos_relative]
    }

    return feature, relative_ma, positivity