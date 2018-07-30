import easygui as eg
from path import Path


class Config:
    def __init__(self):
        self.file_path = Path(f'Bin\\Config\\config.txt')
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

    def config_shares(self):
        display = eg.multchoicebox(msg="选择需要显示的字段", title="配置显示字段", choices=list(self.map.keys()))
        if display:
            return [self.map[i] for i in self.map]
        else:
            eg.msgbox('必须选择一个字段', title='警告')
            self.config_shares()

    @staticmethod
    def config_time_interval():
        time_interval = eg.enterbox(msg="键入时间间隔(s)", title="配置时间间隔", default="10")
        return float(time_interval)


if __name__ == '__main__':
    c = Config()
    print(c.config_shares())
