# -*- coding: utf-8 -*-
import os
import logging
import traceback

from click.testing import CliRunner
from hamcrest import (assert_that, all_of, has_property, has_properties,
                      anything)

from upversion import cli

logger = logging.getLogger('tests.cli')


class CommandTest(object):
    def setup(self):
        self.setup_runner()

    def setup_runner(self):
        self.runner = CliRunner()
        self.result = None

    def run(self, args, **kwargs):
        logger.info(u'run: upversion' + u' '.join(args))

        if hasattr(self, 'defargs'):
            args += self.defargs

        self.result = self.runner.invoke(cli, args, **kwargs)

        if self.result.exit_code:
            logger.info(u'error result: \n' + self.result.output)
        if self.result.exception:
            logger.info(u'exception raised: \n' +
                u''.join(traceback.format_exception(*self.result.exc_info)))

        return self.result

    def assert_result(self, *matchers, **kwargs):
        result = kwargs.get('result', self.result)

        assert_that(result, all_of(
            has_property('exit_code', kwargs.pop('exit_code', 0)),
            has_property('output', kwargs.pop('output', anything())),
            has_properties(**kwargs),
            *matchers
        ))


def here(*parts):
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), *parts)
