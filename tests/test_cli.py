# -*- coding: utf-8 -*-
import io
import os
import shutil
import tempfile
import contextlib

from tests import CommandTest, here
from hamcrest import assert_that, contains_string, matches_regexp

EXAMPLE = here('examples', 'setup_0.0.0.py')


@contextlib.contextmanager
def version_file(version='0.0.0'):
    with tempfile.NamedTemporaryFile() as tmp:
        with io.open(EXAMPLE, encoding='utf-8') as stream:
            tmp.file.write(stream.read().replace('0.0.0', version).encode('utf-8'))
            tmp.file.flush()
        yield tmp.name


class TestRootCommand(CommandTest):
    def test_it_shows_version(self):
        self.run(['--version'])

        self.assert_result(output=matches_regexp(r'version \d+\.\d+\.\d+.*'))


class TestView(CommandTest):
    defargs = ['--path', EXAMPLE]

    def test_it_should_update_major(self):
        self.run(['view'] + ['--major'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.0'))

    def test_it_should_update_minor(self):
        self.run(['view'] + ['--minor'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.0'))

    def test_it_should_update_revision(self):
        self.run(['view'] + ['--revision'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.1'))

    def test_it_should_update_dev(self):
        self.run(['view'] + ['--dev'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.0.dev1'))

    def test_it_should_update_post(self):
        self.run(['view'] + ['--post'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.0.0.post1'))

    def test_it_should_update_major_and_revision(self):
        self.run(['view'] + ['--major', '--revision'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.0.1'))

    def test_it_should_update_minor_and_revision(self):
        self.run(['view'] + ['--minor', '--revision'])

        self.assert_result(output=contains_string('From 0.0.0 to 0.1.1'))

    def test_it_should_update_major_and_minor_and_revision(self):
        self.run(['view'] + ['--major', '--minor', '--revision'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.1'))

    def test_it_should_update_all_at_the_same_time(self):
        self.run(['view'] + ['--major', '--minor', '--revision', '--dev', '--post'])

        self.assert_result(output=contains_string('From 0.0.0 to 1.1.1.post1.dev1'))

    def test_it_should_update_given_var(self):
        self.run(['view'] + ['--major', '--minor', '--revision', '--var', 'no_version'])

        self.assert_result(output=contains_string('From 1.1.1 to 2.1.1'))

    def test_it_should_remove_dev_when_final(self):
        with version_file('0.0.0.dev1') as path:
            self.defargs = ['--path', path]

            self.run(['view'] + ['--final'])

        self.assert_result(output=contains_string('From 0.0.0.dev1 to 0.0.0'))

    def test_it_should_remove_post_when_final(self):
        with version_file('0.0.0.post1') as path:
            self.defargs = ['--path', path]

            self.run(['view'] + ['--final'])

        self.assert_result(output=contains_string('From 0.0.0.post1 to 0.0.0'))

    def setup_fixture(self):
        self.defargs = ['--path', EXAMPLE]


class TestUp(CommandTest):
    def test_it_should_replace_version(self):
        initial = '0.0.0'
        expected = '1.1.1.post1.dev1'

        with self.runner.isolated_filesystem() as path:
            example_path = os.path.join(path, 'setup.py')
            shutil.copyfile(EXAMPLE, example_path)

            self.run(['up', '--major', '--minor', '--revision', '--dev', '--post'])

            self.assert_result(output=contains_string('From {} to {}'.format(initial, expected)))
            self.assert_result(output=contains_string('writing "{}"'.format(example_path)))
            assert_that(open(example_path).read(), contains_string("version='{}'".format(expected)))
