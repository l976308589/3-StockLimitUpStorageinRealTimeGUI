from time import sleep

import arrow as ar
import pandas as pd
from path import Path

from Include.Announcer import beep
from Include.Except import Except
from Include.Header import get_last
from Include.Log import log, filename_exists
from Include.Parsing import parsing
from Include.Trding_Time import is_trading_time


class StockLimitUp:
    def __init__(self, fields):
        self.data = pd.DataFrame()
        self.file_path = Path(f'Bin\\Data\\{ar.now().format("YYYYMMDD")}.csv')
        self.pre_date = ar.now()
        self.fields = fields
        self.map = {'代码': 'code',
                    '股票': 'name',
                    '涨停时间': 'time',
                    '打开涨停时间': 'openTime',
                    '持续时间': 'duration',
                    '更新时间': 'updatedTime',
                    '首次封单量': 'firstVol',
                    '最高封单量': 'highestVol',
                    '涨停次数': 'times',
                    '涨停原因': 'reason'
                    }
        self.stocks_to_watch = []

    def init_pre(self):
        if ar.now().day != self.pre_date.day:
            self.pre_date = ar.now()
            self.file_path = Path(f'Bin\\Data\\{ar.now().format("YYYYMMDD")}.csv')
            if self.file_path.exists():
                self.data = pd.read_csv(self.file_path, encoding='gbk')
            else:
                filename_exists(self.file_path.parent)
        stocks_to_watch_path = Path('Bin\\Config\\StockstoWatch.txt')
        if stocks_to_watch_path.exists():
            self.stocks_to_watch = [i.strip() for i in stocks_to_watch_path.lines()]
        else:
            filename_exists(stocks_to_watch_path.parent)
            self.stocks_to_watch = []
            log('需要配置监控股票')

    @staticmethod
    def waiting():
        sleep_time = is_trading_time()
        if sleep_time > 0:
            log(f'距离开盘仍需{sleep_time}s')
            sleep(sleep_time)
            return True
        else:
            return False

    def get_last(self):
        data = parsing(get_last())
        pre_data = self.data.copy()
        if not data.empty:
            self.data = self.data.append(data)
            self.data = self.data.drop_duplicates(subset=['code', 'openTime', 'time'], keep='last')
            newly_added = self.data.append(pre_data)
            newly_added = newly_added.drop_duplicates(subset=['code', 'openTime', 'time'], keep=False)
            return newly_added
        return pd.DataFrame()

    @staticmethod
    def format_time(x):
        tzinfo = ar.now().tzinfo
        if isinstance(x['openTime'], float) and x['openTime'] > 1000:
            x['openTime'] = ar.get(x['openTime'] / 1000).to(tz=tzinfo).format('YYYY-MM-DD HH:mm:ss')
        x['time'] = ar.get(float(x['time']) / 1000).to(tz=tzinfo).format('YYYY-MM-DD HH:mm:ss')
        x['updatedTime'] = ar.get(float(x['updatedTime']) / 1000).to(tz=tzinfo).format('YYYY-MM-DD HH:mm:ss')
        return x

    def storage(self, newly_added):
        newly_added = newly_added.apply(self.format_time, axis=1)
        if self.stocks_to_watch:
            newly_added = newly_added[newly_added.apply(lambda x: x['code'][:6] in self.stocks_to_watch, axis=1)]

            if (not newly_added.empty) and self.fields:
                newly_added = newly_added[self.fields]
                map_fields = {v: k for k, v in self.map.items()}
                newly_added.columns = [map_fields[i] for i in self.fields]
                beep()
                newly_added.apply(lambda x: print(x), axis=1)
        self.data.apply(self.format_time, axis=1).to_csv(self.file_path, index=False, encoding='gbk')

    def run(self):
        self.waiting()
        self.init_pre()
        newly_added = self.get_last()
        if not newly_added.empty:
            self.storage(newly_added)

    def loop(self, time_interval):
        while 1:
            try:
                self.run()
            except:
                Except()
            sleep(time_interval)
