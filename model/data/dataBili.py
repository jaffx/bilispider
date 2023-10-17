import json
import time

from . import *
from ..bili import UPClnt, popularClnt as popClnt, videoClnt
from ..dao import daoUpInfo, daoVideoInfo


class dataBili(dataLayerBase):
    bcUP = UPClnt.UPClnt()
    bcPop = popClnt.popularClnt()
    bcVideo = videoClnt.videoClnt()
    daoUP = daoUpInfo.DaoUpInfo()
    daoVideo = daoVideoInfo.DaoVideoInfo()

    def __init__(self):
        dataLayerBase.__init__(self)
        pass

    def upInfosInPopList(self, limited=100, sleepDuration=0.5) -> (list | None):
        mids = self.bcPop.upIDInPopList(limited=limited)
        _upInfoList = []
        for mid in mids:
            info = self.bcUP.getUPInfo(mid)
            _upInfoList.append(info)
            time.sleep(sleepDuration)
        return _upInfoList

    def videoInfosInPopList(self, limited=100) -> (list | None):
        bvids = self.bcPop.bvidInPopList(limited)
        _vInfoList = self.bcVideo.getVideoInfosWithTheadingPool(bvids)
        return _vInfoList

    def saveUPInfos(self, upInfoDict: dict = None, upInfoList: list = None) -> int:
        """
        保存UP主信息
        :param upInfoDict: 通过字典格式传入，key为mid，value为info
        :param upInfoList: 通过列表格式传入，值为info字典，必须有mid字段
        :return:
        """
        assert upInfoDict is not None or upInfoList is not None, "There is no video infos in params"
        if upInfoDict is None:
            upInfoDict = {}
            for info in upInfoList:
                if "mid" not in info:
                    self.logger.warning(f"There is no mid in the info ->  {json.dumps(info)}")
                    continue
                upInfoDict[info["mid"]] = info
            if len(upInfoDict) == 0:
                return 0
            success = 0
            for mid in upInfoDict:
                try:
                    if not self.daoUP.isUpInfoExist(mid=mid):
                        _id = self.daoUP.insertUPInfo(upInfoDict[mid])
                        if _id:
                            success += 1
                    else:
                        _affected = self.daoUP.updateUpInfoById(mid, upInfoDict[mid])
                        if _affected:
                            success += 1
                except Exception as e:
                    self.logger.warning(f"Add UpInfo {json.dumps(upInfoDict[mid])} Error for reason <{e}>")
            return success

    def saveVideoInfo(self, vInfoDict=None, vInfoList=None) -> int:
        assert vInfoDict is not None or vInfoList is not None, "There is no video infos in params"
        if vInfoDict is None:
            vInfoDict = {}
            for info in vInfoList:
                if "bvid" not in info:
                    self.logger.warning(f"There is no bvid in video info -> {json.dumps(info)}")
                    continue
                vInfoDict[info["bvid"]] = info
            if len(vInfoDict) == 0:
                return 0
            success = 0
            for bvid in vInfoDict:
                try:
                    if not self.daoVideo.isVideoInfoExist(bvid=bvid):
                        _id = self.daoVideo.insertVideoInfo(info)
                        if _id:
                            success += 1
                    else:
                        _affected = self.daoVideo.updateVideoInfoById(bvid=bvid, info=info)
                        if _affected:
                            success += 1
                except Exception as e:
                    self.logger.warning(f"Add VideoInfo <{json.dumps(vInfoDict[bvid])}> Error for reason <{e}>")
            return success
