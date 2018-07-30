from Code.Config import Config
from Code.StockLimitUp import StockLimitUp as Slp
from Include.Announcer import beep


def run():
    config = Config()
    field = config.config_shares()
    time_interval = config.config_time_interval()
    beep()
    slp = Slp(field)
    slp.loop(time_interval)
