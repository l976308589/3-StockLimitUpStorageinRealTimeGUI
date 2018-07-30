import arrow as ar
import requests as rq


def get_last(get_data_anyway=False):
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive", "Content-Length": "587",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Host": "www.iwencai.com",
               "Origin": "http://www.iwencai.com",
               "Referer": "http://www.iwencai.com/data-robot/extract-new?query=%E4%BB%8A%E6%97%A5%E5%B0%81%E6%9D%BF%E6%AC%A1%E6%95%B0&querytype=stock&qsData=pc_~soniu~others~homepage~box~history&dataSource=send_click",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest"}
    cookies = {
        'PHPSESSID': '41c50232858e1f42eeee65d22c225cb3',
        "v": "AmhAQA4Kp02YQIvJFC1Z0p_oOV1ukcybrvWgHyKZtOPWfQZByqGcK_4FcKpx",
        'guideState': '1',
        'cid': 'b35d7d16d0155003cfceee7b3376551f1531282267',
        'ComputerID': 'b35d7d16d0155003cfceee7b3376551f1531282267',
        "other_uid": "Ths_iwencai_Xuangu_c1zmt73xbuzdvlvt7k8vr8xq9mx6l503",
        'other_uname': '3e6bwp6dln'
    }
    data = {'tid': 'stockpick',
            'querytype': 'stock',
            'w': f'{ar.now().format("YYYY-MM-DD")}封板',
            'robot': {"source": "Ths_iwencai_Xuangu", "user_id": "",
                      "log_info": "{\"other_info\":\"{\\\"eventId\\\":\\\"iwencai_pc_hp_history\\\",\\\"ct\\\":1531387746416}\",\"other_utype\":\"random\",\"other_uid\":\"Ths_iwencai_Xuangu_c1zmt73xbuzdvlvt7k8vr8xq9mx6l503\"}",
                      "user_name": "3e6bwp6dln", "version": "1.5"}}
    data = rq.post('http://www.iwencai.com/data-robot/get-fusion-data', headers=headers, cookies=cookies,
                   data=data).json()
    try:
        if data['success']:
            date = data['data']['wencai_data']['parse']['original'][0]['indexPropertiesMap']['交易日期']
            if date == ar.now().format('YYYYMMDD') or get_data_anyway:
                result = data['data']['wencai_data']['result']['result']
                detail = []
                for i in result:
                    for j in i[7]:
                        j['name'] = i[1]
                        j['reason'] = i[-7]
                        j['times'] = i[-8]
                        detail.append(j)
                return detail
    except:
        return []


if __name__ == '__main__':
    data = get_last(get_data_anyway=True)
    print(data)
