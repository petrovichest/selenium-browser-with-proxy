import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import zipfile


class SeleniumChromeBrowser:

    def __init__(self, profile_name=None, proxy=None):
        if not profile_name:
            self.profile_name = 'Default'
        else:
            self.profile_name = profile_name
        self.proxy = proxy

        self.run()

    def start_browser(self):
        if not self.profile_name:
            profile_name = 'Default'
        print(f'Starting browser - {self.profile_name}')
        chrome_options = Options()
        if self.proxy:
            if '@' in self.proxy:
                # pass
                chrome_options.add_extension(self.proxy_with_password(self.proxy))
            else:
                proxy_ip = self.proxy.split(':')[0]
                proxy_port = self.proxy.split(':')[1]

                chrome_options.add_argument('--proxy-server=' + proxy_ip + ':' + proxy_port)

        # chrome_options.add_extension('chrome_extensions\\fingerprint.crx')
        # chrome_options.add_extension('chrome_extensions\\font.crx')
        # chrome_options.add_extension('chrome_extensions\\webgl.crx')
        # chrome_options.add_extension('chrome_extensions\\random_useragent.crx')
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--ignore-ssl-errors')
        self.user_path = f'{os.getcwd()}/Browser_profile/{self.profile_name}'
        chrome_options.add_argument(f'user-data-dir={self.user_path}')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

        # self.driver.set_window_size(1920, 1080)
        # self.driver.get('https://2ip.ru/')
        print('Browser started, proxy:', self.proxy)
        return True

    def proxy_with_password(self, proxy):

        PROXY_HOST = proxy.split(':')[0]
        PROXY_PORT = proxy.split(':')[1].split('@')[0]
        PROXY_USER = proxy.split(':')[1].split('@')[1]
        PROXY_PASS = proxy.split(':')[2]

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        # path = os.path.dirname(os.path.abspath(__file__))
        # chrome_options = webdriver.ChromeOptions()

        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        # chrome_options.add_extension(pluginfile)
        return pluginfile

    def run(self):
        self.start_browser()
        return self.driver

if __name__ == '__main__':
    proxy = input('Вставьте прокси с паролем: ')
    # proxy = '46.8.192.8:5500@bnAMEc:0LFtD4yMAa'
    driver = SeleniumChromeBrowser(proxy=proxy).driver
    driver.get('https://2ip.ru')
    input(123123)