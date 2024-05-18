from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


@skip
class MutablePageTestMixin(StaticLiveServerTestCase):
    """Without reload page for each test method mixin.

    A one-time ``page`` load is used for all test methods.

    Note
    ----
        -- Set ``base_url`` attr value at derived class
        -- Runs methods alphabetically
        -- ``setUp`` once, when start class test
        -- ``tearDown`` once, when end class test
        -- Reused page state
        -- Runs test not applies --headed

    Example
    -------
    class TestHomePage(MutablePageTestMixin):

        base_url = 'https://github.com/'
        page: Page = None
        response = None

        def test_page_status(self):
            assert self.response.ok

        def test_page_title(self):
            expect(self.page).to_have_title('GitHub')
    """

    base_url = None

    @classmethod
    def setUpClass(cls):
        """Start playwright."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.page = cls.browser.new_page()
        cls.response = cls.page.goto(cls.base_url)

    @classmethod
    def tearDownClass(cls):
        """Stop playwright."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()


@skip
class ReloadPageTestMixin(StaticLiveServerTestCase):
    """Reload page for each test method mixin.

    Note
    ----
        -- Set ``base_url`` attr value at derived class
        -- Runs methods alphabetically
        -- Runs test not applies --headed
    """

    base_url = None

    @classmethod
    def setUp(cls):
        """Start playwright."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.page = cls.browser.new_page()
        cls.response = cls.page.goto(cls.base_url)

    @classmethod
    def tearDown(cls):
        """Stop playwright."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
