import time

from futuquant.timluo import Global


class OperaSystem:
    status = Global.SYSTEM_STATUS_EMPTY
    callOperator = None
    exitOperator = None

    def run(self):
        return

    def runSystem(self, stockCode=Global.TENCENT,
                  startTime=time.strftime("%Y-%m-%d", time.localtime()),
                  endTime=time.strftime("%Y-%m-%d", time.localtime())):
        return

    def __init__(self, callOperator, exitOperator):
        self.callOperator = callOperator
        self.exitOperator = exitOperator
        return
