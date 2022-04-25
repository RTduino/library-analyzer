# 运行本程序，会自动生成一个csv文件，显示爬取到的所有arduino软件包的信息
# 需要clone这个仓库 https://github.com/arduino/library-registry ，并将这个脚本放在这个仓库文件夹的根目录下
import json
from lib2to3.pygram import pattern_symbols
import requests
import csv

# 需要使用你的token来提高github请求次数至每小时5000次，详见：#https://blog.csdn.net/weixin_43274247/article/details/106577653
headers = {
    'Authorization':'token '+'your token ID', # 不要忘记改这里，添加tokenID
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

with open('result.csv', 'w+') as csv_result:
    csv_headers = ['repo', 'stars', 'forks', 'lastpush']
    writer = csv.DictWriter(csv_result, fieldnames=csv_headers)
    writer.writeheader()

    with open('repositories.txt','r') as file:
        for line in file:
            if 'github' in line:
                user_repo = line[len('https://github.com/'):] # user/repo
                repo_info_api = 'https://api.github.com/repos/' + user_repo #拼出获取仓库信息的API
                repo_info_api = repo_info_api.rstrip('\r\n') # 去除行末尾的\r\n或\n，否则会导致url错误
                repo_info_api = repo_info_api.rstrip('\n')
                repo_info_api = repo_info_api.rstrip('.git') # 去除行末尾可能潜在的.git

                r = requests.get(repo_info_api, headers = headers)
                html = r.content
                html_doc = str(html, 'utf-8')
                repo_info_dict = json.loads(html_doc)
                try:
                    stargazers_count = repo_info_dict['stargazers_count'] # 获取到repo的star数量
                    forks_count = repo_info_dict['forks_count'] # 获取到repo的fork数量
                    lastpush = repo_info_dict['pushed_at'] # 获取最后一次commit时间
                    repo_dict = {'repo':user_repo, 'stars':str(stargazers_count), 'forks':str(forks_count), 'lastpush':lastpush}
                    writer.writerow(repo_dict)
                except:
                    print('fail to get information: ' + repo_info_api)
                    print(html_doc)
                    print('--------------------------------')
                    pass
