from . import *

Base = declarative_base()


class VideoInfo(Base):
    id = Column(BigInteger, primary_key=True, comment="自增ID")
    aid = Column(String(32), nullable=False, comment="aid")
    bvid = Column(String(32), nullable=False, comment="bvid")
    tid = Column(Integer, comment="类型id")
    tname = Column(String(32), comment="类型名称")
    pic = Column(String(2048), comment="视频封面")
    title = Column(String(2048), comment="视频标题")
    pubdate = Column(BigInteger, comment="创建时间，unix时间戳")
    desc = Column(String(4096), comment="视频简介")
    duration = Column(Integer, comment="视频时长")
    upname = Column(String(32), comment="UP主名称")
    mid = Column(String(32), comment="mid")
    like = Column(BigInteger, comment="点赞量")
    coin = Column(BigInteger, comment="投币量")
    favorite = Column(BigInteger, comment="收藏量")
    share = Column(BigInteger, comment="转发量")
    view = Column(BigInteger, comment="播放量")
    danmaku = Column(BigInteger, comment="弹幕数量")
    reply = Column(BigInteger, comment="评论数量")
    his_rank = Column(BigInteger, comment="历史排名")
    created_at = Column(DateTime, default=sqlalchemy.func.now())
    updated_at = Column(DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    __tablename__ = 'video_infos'
    __table_args__ = (
        sqlalchemy.Index("idx_mid_pubdate", "mid", "pubdate"),
        sqlalchemy.Index("idx_aid", "aid"),
        sqlalchemy.Index("idx_bvid", "bvid"),
    )


Base.metadata.create_all(engine, checkfirst=True)


class DaoVideoInfo(DaoBase):
    def __init__(self):
        DaoBase.__init__(self)

    def insertVideoInfo(self, info: dict) -> int | None:
        try:
            _videoInfo = VideoInfo(**info)
        except Exception as e:
            self.logger.error(f"Transform to VideoInfo failed for reason {e}")
            return None
        _id = self.add(_videoInfo)
        if _id is None:
            self.logger.warning(f"Insert video info fail!")
            return None
        return _id

    def updateVideoInfoById(self, aid=None, bvid=None, info: dict = None):
        assert aid is not None or bvid is not None, "Aid or bvid must be specified"
        if bvid:
            affected = self.session.query(VideoInfo).filter(VideoInfo.bvid == bvid).update(info)
        else:
            affected = self.session.query(VideoInfo).filter(VideoInfo.aid == aid).update(info)
        return affected

    def isVideoInfoExist(self, aid=None, bvid=None) -> bool:
        assert aid is not None or bvid is not None
        if bvid:
            num = self.session.query(VideoInfo).filter(VideoInfo.bvid == bvid).count()
        else:
            num = self.session.query(VideoInfo).filter(VideoInfo.aid == aid).count()
        return num > 0
