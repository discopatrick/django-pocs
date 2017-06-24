from django.test.runner import DiscoverRunner

class RestoreDBDumpRunner(DiscoverRunner):

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        print('Running the "RestoreDBDumpRunner" test runner')
        super(RestoreDBDumpRunner, self).run_tests(test_labels, extra_tests, **kwargs)
