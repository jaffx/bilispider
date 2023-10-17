import logging
import sys
import threading
import time

sys.path.append(".")
from model.data import dataBili

dBili = dataBili.dataBili()


def getUPInfos():
    upInfos = dBili.upInfosInPopList(100)
    print(f"获取UP主数量{len(upInfos)}")
    succ = dBili.saveUPInfos(upInfoList=upInfos)
    print(f"保存UP主数量{succ}")


def getVideoInfos():
    vInfos = dBili.videoInfosInPopList(40)
    print(f"获取视频数量{len(vInfos)}")
    succ = dBili.saveVideoInfo(vInfoList=vInfos)
    print(f"保存视频数量{succ}")


# t1 = threading.Thread(target=getUPInfos, args=())
# t2 = threading.Thread(target=getVideoInfos, args=())
# t1.start()
# time.sleep(5)
getVideoInfos()
