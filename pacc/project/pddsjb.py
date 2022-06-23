from random import randint
from datetime import datetime
from ..tools import findAllWithRe, findAllNumsWithRe, sleep, SliderCaptcha
from .project import Project
from .qq import QQ

statement = '本链接仅用于对抗电商诈骗，打击无良商家，不能用于敲诈勒索正常商家。本链接免费提供，严禁用于割韭菜，收取任何形式的费用\n' \
            '投诉反馈请联系：人民老板-徐哥 18739776523\n' \
            '座右铭：要始终坚持为人民服务而不是为人民币服务，君子爱财取之有道，不义之财切记不可取'

keywords = ['货', '车', '衣', '裤', '鞋', '书', '食', '机', '电', '瓜', '果', '件', '礼',
            '酒', '机', '家', '床', '柜']


class Activity:
    MainFrameTabActivity = 'com.xunmeng.merchant/com.xunmeng.merchant.ui.MainFrameTabActivity'
    TransparentFullscreenWebActivity = 'com.xunmeng.merchant/com.xunmeng.merchant.ui.TransparentFullscreenWebActivity'


class Class:
    EditText = 'android.widget.EditText'


class Bounds:
    InputBox = '[246,-1][903,-1]'  # 搜索框


class PDDSJB(Project):
    def __init__(self, deviceSN):
        super(PDDSJB, self).__init__(deviceSN)
        self.qIns = QQ('002001003')
        self.walkedCnt = 0
        self.succeededCnt = 0

    def decryptCaptcha(self):
        errCnt = 1
        while Activity.TransparentFullscreenWebActivity in self.adbIns.get_current_focus():
            # self.qIns.sendMsg("采集器于%s碰到验证码，正在尝试第%d次破解" % (datetime.now(), errCnt))
            x = SliderCaptcha.getX(self.uIAIns.get_screen())
            self.adbIns.swipe(226, 1108, x + 160, 1108, 3000)
            sleep(6)
            errCnt += 1
            if self.uIAIns.click(text='立即刷新'):
                sleep(6)
        # if not errCnt == 1:
        #     self.qIns.sendMsg("采集器于%s成功破解验证码，共尝试了%d次" % (datetime.now(), errCnt))

    def mainloop(self):
        # self.qIns.sendMsg("采集器于%s开始启动" % datetime.now())
        while True:
            try:
                self.loop()
            except Exception as e:
                print(e)

    def loop(self):
        keyword = keywords[randint(0, len(keywords) - 1)]
        # self.qIns.sendMsg("正在扫描关键词【%s】，开始扫描时间%s" % (keyword, datetime.now()))
        self.search(keyword)
        while True:
            self.enterProductDetailsPage()
            self.swipe()

    def swipe(self):
        self.adbIns.swipe(536, 900, 536, 360)
        sleep(2, False)

    def openApp(self):
        super(PDDSJB, self).openApp(Activity.MainFrameTabActivity)
        sleep(9, False)
        self.decryptCaptcha()

    def enterShoppingInterface(self):
        try:
            self.reopenApp()
            self.uIAIns.click(text='我的')
            self.uIAIns.click(text='拼多多批发')
            sleep(6)
            self.decryptCaptcha()
        except FileNotFoundError as e:
            print(e)
            self.enterShoppingInterface()

    def search(self, keyword):
        print(keyword)
        self.enterShoppingInterface()
        self.uIAIns.getCurrentUIHierarchy()
        self.uIAIns.click(Class=Class.EditText)
        self.uIAIns.click(Class=Class.EditText)
        self.adbIns.input_text(keyword)
        self.adbIns.press_enter_key()
        self.uIAIns.click(text='价格')

    def getValidItems(self):
        rd = self.uIAIns.getDict(index='0', Class='android.view.View', bounds='[0,-1][1080,1920]')[
            'node']
        rawItems = [i for i in rd if 'node' in i]
        validItems = []
        for i in rawItems:
            index = i['@index']
            name = i['node'][1]['@text']
            bounds = i['node'][3]['node'][1]['@bounds']
            price = i['node'][3]['node'][1]['@text']
            if not bounds == '[0,0][0,0]':
                print(index, name, price, bounds)
                validItems.append((index, name, float(price), bounds))
            if len(validItems) >= 2:
                break
        return validItems

    def getURLFromProductDetailPage(self, productInfo):
        self.uIAIns.click(bounds='[936,72][1032,204]')
        self.uIAIns.click(text='复制链接')
        data = findAllWithRe(self.adbIns.get_data_from_clipboard(), '(.+)&type=.+')[0]
        print(data)
        index, name, price, discountInformation = productInfo
        self.qIns.sendMsg("索引号：%s\n商品名：%s\n价格：%s\n最大折扣：≥%s件 %s折\n商品链接：%s\n声明：%s" % (
            index, name, price, discountInformation[0], discountInformation[1], data, statement))

    def enterProductDetailsPage(self):
        validItems = self.getValidItems()
        if validItems[0][2] > validItems[1][2]:
            flag = self.clickByBoundsSafely(validItems[1][3])
            index, name, price = validItems[1][:3]
        else:
            flag = self.clickByBoundsSafely(validItems[0][3])
            index, name, price = validItems[0][:3]
        if not flag:
            self.enterProductDetailsPage()
            return
        self.decryptCaptcha()
        d = findAllWithRe(self.uIAIns.getDict(text='≥')['@text'], '≥(\d+)件 (\d\.\d)折')[0]
        discountInformation = [int(d[0]), float(d[1])]
        if discountInformation[0] <= 10 and discountInformation[1] <= 2:
            self.getURLFromProductDetailPage((index, name, price, discountInformation))
            self.succeededCnt += 1
        self.adbIns.press_back_key()
        # if self.walkedCnt % 50 == 0: self.qIns.sendMsg('状态报告：已遍历%d条，共发现%d条链接，当前时间：
        # %s' % (self.walkedCnt, self.succeededCnt, datetime.now()))
        self.walkedCnt += 1

    def clickByBoundsSafely(self, bounds):
        cP = self.uIAIns.getCPFromTPs(findAllNumsWithRe(bounds))
        if 320 < cP[1] < 1600:
            self.uIAIns.tap(cP)
            return True
        self.adbIns.swipe(536, 600, 536, 360)
        return False
