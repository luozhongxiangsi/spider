import requests
import re
import pandas as pd
import time
import random


def get_id_from(ip:str) -> str:
    """
    查询IP归属地
    :param ip:
    :return: 返回ip归属地
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75\
         Safari/537.36",
        "Referer": "https://www.ip138.com/"

    }
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    # url = r'https://www.ip138.com/iplookup.asp?ip=103.140.246.234&action=2'
    try:
        res = requests.get(url, headers=headers)
        res.encoding = 'gb2312'
        result = re.findall('var ip_result = {"ASN归属地":"(.*?)"', res.text)
        return result[0]
    except Exception as e:
        return


def read_excel(path: str) -> None:
    ip_froms = []
    df = pd.read_excel(path)
    ips = df['IP']
    for ip in ips:
        ip_from = get_id_from(ip)
        ip_froms.append(ip_from)
    dataser = pd.DataFrame(ip_froms)
    df = pd.concat([df, dataser])
    print(df)



if __name__ == '__main__':
    # print(get_id_from('103.140.246.234'))
    excel_path = r'C:\Users\123456\Desktop\1.xlsx'
    read_excel(excel_path)