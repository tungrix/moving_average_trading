import ta
import pandas as pd
import numpy as np



# add indicator column to the dataframe
class add_indicator:
    def __init__(self, df,first_window,second_window, backtest_type):
        self.df = df

        self.first_window = first_window  # fast ema window
        self.second_window = second_window # # slow ema window
        self.backtest_type = backtest_type

    # according the backtest_type to generate corresponding indicator
    def generator(self):

        if 'EMA' in self.backtest_type:
            self.ema()
        if 'SMA' in self.backtest_type:
            self.sma()
            print('sssss')
        if 'WMA' in self.backtest_type:
            self.wma()

        return self.df

    def ema(self):
        # self.first_window = fast_window, self.second_window = slow_window

        self.df['fast_ema'] = ta.trend.EMAIndicator(self.df['Close'], window=self.first_window).ema_indicator()
        self.df['slow_ema'] = ta.trend.EMAIndicator(self.df['Close'], window=self.second_window).ema_indicator()


    def sma(self):
        # self.first_window = fast_window, self.second_window = slow_window

        self.df['fast_ema'] = ta.trend.SMAIndicator(self.df['Close'], window=self.first_window).sma_indicator()
        self.df['slow_ema'] = ta.trend.SMAIndicator(self.df['Close'], window=self.second_window).sma_indicator()

    def wma(self):
        # self.first_window = fast_window, self.second_window = slow_window

        self.df['fast_ema'] = ta.trend.WMAIndicator(self.df['Close'], window=self.first_window).wma()
        self.df['slow_ema'] = ta.trend.WMAIndicator(self.df['Close'], window=self.second_window).wma()


