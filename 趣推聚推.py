''' 
@阿慈
垃圾毛自己玩吧
入口：https://wx.qrurl.net/?t=231005dD57Uv
new Env('趣推聚推'); 
www.rroadem.cn域名内的session_id末尾的scene填入变量
已经改变了原来的变量了多号用@隔开小数据用&格式：session_id&scene
提现看29行
'''
import os
import requests


qtjt_data = os.getenv('qtjt').split('@')


headers = {
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; 21091116UC Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5307 MMWEBSDK/20230504 MMWEBID/6808 MicroMessenger/8.0.37.2380(0x2800255B) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'Referer': 'https://servicewechat.com/wxf2b0ee8ed60663b4/6/page-frame.html'
}


request_data = {
    "hid": "30"
}


run_task2 = True #开启提现填True

for i in range(len(qtjt_data)):
    qtjt_params = qtjt_data[i].split('&')
    session_id = qtjt_params[0]  
    scene = qtjt_params[1]  

    
    url_task1 = f"https://www.rroadem.cn/?s=/ApiRewardVideoAd/givereward&aid=3&platform=wx&session_id={session_id}&pid=0&scene={scene}"
    
    
    response_task1 = requests.post(url_task1, headers=headers, json=request_data)
    json_data_task1 = response_task1.json()
    msg_task1 = json_data_task1.get('msg')
    print(f"第{i+1}个号运行结果：{msg_task1}")

    if run_task2:
        
        url_task2 = f"https://www.rroadem.cn/?s=/ApiMy/withdraw&aid=3&platform=wx&session_id={session_id}&pid=0&scene={scene}"
    
        
        request_data_task2 = {
            "money" : 0.1,
            "paytype" : "微信钱包"
        }
        
       
        response_task2 = requests.post(url_task2, headers=headers, json=request_data_task2)
        json_data_task2 = response_task2.json()
        msg_task2 = json_data_task2.get('msg')
        print(f"第{i+1}个号运行结果：{msg_task2}")