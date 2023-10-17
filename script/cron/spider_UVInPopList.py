import sys

sys.path.append(".")

import model.task.spider.TaskSpiderUPVidInPop as TaskSpiderUPVidInPop

task = TaskSpiderUPVidInPop.TaskSpiderUPVidInPop()

task.run()
print(task.getTaskInfo())
