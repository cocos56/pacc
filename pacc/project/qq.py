from .project import Project


class ResourceID:
    input = 'com.tencent.mobileqq:id/input'  # 输入框
    fun_btn = 'com.tencent.mobileqq:id/fun_btn'  # 发送按钮


class QQ(Project):
    def __init__(self, deviceSN):
        super(QQ, self).__init__(deviceSN, False)

    def sendMsg(self, msg):
        self.uIAIns.click(ResourceID.input)

        self.adbIns.inputTextWithB64(msg)
        self.uIAIns.click(ResourceID.fun_btn)
