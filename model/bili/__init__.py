import json
import time
import cachetools
import requests
import yaml
import logging
from libs.xyq import fmt
from libs.init import *

COOKIE_PATH = "setting/cookie.yaml"


class biliClnt(object):
    _DEFAULT_REFERER = "https://www.bilibili.com"
    _DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    _DEFAULT_RETRY_DURATION = 2  # second
    logger = logging.getLogger()
    ttlCache = cachetools.TTLCache(maxsize=100, ttl=60)

    @staticmethod
    def checkResponse(resp: requests.Response) -> (str | None):
        """
        检查Response是否合法，status_code是否是200
        :param resp:
        :return:
        """
        if not isinstance(resp, requests.Response):
            return f"expect requests.Response, get type <{type(resp)}>"
        if resp.status_code != 200:
            return f"get http status code {resp.status_code}"

    @staticmethod
    def checkBody(body) -> (str | None):
        if "code" not in body:
            return f"there is no code in body"
        if body["code"] != 0:
            return f"body code is not 0 but {body['code']}, " \
                   f"message {fmt.getDefault(body, 'message', 'None')}"
        if "data" not in body:
            return f"data not in body"

    @staticmethod
    def loadCookie(key="default"):
        with open(COOKIE_PATH) as fp:
            cookies = yaml.load(fp, yaml.SafeLoader)
            fp.close()
        assert key in cookies, f"{key} not exist in cookie.yaml"
        return cookies[key]

    def get(self, url, params=None, headers=None) -> (dict | None):
        _headers = self.defaultHeader()
        if headers is not None:
            _headers.update(headers)
        ok = False
        body = None
        retry = 0
        while not ok and retry < self.retryTime:
            retry += 1
            try:
                resp = requests.get(url=url, params=params, headers=_headers, verify=False)
                # 检查Response
                err = biliClnt.checkResponse(resp)
                if err is not None:
                    biliClnt.logger.warning(f"Response of [{url}] invalid for reason {err}")
                    continue
                # 检查body
                body = resp.json()
                err = biliClnt.checkBody(body)
                if err is not None:
                    biliClnt.logger.warning(f"Data of [{url}] invalid for reason {err}")
                    continue
                ok = True
                break
            except requests.exceptions.JSONDecodeError:
                biliClnt.logger.warning(f"Response of [{url}] is not json")
                time.sleep(biliClnt._DEFAULT_RETRY_DURATION)
            except Exception as e:
                biliClnt.logger.warning(f"Request [{url}] get unknown error{e}")
                time.sleep(biliClnt._DEFAULT_RETRY_DURATION)
        if not ok:
            biliClnt.logger.error(
                f"Request [{url}] failed! params = {json.dumps(params)}, header = {json.dumps(_headers)}")
            return None
        return body

    def post(self, url: str, data=None, params: (dict | None) = None, headers=None) -> (dict | None):
        _headers = self.defaultHeader()
        if headers is not None:
            _headers.update(headers)
        ok = False
        body = None
        retry = 0
        while not ok and retry < self.retryTime:
            try:
                resp = requests.post(url=url, params=params, headers=_headers, data=data, verify=False)
                # 检查Response
                err = biliClnt.checkResponse(resp)
                if err is not None:
                    biliClnt.logger.warning(f"Response of [{url}] invalid for reason {err}")
                    continue
                # 检查body
                body = resp.json()
                err = biliClnt.checkBody(body)
                if err is not None:
                    biliClnt.logger.warning(f"Data of [{url}] invalid for reason {err}")
                    continue
                ok = True
                break
            except requests.exceptions.JSONDecodeError:
                biliClnt.logger.warning(f"Response of [{url}] is not json")
                time.sleep(biliClnt._DEFAULT_RETRY_DURATION)
            except Exception as e:
                biliClnt.logger.warning(f"Request [{url}] get unknown error{e}")
                time.sleep(biliClnt._DEFAULT_RETRY_DURATION)
        if not ok:
            biliClnt.logger.error(
                f"Request [{url}] failed! params = {json.dumps(params)}, header = {json.dumps(_headers)}, data = {json.dumps(data)}")
            return None
        return body

    def __init__(self):
        self.retryTime = 3
        self.cookieKey = "default"
        self.cookie = self.loadCookie(self.cookieKey)

    def defaultHeader(self):
        return {
            "Referer": biliClnt._DEFAULT_REFERER,
            "User-Agent": biliClnt._DEFAULT_UA,
            "Cookie": self.cookie
        }

    def setRetryTime(self, value):
        self.retryTime = value


fileHandler.setLevel(logging.WARNING)
fileHandler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
biliClnt.logger.addHandler(fileHandler)
