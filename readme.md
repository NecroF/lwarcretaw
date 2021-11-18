# 安装环境
安装anaconda，配置环境

    conda create -n watercrawl python=3.8
    conda activate watercrawl
    conda install ffmpeg you-get scrapy requests pymongo tqdm protego -c conda-forge -y

在你任意指定的路径下创建scrapy工程

    scrapy startproject NAME_OF_SPIDER

之后在NAME_OF_SPIDER/spider/下新建文件NAME_YOU_LIKE.py
完成基本功能只需要重写如下部分，参考已经完成的例子，主要都在创建的NAME_YOU_LIKE.py里

 - 指定name
 - 重写start_requests，功能是构建request，其中回调prase()
 - 重写prase，功能是处理response，通常需要yield request、yield item
 - 在items.py中加入待爬取的词条(复制粘贴例子中的即可)


