from django.test.runner import DiscoverRunner


class NoCreateTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return {}

    def teardown_databases(self, old_config, **kwargs):
        return
