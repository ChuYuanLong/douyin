import random

from appium import webdriver
import time


"""
此版本适用于抖音6.0.0版本
adb connect 127.0.0.1:62001  连接
测试输入的抖音号 1312235991
[300,307][599,706] 点击滑动802
[601,1109][900,1508]
"""


class DY:
    """
    抖音appium爬虫
    """
    def __init__(self):
        # 配置信息
        self.option = {
            "platformName": "Android",
            "platformVersion": "5.1.1",
            "deviceName": "127.0.0.1:62001",
            # 自动化测试包名
            "appPackage": "com.ss.android.ugc.aweme",
            # 自动化测试Activity
            "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
            'appWaitActivity': '',
            'unicodeKeyboard': True,  # 绕过手机键盘操作，unicodeKeyboard是使用unicode编码方式发送字符串
            'resetKeyboard':True,# 绕过手机键盘操作，resetKeyboard是将键盘隐藏起来
        }
        # 其中的4723就是appium服务启动时的端口号
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.option)
        self.search_count = 1

    def run_click_search(self):
        """
        点击搜索框
        :return:
        """
        time.sleep(3)
        self.driver.tap([(792, 50), (76, 138)], 100)
        print('点击搜索框(成功)')
        time.sleep(2)
        try:
            self.send_search_info()
        except Exception as e:
            raise e
            # print('未知错误')
        finally:
            self.driver.close_app()
            self.driver.quit()

    def send_search_info(self):
        """
        输入查询的信息
        :return:
        """
        # dy_num = input("请在30秒内输入该用户抖音号:")
        # time.sleep(30)
        # dy_num = 1312235991
        global dy_num
        # dy_num = 'XIYEXIYE'
        # dy_num = 'jiangongzi'
        # dy_num = 'suyanwan01'
        # dy_num = 'smx1229'
        dy_num = 'dgfs001'
        self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/ai3').send_keys(dy_num)
        print('输入查询的信息(成功)')
        time.sleep(2)
        try:
            search_person = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/gaz')
        except Exception as e:
            search_person = None
        if search_person:
            self.click_first_search()
        else:
            print(f'用户{dy_num}不存在')

    def click_first_search(self):
        """
        点击第一个进入搜索页面
        :return:
        """
        try:
            search_person = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/gi1')
        except Exception as e:
            search_person = None
        if search_person:
            search_person.click()
            print('点击第一个进入搜索页面(成功)')
            time.sleep(3)
            self.to_first_user_info()
        else:
            print(f'用户{dy_num}不存在')

    def to_first_user_info(self):
        """
        点击第一个用户进入详情页
        :return:
        """
        try:
            first_user = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/gjv')  # 昵称
            # first_user = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/g10')  # 粉丝
        except Exception as e:
            first_user = None
        if first_user:
            first_user.click()
            print('点击第一个用户进入详情页(成功)')
            time.sleep(3)
            self.swipe_video()
        else:
            if self.search_count == 3:
                print(f'用户{dy_num}不存在')
            else:
                print(f'第{self.search_count}次点击详情失败')
                self.search_count += 1
                self.run_click_search()

    def swipe_video(self):
        """
        滑动视频
        :return:
        """
        global swipe_num
        print(self.driver.find_element_by_id('android:id/text1').text)
        try:
            swipe_num = int(self.driver.find_element_by_id('android:id/text1').text.replace(' ', '')[2:])  # 翻页次数
        except:
            swipe_num = 20  # 如果是企业号只爬取20个视频
            print('该用户是企业号')
        print(f'总作品数量为:{swipe_num},翻页次数为:{swipe_num}')
        if swipe_num == 0:
            print('该用户没有视频作品')
        else:
            self.click_video()
            time.sleep(2)
            for i in range(swipe_num):
                self.driver.tap([(799, 1026), (879, 1106)], 200)  # 点击进入评论
                print('点击进入评论(成功)')
                is_comment = self.into_area_or_shop()
                self.swipe_comment(is_comment)

                self.driver.swipe(300, 1200, 300, 400, random.randint(500, 800))  # 视频翻页
                print(f'滑动次数:{i + 1}')
                time.sleep(1)

    def into_area_or_shop(self):
        """
        进入商品或者地区页面
        :return:
        """
        try:
            is_comment = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/aa_')
        except Exception as e:
            is_comment = None
        if is_comment:

            self.driver.tap([(200, 200), (200, 200)], 200)
            time.sleep(1)
        try:
            area = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/ad7')  # 点击进入商品
        except:
            area = None
        if area:
            area.click()
            time.sleep(5)
            try:
                area_exit = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/dtt')
            except:
                area_exit = None
            if area_exit:
                self.driver.tap([(24, 70), (88, 134)], 500)  # 关闭地区
            else:
                self.driver.tap([(29, 62), (106, 139)], 500)  # 关闭商品信息

            print('进入地区或者商品详情成功')
            time.sleep(5)
            # self.driver.tap([(200, 200), (200, 200)], 200)  # 点击关闭评论
            # time.sleep(2)
        else:
            print('该视频没有商品或者地区')
            time.sleep(2)
            # self.driver.tap([(200, 200), (200, 200)], 200)  # 点击关闭评论
            # time.sleep(2)
        return is_comment

    def swipe_comment(self, is_comment):
        """
        滑动评论
        :return:
        """
        swipe_comment_num = 1
        # try:
        #     is_comment = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/aa_')
        # except Exception as e:
        #     is_comment = None
        if is_comment:
            self.driver.tap([(200, 200), (200, 200)], 200)
            print('该视频没有评论')
            time.sleep(1)
        else:

            while True:
                # time.sleep(0.01)

                # try:
                #     open_comment = self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/gee') # 点击展开评论
                #     time.sleep(0.3)
                # except Exception as e:
                #     open_comment = None
                # if open_comment:
                #     open_comment.click()
                #     time.sleep(0.5)
                #     self.driver.swipe(300, 1378, 300, 1000, 200)
                #     time.sleep(0.2)
                # else:
                self.driver.swipe(300, 1378, 300, 600, 200)
                print(f'评论翻页次数:{swipe_comment_num}')
                swipe_comment_num += 1
                try:
                    comment_is_more = self.driver.find_element_by_android_uiautomator('text("暂时没有更多了")')
                    # comment_is_more = self.driver.find_element_by_xpath('//*[@text="暂时没有更多了"]').exists

                except Exception as e:
                    comment_is_more = None
                if comment_is_more:
                    print("爬取评论完成")
                    self.driver.tap([(200, 200), (200, 200)], 200)  # 点击关闭评论
                    time.sleep(1)
                    break

    def click_video(self):
        """
        点击进入作品详情
        :return:
        """
        self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/aj8').click()
        time.sleep(2)
        print('点击视频进入详情(成功)')


if __name__ == "__main__":
    print('启动爬虫')
    dy = DY()
    dy.run_click_search()

