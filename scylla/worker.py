import requests
from playwright.sync_api import sync_playwright
from pyquery import PyQuery
from requests import Response
from typing import Union

from scylla.loggings import logger

DEFAULT_TIMEOUT_SECONDS = 10

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/89.0.4389.90 Safari/537.36 '


class Worker:

    def __init__(self):
        """Initialize the worker object
        """
        # Store the playwright instance to keep it alive
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

        self.requests_session = requests.Session()
        self.requests_session.headers['User-Agent'] = DEFAULT_USER_AGENT


    def stop(self):
        """Clean the session
        """
        try:
            if self.browser is not None:
                self.browser.close()
        except Exception as e:
            self.browser = None

        try:
            if self.playwright is not None:
                self.playwright.stop()
                self.playwright = None
        except Exception as e:
            self.playwright = None

        try:
            if self.requests_session is not None:
                self.requests_session.close()
        except Exception as e:
            self.requests_session = None

    def reinit(self):
        self.stop()
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

        self.requests_session = requests.Session()
        self.requests_session.headers['User-Agent'] = DEFAULT_USER_AGENT


    def get_html(self, url: str, render_js: bool = True) -> Union[PyQuery, None]:
        """Get html from a specific URL

        :param url: the URL
        :param render_js: [whether to render js], defaults to True
        :param render_js: bool, optional
        :return: [the HTML string]
        :rtype: str
        """
        if self.browser is None:
            self.reinit()

        if render_js:
            return self._get_html_js(url)
        else:
            return self._get_html_no_js(url)

    def _get_html_no_js(self, url: str) -> Union[PyQuery, None]:
        try:
            # TODO: load config for timeout
            response: Response = self.requests_session.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        except requests.RequestException:
            logger.warning('[Worker] Cannot get this url: ' + url)
            return None
        except (KeyboardInterrupt, SystemExit, InterruptedError) as e:
            logger.warning(f'[Worker] exiting... Exception: {e}')
            self.stop()
            return None
        if response.ok:
            doc = PyQuery(response.text)
            return doc
        else:
            logger.debug(f'Request for {url} failed, status code: {response.status_code}')
            return None

    def _get_html_js(self, url: str) -> Union[PyQuery, None]:
        try:
            page = self.browser.new_page()
            try:
                response = page.goto(url=url, timeout=DEFAULT_TIMEOUT_SECONDS * 1000, wait_until='domcontentloaded')
                
                if not response:
                    logger.debug(f'Request for {url} failed because response is None')
                    return None
                    
                if response.ok:
                    content = page.content()
                    doc = PyQuery(content)
                    return doc
                else:
                    logger.debug(f'Request for {url} failed, status code: {response.status}')
                    return None
            except Exception as e:
                logger.warning(f'[Worker] Error while loading page {url}: {e}')
                return None
            finally:
                # Always close the page to prevent resource leaks
                page.close()
        except Exception as e:
            # This will catch browser-related errors like browser being closed
            logger.error(f'[Worker] Browser error for {url}: {e}')
            # Try to reinitialize if the browser is in a bad state
            if "is closed" in str(e) or "Event loop is closed" in str(e):
                logger.info('[Worker] Reinitializing browser due to closed state')
                self.reinit()
            return None
