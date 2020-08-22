import requests
import re
import os
import time
import Utils

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

# 获取歌手信息和作品总数以获取'start'总数
inputSingerUid = input("Please input the singer's uid:")
MainPageUrl = 'https://kg.qq.com/node/personal?uid=' + inputSingerUid
response_MainPageUrl = requests.get(url = MainPageUrl,headers = headers)
htmlData_MainPageUrl = response_MainPageUrl.text
pattern_SongsAmount = re.compile('的个人主页","content":"作品: (.*?);')
result_SongsAmount = pattern_SongsAmount.findall(htmlData_MainPageUrl)
pattern_SingerInfo = re.compile('<title>(.*?) - 全民K歌</title>')
result_SingerInfo = pattern_SingerInfo.findall(htmlData_MainPageUrl)
print("You are entering " + str(result_SingerInfo) + "'s Mainpage.")
time.sleep(2)
print("Now start to download.")
songsAmount = int(''.join(result_SongsAmount))
start = int(songsAmount / 15 + 1)

# 初始化同名文件数
number = 1
number_exception = 1
# 初始化正在下载数
number_download = 1
# 初始化总耗时
totalTime = 0.00

pages = 1
while(pages <= start):
    # 获取每首歌曲的shareid
    Url = 'https://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_0&inCharset=GB2312&outCharset=utf-8&format=&g_tk=5381&g_tk_openkey=719182536&nocache=0.8706501019187272&share_uid=' + inputSingerUid +'&type=get_uinfo&_=1551533068931&num=15&start=' + str(pages)
    response_Url = requests.get(url = Url,headers = headers)
    htmlData_Url = response_Url.text
    pattern_SongShareid = re.compile('"shareid": "(.*?)",')
    result_SongShareid = pattern_SongShareid.findall(htmlData_Url)
    # print(result_SongShareid)
    # 获取每首歌所在的网页链接
    result_SongEntry = ['https://node.kg.qq.com/play?s=' + everySongShareid + '&g_f=personal' for everySongShareid in result_SongShareid]
    # print(result_SongEntry)
    # 获取每首歌的Url，并将其下载到本地
    for songEntryUrl in result_SongEntry:
        response_SongEntryUrl = requests.get(url = songEntryUrl,headers = headers)
        htmlData_SongEntryUrl = response_SongEntryUrl.text
        pattern_SongUrl = re.compile('"playurl":"http://(.*?)",')
        result_SongUrl = pattern_SongUrl.findall(htmlData_SongEntryUrl)
        pattern_FilenameAndID = re.compile('<title>(.*?)- 全民K歌，KTV交友社区</title>')
        result_FilenameAndID = pattern_FilenameAndID.findall(htmlData_SongEntryUrl)
        finalResult = list(zip(result_SongUrl, result_FilenameAndID))
        for songUrl, songFilenameAndID in finalResult:
            songUrl = "http://" + songUrl
            songFileData = requests.get(url = songUrl, headers=headers).content
            path = 'QuanMinKGe_SongsDownload\\' + songFilenameAndID + '.m4a'
            try:
                if(os.path.isfile(path)):# 判断是否有同名文件
                    songFilenameAndID = songFilenameAndID + "_" + str(number)
                    number = number + 1
                with open('QuanMinKGe_SongsDownload\\' + songFilenameAndID + '.m4a', mode = 'wb') as f:
                    f.write(songFileData)
                    print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                    everyConsumeTime = Utils.progressbar(songUrl, path, songFilenameAndID)
                    totalTime = everyConsumeTime + totalTime
                    number_download = number_download + 1
            except (FileNotFoundError, OSError):
                originSongFilenameAndID = songFilenameAndID
                songFilenameAndID = "Need to be renamed"
                if(os.path.isfile('QuanMinKGe_SongsDownload\\Need to be renamed.m4a')):# 判断是否有同名文件
                    songFilenameAndID = "Need to be renamed" + "_" + str(number_exception)
                    number_exception = number_exception + 1
                with open('QuanMinKGe_SongsDownload\\' + songFilenameAndID + '.m4a', mode = 'wb') as f:
                    f.write(songFileData)
                    print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                    everyConsumeTime = Utils.progressbar(songUrl, 'QuanMinKGe_SongsDownload\\Need to be renamed.m4a', originSongFilenameAndID)
                    print("The filename has been renamed in \"" + songFilenameAndID + "\" because of system not allowed characters.")
                    totalTime = everyConsumeTime + totalTime
                    number_download = number_download + 1
    pages = pages + 1

print("\nAll songs have been downloaded!")
print("Total Time: " + str(round(totalTime, 2)) + "sec")


# TODO 带英文冒号的歌曲无法正确命名
# TODO 优化重名文件命名规则
# TODO 下载视频MV
# TODO 合唱曲文件名优化
# TODO 当遇到网络连接超时的处理方法

# 文件名字符方面的错误不想再修了，太麻烦了