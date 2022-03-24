
from price import perp_price
import schedule
from trading import trading
import time

def main():
    df = perp.aggregated_dataframe()
    trade.execute(df)


if __name__ == "__main__":
    perp = perp_price()
    trade = trading()
    schedule.every(perp.interval).minutes.do(main) # get the data and trade every perp.interval miniutes
    while True:
        schedule.run_pending()
        time.sleep(1)