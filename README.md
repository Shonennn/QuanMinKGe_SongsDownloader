# 全民K歌歌曲下载器

## 基本介绍

前4个commit都没有readme.md，现在才开始写。

这是一个用python写的爬虫程序，主要运用requests和re库，曾经想过beautifulsoup4，然而全民K歌的歌曲URL居然不是在HTML标签里，因此只能通过正则表达式来匹配相关字段。

目前还有些可以完善的功能，抽空继续写吧。

## 目前已有的功能

+ 通过使用者输入歌手的uid，获取该歌手的所有歌曲和MV的URL，并将其下载下来，保存到指定目录
+ 程序会实时输出正在下载的文件名和文件大小以及下载进度
+ 当文件名存在windows不允许的字符时，会将其替换为“_”或“：”

* 当文件保存时遇上FileNotFoundError、 OSError错误时，文件名将会被替换为“Need_to_be_renamed”
* 合唱曲的文件名会包含两个歌手的ID（一个人完成的合唱曲也会有两个相同的名字，例如：歌手 & 歌手 - 歌名）
* 下载结束时会输出总耗时

## 注意事项

* 一旦输入uid并敲下回车，**除非自己关闭程序，否则程序不会停下**
* 偶尔可能会因为主机网络或服务器的问题，发出请求的时间会长一点，**不排除一直卡住的情况**
* **本程序仅用于学习，转载请标明出处**

## 可能还会加入的功能

* 当遇到网络连接超时时的处理方法
* 加入RGB控制台的显示