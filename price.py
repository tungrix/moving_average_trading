from pybit import HTTP, WebSocket
from strategies import add_indicator
from config import *
import pandas as pd
import time

import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 320)

class perp_price:
    def __init__(self):



        self.symbol = 'FTMUSDT'
        self.session = HTTP("https://api.bybit.com",
                            api_key=api_key, api_secret=api_secret)
        self.subs = [
            "orderBookL2_25." + self.symbol,
            "execution"
        ]
        self.ws = WebSocket(
            "wss://stream.bybit.com/realtime_public",
            subscriptions=self.subs[0],
            api_key=api_key, api_secret=api_secret
        )
        self.ws_private = WebSocket(
            "wss://stream.bybit.com/realtime_private",
            subscriptions=self.subs[1],
            api_key=api_key, api_secret=api_secret
        )
        self.first_window = 10
        self.second_window = 50
        self.interval = 15 # what is the interval (in minutes) get the data and trade
        self.stop_loss = 3 # in percentage
        self.backtest_type = 'SMA'
        self.df = pd.DataFrame(columns=['Datetime', 'Symbol','Close'])


    # fetch the raw orderbook data
    def get_raw_data(self):
        data = self.ws.fetch(self.subs[0])
        if data:
            return data

    # convert the orderbook data to dataframe
    def convect_to_dataframe(self):
        data = self.get_raw_data()
        if data:
            df = pd.DataFrame.from_dict(data).sort_values(by=['price'])
            return df

    # find the best bid and ask price
    def get_best_bid_ask(self):
        df = self.convect_to_dataframe()

        if df is not None:
            for i in range(len(df)):
                if df.iloc[i,3] == 'Sell':
                    best_ask = df.iloc[i,0]
                    best_bid = df.iloc[i-1,0]
                    return best_bid, best_ask

    # generate final dataframe for adding the indicator
    def aggregated_dataframe(self):
        while True:
            if self.get_best_bid_ask():
                bid,ask = self.get_best_bid_ask()

                df2 = {'Datetime':datetime.datetime.now(),'Symbol':self.symbol,'Close': bid}

                self.df = self.df.append(df2, ignore_index=True)
                add_indicator(df = self.df, first_window = self.first_window, second_window = self.second_window, backtest_type = self.backtest_type).generator()
                print(self.df)

                break
                return self.df
