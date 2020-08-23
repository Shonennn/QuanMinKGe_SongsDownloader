import requests
import re
import os
import time
import Utils

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

# 获取歌手信息和作品总数以获取'start'总数
inputSingerUid = input("Please input the singer's uid:") # 等待用户输入歌手uid
MainPageUrl = 'https://kg.qq.com/node/personal?uid=' + inputSingerUid # 组成歌手主页
response_MainPageUrl = requests.get(url = MainPageUrl,headers = headers)
htmlData_MainPageUrl = response_MainPageUrl.text
pattern_SongsAmount = re.compile('的个人主页","content":"作品: (.*?);') # 匹配歌曲总数
result_SongsAmount = pattern_SongsAmount.findall(htmlData_MainPageUrl) # 找到歌曲总数
pattern_SingerInfo = re.compile('<title>(.*?) - 全民K歌</title>') # 匹配歌手信息
result_SingerInfo = pattern_SingerInfo.findall(htmlData_MainPageUrl) # 找到歌手信息
print("You are entering " + str(result_SingerInfo) + "'s Mainpage.")
time.sleep(2) # 延时2秒
print("Now start to download.")
songsAmount = int(''.join(result_SongsAmount))
start = int(songsAmount / 15 + 1)

number_exception = 1 # 初始化异常文件名文件和同名文件数
number_download = 1 # 初始化正在下载数
start_time = time.time() # 初始化开始时间
totalTime = 0.00 # 初始化总耗时
pages = 1 # 初始化页码

