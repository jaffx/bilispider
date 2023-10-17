from . import *
Base = declarative_base()

class UPInfo(Base):
    id = Column(BigInteger, primary_key=True, comment="自增ID")
    name = Column(String(128), nullable=False, comment="Up名称")
    mid = Column(String(32), nullable=False, index=True, comment="UP主mid")
    sex = Column(String(10), comment="性别")
    sign = Column(String(1024), comment="个签")
    level = Column(Integer, comment="用户等级")
    title = Column(String(1024), comment="头衔")
    face = Column(String(2048), comment="封面")
    follower = Column(Integer, comment="粉丝数量")
    ext = Column(String(4096), comment="Json数据")
    created_at = Column(DateTime, default=sqlalchemy.func.now())
    updated_at = Column(DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    __tablename__ = 'up_infos'
    __table_args__ = (
        sqlalchemy.Index("idx_mid", "mid"),
    )


Base.metadata.create_all(engine, checkfirst=True)


class DaoUpInfo(DaoBase):
    def __init__(self):
        DaoBase.__init__(self)

    def insertUPInfo(self, info):
        _upInfo = UPInfo(**info)
        _upId = self.add(_upInfo)
        if not _upId:
            self.logger.error("Dao addUpInfo failed")
            return None
        return _upId

    def multiInsertUPInfos(self, infos):
        _upInfos = []
        for info in infos:
            _upInfos.append(UPInfo(**info))
        succ = self.add_all(_upInfos)
        return succ

    def getUpInfoByMID(self, mid: str):
        try:
            _upInfo = self.session.query(UPInfo).filter(UPInfo.mid == mid).all()
        except Exception as e:
            self.logger.Error(f"Dap getUpInfoById failed for reason {e}")
            return None
        if not _upInfo:
            return None
        return _upInfo[0]

    def updateUpInfoById(self, mid: str, info):
        affected = self.session.query(UPInfo).filter(UPInfo.mid == mid).update(info)
        self.session.commit()
        return affected

    def isUpInfoExist(self, mid: str):
        num = self.session.query(UPInfo.mid).filter(UPInfo.mid == mid).count()
        return num > 0
