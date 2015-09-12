# -*- coding: utf-8 -*-
import os
import shutil

from tests import CommandTest, here
from hamcrest import assert_that, contains_string

EXAMPLE = here('examples', 'setup_0.0.0.py')


class TestView(CommandTest):
    defargs = ['--path', EXAMPLE]

    def test_it_should_update_major(self):
        self.run(['view'] + ['--major'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.0'))

    def test_it_should_update_minor(self):
        self.run(['view'] + ['--minor'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.0'))

    def test_it_should_update_patch(self):
        self.run(['view'] + ['--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.1'))

    def test_it_should_update_dev(self):
        self.run(['view'] + ['--dev'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.0.dev1'))

    def test_it_should_update_major_and_minor(self):
        self.run(['view'] + ['--major', '--minor'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.0'))

    def test_it_should_update_major_and_patch(self):
        self.run(['view'] + ['--major', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.1'))

    def test_it_should_update_minor_and_patch(self):
        self.run(['view'] + ['--minor', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.1'))

    def test_it_should_update_major_and_minor_and_patch(self):
        self.run(['view'] + ['--major', '--minor', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.1'))


class TestUp(CommandTest):
    def test_it_should_replace_version(self):
        initial = '0.0.0'
        expected = '1.1.1.dev1'

        with self.runner.isolated_filesystem() as path:
            example_path = os.path.join(path, 'setup.py')
            shutil.copyfile(EXAMPLE, example_path)

            self.run(['up', '--major', '--minor', '--patch', '--dev'])

            self.assert_result(output=contains_string('From {} to {}'.format(initial, expected)))
            self.assert_result(output=contains_string('writing "{}"'.format(example_path)))
            assert_that(open(example_path).read(), contains_string("version='{}'".format(expected)))
