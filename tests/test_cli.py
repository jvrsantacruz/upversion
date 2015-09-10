# -*- coding: utf-8 -*-
from tests import CommandTest, here
from hamcrest import contains_string


class TestView(CommandTest):
    defargs = ['--path', here('examples', 'setup_0.0.0.py')]

    def test_it_should_update_major(self):
        self.run(['view'] + ['--major'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.0'))

    def test_it_should_update_minor(self):
        self.run(['view'] + ['--minor'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.0'))

    def test_it_should_update_patch(self):
        self.run(['view'] + ['--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.1'))

    def test_it_should_update_major_and_patch(self):
        self.run(['view'] + ['--major', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.1'))

    def test_it_should_update_major_and_minor(self):
        self.run(['view'] + ['--major', '--minor'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.0'))

    def test_it_should_update_minor_and_patch(self):
        self.run(['view'] + ['--minor', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.1'))

    def test_it_should_update_major_and_minor_and_patch(self):
        self.run(['view'] + ['--major', '--minor', '--patch'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.1'))
