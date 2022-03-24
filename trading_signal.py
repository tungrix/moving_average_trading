
from price import perp_price


# generate the trading signal for: open long, open short, close long, close short position
class signal(perp_price):
    def __init__(self,df,backtest_type, holding_type, entry_price):
        super().__init__()
        self.open_long_signal, self.close_long_signal, self.open_short_signal, self.close_short_signal = [False for _ in range(4)]

        self.df = df


        self.holding_type = holding_type
        self.entry_price = entry_price
        self.stop_loss = self.stop_loss/100
    def generator(self):
        if len(self.df) >= 2:

            self.ma_signal()

            if 'WITH_STOP_LOSS' in self.backtest_type:
                self.stop_loss_signal()
            # print(self.open_long_signal, self.close_long_signal, self.open_short_signal, self.close_short_signal)
        return self.open_long_signal, self.close_long_signal, self.open_short_signal, self.close_short_signal

    def ma_signal(self):
        fast_ema = self.df.iloc[-1]['fast_ema']
        slow_ema = self.df.iloc[-1]['slow_ema']
        last_fast_ema = self.df.iloc[-2]['fast_ema']
        last_slow_ema = self.df.iloc[-2]['slow_ema']

        self.open_long_signal = (fast_ema > slow_ema) and (last_fast_ema <= last_slow_ema)
        self.close_long_signal = slow_ema > fast_ema

        self.open_short_signal = (slow_ema > fast_ema) and (last_slow_ema <= last_fast_ema)

        self.close_short_signal = fast_ema > slow_ema

    def stop_loss_signal(self):
        now_close = self.df.loc[-1, 'Close']
        if self.holding_position == "LONG":
            if (now_close - self.entry_price) < -self.stop_loss * self.entry_price:
                self.close_long_signal = True
                print('Long position stop loss out')
                print('entry price: ',self.entry_price, 'now close: ', now_close)
        elif self.holding_position == "Short":
            if (now_close - self.entry_price) > self.stop_loss * self.entry_price:
                self.close_short_signal = True
                print('Short position stop loss out')
                print('entry price: ',self.entry_price, 'now close: ', now_close)