while(pages <= start): # 扫描完所有页码后程序结束
    # 获取每首歌曲的shareid
    Url = 'https://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_0&inCharset=GB2312&outCharset=utf-8&format=&g_tk=5381&g_tk_openkey=719182536&nocache=0.8706501019187272&share_uid=' + inputSingerUid +'&type=get_uinfo&_=1551533068931&num=15&start=' + str(pages) # 主页接口
    response_Url = requests.get(url = Url,headers = headers)
    htmlData_Url = response_Url.text
    pattern_SongShareid = re.compile('"shareid": "(.*?)",') # 匹配歌曲shareid
    result_SongShareid = pattern_SongShareid.findall(htmlData_Url) # 找到歌曲shareid
    # print(result_SongShareid)
    result_SongEntry = ['https://node.kg.qq.com/play?s=' + everySongShareid + '&g_f=personal' for everySongShareid in result_SongShareid] # 获取每首歌所在的网页链接
    # print(result_SongEntry)
    # 获取每首歌的Url，并将其下载到本地
    for songEntryUrl in result_SongEntry:
        response_SongEntryUrl = requests.get(url = songEntryUrl,headers = headers) # 向每首歌所在网页发出请求
        htmlData_SongEntryUrl = response_SongEntryUrl.text # 获取每首歌所在网页的html
        pattern_SongUrl = re.compile('"playurl":"http://(.*?)",')  # 匹配下载歌曲Url
        result_SongUrl = pattern_SongUrl.findall(htmlData_SongEntryUrl)  # 找到下载歌曲Url

        # 判断歌曲是否为合唱曲
        pattern_soloorcouple = re.compile('<div class="singer_show singer_show--(.*?)">')
        result_soloorcouple = pattern_soloorcouple.findall(htmlData_SongEntryUrl)
        soloorcouple = "".join(result_soloorcouple)

        # 当为歌曲为独唱曲时
        if(soloorcouple == "solo"):
            pattern_FilenameAndID = re.compile('<title>(.*?)- 全民K歌，KTV交友社区</title>') # 匹配歌曲名和歌手ID
            result_FilenameAndID = pattern_FilenameAndID.findall(htmlData_SongEntryUrl) # 找到歌曲名和歌手ID
            finalResult = list(zip(result_SongUrl, result_FilenameAndID)) # 将歌曲Url和歌曲名和歌手ID存于一个列表中

            for songUrl, songFilenameAndID in finalResult:
                songUrl = "http://" + songUrl
                songFileData = requests.get(url=songUrl, headers=headers).content
                originSongFilenameAndID = songFilenameAndID
                number = 1  # 初始化同名文件数
                try:
                    path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a'
                    while (os.path.isfile(path)):  # 判断是否有同名文件
                        songFilenameAndID = originSongFilenameAndID + "_" + str(number)
                        path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a'
                        number = number + 1
                    with open('QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a', mode='wb') as f:
                        f.write(songFileData)
                        print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                        Utils.progressbar(songUrl, path, songFilenameAndID)
                        number_download = number_download + 1  # 已下载的数量+1
                except (FileNotFoundError, OSError):
                    songFilenameAndID = "Need_to_be_renamed"
                    path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a'
                    while (os.path.isfile(path)):  # 判断是否有同名文件
                        songFilenameAndID = "Need_to_be_renamed" + "_" + str(number_exception)
                        path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a'
                        number_exception = number_exception + 1
                    with open('QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameAndID) + '.m4a', mode='wb') as f:
                        f.write(songFileData)
                        print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                        Utils.progressbar(songUrl, 'QuanMinKGe_SongsDownload\\Need_to_be_renamed.m4a', originSongFilenameAndID)
                        print("The filename has been renamed in \"" + songFilenameAndID + "\" because of system not allowed characters.")
                        number_download = number_download + 1  # 已下载的数量+1

        # 当为歌曲为合唱曲时
        else:
            pattern_Filename = re.compile('"song_name":"(.*?)","tail_name"') # 匹配歌曲文件名
            result_Filename = pattern_Filename.findall(htmlData_SongEntryUrl) # 找到歌曲文件名
            pattern_ID = re.compile('"kg_nick":"(.*?)","ksong_mid"') # 匹配歌手ID
            result_ID = pattern_ID.findall(htmlData_SongEntryUrl) # 找到歌手ID
            pattern_partnerID = re.compile('"hc_nick":"(.*?)","hc_second_sing_count"') # 匹配合唱伙伴ID
            result_partnerID = pattern_partnerID.findall(htmlData_SongEntryUrl) # 找到合唱伙伴ID
            finalResult = list(zip(result_SongUrl, result_Filename, result_ID, result_partnerID)) # 将歌曲Url和歌曲名和歌手ID和合唱伙伴ID存于一个列表中

            for songUrl, songFilename, ID, partnerID in finalResult:
                songUrl = "http://" + songUrl
                songFileData = requests.get(url=songUrl, headers=headers).content
                songFilenameandIDandpartnerID = ID + " & " + partnerID + "-" + songFilename
                originSongFilenameandIDandpartnerID = songFilenameandIDandpartnerID
                number = 1  # 初始化同名文件数
                try:
                    path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a'
                    while (os.path.isfile(path)):  # 判断是否有同名文件
                        songFilenameandIDandpartnerID = originSongFilenameandIDandpartnerID + "_" + str(number)
                        path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a'
                        number = number + 1
                    with open('QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a', mode='wb') as f:
                        f.write(songFileData)
                        print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                        Utils.progressbar(songUrl, path, songFilenameandIDandpartnerID)
                        number_download = number_download + 1  # 已下载的数量+1
                except (FileNotFoundError, OSError):
                    songFilenameandIDandpartnerID = "Need_to_be_renamed"
                    path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a'
                    while (os.path.isfile(path)):  # 判断是否有同名文件
                        songFilenameAndID = "Need_to_be_renamed" + "_" + str(number_exception)
                        path = 'QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a'
                        number_exception = number_exception + 1
                    with open('QuanMinKGe_SongsDownload\\' + Utils.characterChange(songFilenameandIDandpartnerID) + '.m4a', mode='wb') as f:
                        f.write(songFileData)
                        print("\n(" + str(number_download) + "/" + str(songsAmount) + ")", end="")
                        Utils.progressbar(songUrl, 'QuanMinKGe_SongsDownload\\Need_to_be_renamed.m4a', originSongFilenameandIDandpartnerID)
                        print("The filename has been renamed in \"" + songFilenameandIDandpartnerID + "\" because of system not allowed characters.")
                        number_download = number_download + 1  # 已下载的数量+1

    pages = pages + 1 # 每浏览完1页（15首歌）时页数加1

end_time = time.time() # 初始化结束时间
totalTime = end_time - start_time # 计算得到总耗时
print("\nAll songs have been downloaded!")
print("Total Time: " + str(round(totalTime, 2)) + "sec")

# TODO 下载视频MV
# TODO QQ表情符号转emoji
# TODO 当遇到网络连接超时的处理方法
# TODO 加入RGB
# TODO 遇到其他特殊字符时可能导致程序卡住