"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
小阅阅_V1.42
入口：https://wi53263.nnju.top:10258/yunonline/v1/auth/a736aa79132badffc48e4b380f21c7ac?codeurl=wi53263.nnju.top:10258&codeuserid=2&time=1693450574
抓包搜索关键词ysmuid 取出ysmuid的值即可 注意不是: ysm_uid

export ysmuid=xxxxxxx
多账号用'===='隔开 例 账号1====账号2
export ysmuid=xxxxxxx====xxxxxx
"""
money_Withdrawal = 0  # 提现开关 1开启 0关闭
max_concurrency = 1  # 设置要运行的线程数
key = "c2584357-e7e8-46d6-8327-1009122d854e"  # 内置key 必填！！！ key为企业微信webhook机器人后面的 key


import json
import os
import random
import re
import threading
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse, parse_qs
from requests.exceptions import ConnectionError, Timeout
import requests

lock = threading.Lock()
max_retries = 3

def process_account(account, i):
    values = account.split('@')
    ysmuid = values[0]
    print(f"\n=======开始执行账号{i}=======")
    print(f"unionid:{ysmuid}")
    url = "http://nsr.zsf2023e458.cloud/?cate=0"
    headers = {
        'Host': 'nsr.zsf2023e458.cloud',
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; 21091116UC Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5307 MMWEBSDK/20230504 MMWEBID/6808 MicroMessenger/8.0.37.2380(0x2800255B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'X-Requested-With': 'com.tencent.mm',
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': f'ysmuid={ysmuid}'
    }
    res = requests.get(url, headers=headers).text
    res1 = re.sub('\s', '', res)
    exchangeUrl = re.findall('"target="_blank"href="(.*?)">提现<', res1)
    ysm_uid1 = re.findall('\{unionid="(.*?)"', res1)
    ysm_uid = ysm_uid1[0]
    eurl = exchangeUrl[0]
    query_dict = parse_qs(urlparse(exchangeUrl[0]).query)
    unionid = query_dict.get('unionid', [''])[0]
    request_id = query_dict.get('request_id', [''])[0]
    b = urlparse(eurl)
    host = b.netloc

    current_timestamp = int(time.time() * 1000)

    url = 'http://nsr.zsf2023e458.cloud/yunonline/v1/gold'

    headers = {
        'Cookie': f'ejectCode=1; ysmuid={ysmuid}',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
    }

    params = {
        'unionid': f'{ysm_uid}',
        'time': current_timestamp
    }

    res = requests.get(url, headers=headers, params=params).json()
    if res['errcode'] == 0:
        day_gold = res['data']['day_gold']
        day_read = res['data']['day_read']
        last_gold = res['data']['last_gold']
        remain_read = res['data']['remain_read']
        print(f'当前金币:{last_gold}\n今日阅读文章:{day_read} 剩余:{remain_read}')
        print(f"{'=' * 18}开始阅读文章{'=' * 18}")
        for i in range(30):
            checkDict = [
                'MzkxNTE3MzQ4MQ==',
                'Mzg5MjM0MDEwNw==',
                'MzUzODY4NzE2OQ==',
                'MzkyMjE3MzYxMg==',
                'MzkxNjMwNDIzOA==',
                'Mzg3NzUxMjc5Mg==',
                'Mzg4NTcwODE1NA==',
                'Mzk0ODIxODE4OQ==',
                'Mzg2NjUyMjI1NA==',
                'MzIzMDczODg4Mw==',
                'Mzg5ODUyMzYzMQ==',
                'MzU0NzI5Mjc4OQ==',
                'Mzg5MDgxODAzMg==',
            ]
            url = "http://nsr.zsf2023e458.cloud/yunonline/v1/wtmpdomain"
            headers = {
                "Host": 'nsr.zsf2023e458.cloud',
                "Accept": 'application/json, text/javascript, */*; q=0.01',
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://nsr.zsf2023e458.cloud/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': f'ysmuid={ysmuid}; ejectCode=1'
            }

            data = {
                "unionid": ysm_uid
            }
            for retry in range(max_retries):
                try:
                    res = requests.post(url, headers=headers, data=data, timeout=7).json()
                    break
                except (ConnectionError, Timeout):
                    if retry < max_retries - 1:
                        continue
                    else:
                        print("异常退出")
                        break
                except Exception as e:
                    print(e)
                    print("状态1异常，尝试重新发送请求...")
                    res = requests.post(url, headers=headers, data=data, timeout=7).json()
            if res['errcode'] == 0:
                ukurl = res['data']['domain']
                parsed_url = urlparse(ukurl)
                domain = parsed_url.scheme + '://' + parsed_url.netloc
                query_params = parse_qs(parsed_url.query)
                uk = query_params.get('uk', [])[0] if 'uk' in query_params else None
                time.sleep(1)
                url = "https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"
                headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                    "Origin": f"{domain}",
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br"
                }
                params = {
                    "uk": uk
                }
                for retry in range(max_retries):
                    try:
                        res = requests.get(url, headers=headers, params=params, timeout=7).json()
                        break
                    except (ConnectionError, Timeout):
                        if retry < max_retries - 1:
                            continue
                        else:
                            print("异常退出")
                            break
                    except Exception as e:
                        print(e)
                        print("状态2异常，尝试重新发送请求...")
                        res = requests.get(url, headers=headers, params=params, timeout=7).json()
                if res['errcode'] == 0:
                    link = res['data']['link'] + "?/"
                    res = requests.get(url=link, headers=headers).text
                    pattern = r'<meta\s+property="og:url"\s+content="([^"]+)"\s*/>'
                    matches = re.search(pattern, res)

                    if matches:
                        fixed_url = matches.group(1)
                        og_url = fixed_url.replace("amp;", "")
                        biz = og_url.split('__biz=')[1].split('&')[0]
                        mid = og_url.split('&mid=')[1].split('&')[0]
                        print(f"获取文章成功---{mid} 来源[{biz}]")
                        sleep = random.randint(8, 9)

                        if biz in checkDict:
                            print(f"发现目标[{biz}] 疑似检测文章！！！")
                            link = og_url
                            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

                            messages = [
                                f"出现检测文章！！！\n{link}\n请在60s内点击链接完成阅读",
                            ]

                            for message in messages:
                                data = {
                                    "msgtype": "text",
                                    "text": {
                                        "content": message
                                    }
                                }
                                headers_bot = {'Content-Type': 'application/json'}
                                res = requests.post(url, headers=headers_bot, data=json.dumps(data))
                                print("以将该文章推送至微信请在60s内点击链接完成阅读--60s后继续运行")
                                time.sleep(60)
                                url = "https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold"
                                headers = {
                                    'Host': 'nsr.zsf2023e458.cloud',
                                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                                    "Origin": f"{domain}",
                                    'Sec-Fetch-Site': 'cross-site',
                                    'Sec-Fetch-Mode': 'cors',
                                    'Sec-Fetch-Dest': 'empty',
                                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                                    "Accept-Encoding": "gzip, deflate, br"
                                }
                                params = {
                                    "uk": uk,
                                    "time": sleep,
                                    "timestamp": current_timestamp
                                }
                                for retry in range(max_retries):
                                    try:
                                        res = requests.get(url, headers=headers, params=params, timeout=7).json()
                                        break
                                    except (ConnectionError, Timeout):
                                        if retry < max_retries - 1:
                                            continue
                                        else:
                                            print("异常退出")
                                            break
                                    except Exception as e:
                                        print('设置状态异常')
                                        print(e)
                                if res['errcode'] == 0:
                                    gold = res['data']['gold']
                                    print(f"第{i + 1}次阅读检测文章成功---获得金币[{gold}]")
                                    print(f"{'-' * 30}")
                                    time.sleep(1)
                                else:
                                    print(f"过检测失败，请尝试重新运行")
                                    exit()
                        else:
                            print(f"本次模拟阅读{sleep}秒")
                            time.sleep(sleep)
                            url = "https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold"
                            headers = {
                                'Host': 'nsr.zsf2023e458.cloud',
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                                "Origin": f"{domain}",
                                'Sec-Fetch-Site': 'cross-site',
                                'Sec-Fetch-Mode': 'cors',
                                'Sec-Fetch-Dest': 'empty',
                                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                                "Accept-Encoding": "gzip, deflate, br"
                            }
                            params = {
                                "uk": uk,
                                "time": sleep,
                                "timestamp": current_timestamp
                            }
                            for retry in range(max_retries):
                                try:
                                    res = requests.get(url, headers=headers, params=params, timeout=7).json()
                                    break
                                except (ConnectionError, Timeout):
                                    if retry < max_retries - 1:
                                        continue
                                    else:
                                        print("异常退出")
                                        break
                                except Exception as e:
                                    print('设置状态异常')
                                    print(e)
                            if res['errcode'] == 0:
                                gold = res['data']['gold']
                                print(f"第{i + 1}次阅读文章成功---获得金币[{gold}]")
                                print(f"{'-' * 30}")
                                time.sleep(1)
                            else:
                                print(f"阅读文章失败{res}")
                                break
                    else:
                        print("未找到link")

                elif res['errcode'] == 405:
                    print('阅读重复，重新尝试....')
                    print(f"{'-' * 30}")
                    time.sleep(3)
                elif res['errcode'] == 407:
                    print(f'{res}')
                    break

            else:
                print(f"获取阅读文章失败{res}")
                break

        if money_Withdrawal == 1:

            print(f"{'=' * 18}开始提现{'=' * 18}")

            url = 'http://nsr.zsf2023e458.cloud/yunonline/v1/gold'
            headers = {
                'Cookie': f'ysmuid={ysmuid}; ejectCode=1',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
            }
            params = {
                'unionid': f'{ysm_uid}',
                'time': current_timestamp
            }
            res = requests.get(url, headers=headers, params=params).json()
            if res['errcode'] == 0:
                last_gold = res['data']['last_gold']
                gold = int(int(last_gold) / 1000) * 1000


            url = "http://1693462663.sethlee.top/yunonline/v1/user_gold"
            headers = {
                'Host': host,
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a25) NetType/WIFI Language/zh_CN",
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': f'http://{host}',
                'Referer': eurl,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                'Cookie': f'ysmuid={ysmuid}; ejectCode=1'
            }
            data = {
                "unionid": unionid,
                "request_id": request_id,
                "gold": gold,
            }
            res = requests.post(url, headers=headers, data=data).json()
            if res['errcode'] == 0:
                money = res['data']['money']
                print(f"当前可提现{money}元")
            elif res['errcode'] == 405:
                print(f"当前可提现{gold}")

            url = "http://1693462663.sethlee.top/yunonline/v1/withdraw"
            headers = {
                'Host': host,
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a25) NetType/WIFI Language/zh_CN",
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': f'http://{host}',
                'Referer': eurl,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                'Cookie': f'ysmuid={ysmuid}; ejectCode=1'
            }

            data = {
                "unionid": unionid,
                "signid": request_id,
                "ua": "2",
                "ptype": "0",
                "paccount": "",
                "pname": ""
            }
            res = requests.post(url, headers=headers, data=data).json()
            if res['errcode'] == 0:
                print(f"提现成功")
            elif res['errcode'] == 405:
                print(res)

        elif money_Withdrawal == 0:
            print(f"{'=' * 18}{'=' * 18}")
            print(f"不执行提现")
    else:
        print(f"获取用户信息失败")
        exit()


if __name__ == "__main__":
    accounts = os.getenv('ysmuid')
    response = requests.get('https://gitee.com/shallow-a/qim9898/raw/master/label.txt').text
    print(response)
    if accounts is None:
        print('你没有填入ysmuid，咋运行？')
        exit()
    else:
        accounts_list = os.environ.get('ysmuid').split('====')
        num_of_accounts = len(accounts_list)
        print(f"获取到 {num_of_accounts} 个账号")
        with Pool(processes=num_of_accounts) as pool:
            thread_pool = ThreadPool(max_concurrency)
            thread_pool.starmap(process_account, [(account, i) for i, account in enumerate(accounts_list, start=1)])
