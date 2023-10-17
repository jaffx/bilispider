import json
import time
import enum
import logging
from libs.xyq import fmt
from libs.init import *


class TaskStatus(enum.Enum):
    WAITING = 1
    RUNNING = 2
    FINISHED = 3
    ERROR = -1
    KILLED = -2


TaskStatusName = {
    TaskStatus.WAITING: "WAITING",
    TaskStatus.RUNNING: "RUNNING",
    TaskStatus.FINISHED: "FINISHED",
    TaskStatus.ERROR: "ERROR",
    TaskStatus.KILLED: "KILLED",
}


class TaskBase(object):
    __taskName__ = "Base"

    def __init__(self):
        self.__updateTime__ = time.time()
        self.__status__ = TaskStatus.WAITING
        self.__createTime__ = time.time()
        self.__startTime__ = 0
        self.__finishTime__ = 0

    def before(self):
        pass

    def main(self):
        pass

    def after(self):
        pass

    def run(self):
        self.__changeStatus__(TaskStatus.RUNNING)
        self.__startTime__ = time.time()
        try:
            self.before()
            if self.__status__ == TaskStatus.KILLED:
                return
            self.main()
            self.after()
        except Exception:
            self.__changeStatus__(TaskStatus.ERROR)
        else:
            self.__changeStatus__(TaskStatus.FINISHED)
        self.__finishTime__ = time.time()

    def __changeStatus__(self, status: TaskStatus):
        self.__updateTime__ = time.time()
        self.__status__ = status

    def kill(self):
        self.__changeStatus__(TaskStatus.KILLED)

    def getTaskInfo(self, useJson=True):
        info = {
            "taskName": self.__taskName__,
            "status": TaskStatusName[self.__status__],
            "createTime": fmt.timeStamp2Str(self.__createTime__),
            "startTime": fmt.timeStamp2Str(self.__startTime__),
            "finishTime": fmt.timeStamp2Str(self.__finishTime__),
            "duration": self.__finishTime__ - self.__startTime__,
        }
        if useJson:
            return json.dumps(info, ensure_ascii=False)
        return info
