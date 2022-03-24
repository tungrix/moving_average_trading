

from price import perp_price
from trading_signal import signal
class trading(perp_price):
    def __init__(self):
        super().__init__()
        self.qty = 1
        self.holding_type = 'nan'
        self.entry_price = 0
        self.position_opened = False


    def execute(self, df):

        if self.df.empty == False:
            open_long_signal, close_long_signal, open_short_signal, close_short_signal = signal(df,
                                                  holding_type=self.holding_type,entry_price=self.entry_price).generator()

            if self.position_opened == True:
                if (close_short_signal == True) and (self.holding_type == 'SHORT'):
                    self.close_short_position()
                    self.position_opened = False
                elif (close_long_signal == True) and (self.holding_type == 'LONG'):
                    self.close_long_position()
                    self.position_opened = False
                self.holding_type = 'nan'

            if self.position_opened == False:
                if open_long_signal == True:
                    self.open_long_position()
                    self.holding_type = 'LONG'
                    self.position_opened = True

                    while True:
                        data = self.ws_private.fetch(self.subs[1])
                        if data:
                            self.entry_price = data[0]['price']
                            break
                elif open_short_signal == True:
                    self.open_short_position()
                    self.holding_type = 'SHORT'

                    self.position_opened = True
                    while True:
                        data = self.ws_private.fetch(self.subs[1])
                        if data:
                            self.entry_price = data[0]['price']
                            break

    def open_long_position(self):
        print('open_long_position', datetime.datetime.now())
        print(self.session.place_active_order(symbol=self.symbol, side="Buy", order_type="Market",
                                              qty=self.qty, time_in_force="GoodTillCancel", reduce_only=False,
                                              close_on_trigger=False))
        print('\n')

    def open_short_position(self):
        print('open_short_position', datetime.datetime.now())
        print(self.session.place_active_order(symbol=self.symbol, side="Sell", order_type="Market", qty=self.qty,
                                              time_in_force="GoodTillCancel", reduce_only=False,
                                              close_on_trigger=False))
        print('\n')

    def close_long_position(self):
        print('close_long_position', datetime.datetime.now())
        print(self.session.place_active_order(symbol=self.symbol, side="Sell", order_type="Market", qty=self.qty,
                                              time_in_force="GoodTillCancel", reduce_only=True, close_on_trigger=False))
        print('\n')

    def close_short_position(self):
        print('close_short_position', datetime.datetime.now())
        print(self.session.place_active_order(symbol=self.symbol, side="Buy", order_type="Market",
                                              qty=self.qty, time_in_force="GoodTillCancel", reduce_only=True,
                                              close_on_trigger=False))
