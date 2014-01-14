#!/usr/bin/python2
import unittest
from unittest import expectedFailure
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from bacula_parser import remove_comment, baculaParser


class Test(unittest.TestCase):

    maxDiff = 2000

    def test_remove_comment(self):
        check_str = 'Job {\n}\n'
        self.assertMultiLineEqual(remove_comment('comment.conf'), check_str)

    def test_one_section(self):
        check_list = [['Job',
                      ['Name', 'RestoreFiles'],
                      ['Type', 'Restore'],
                      ['Client', 'client.example.com'],
                      ['FileSet', 'Full Set'],
                      ['Storage', 'File'],
                      ['Pool', 'Default'],
                      ['Messages', 'Standard'],
                      ['Where', '/tmp/bacula-restores']]]

        self.assertListEqual(
            baculaParser('one_section.conf').asList(),
            check_list
        )

    def test_recursive_section(self):
        check_list = [['FileSet',
                      ['Name', 'Full Set'],
                      ['Include',
                       ['Options', ['signature', 'MD5']],
                       ['File', '/usr/sbin']],
                      ['Exclude',
                       ['File', '/var/lib/bacula'],
                       ['File', '/tmp'],
                       ['File', '/proc'],
                       ['File', '/tmp'],
                       ['File', '/.journal'],
                       ['File', '/.fsck']]]]

        self.assertListEqual(
            baculaParser('recursive_section.conf').asList(),
            check_list
        )

    def test_include_config(self):
        check_list = [['FileSet',
                       ['Name', 'importantly'],
                       ['Include',
                        ['Options', ['signature', 'MD5']],
                        ['File', '/etc'],
                        ['File', '/opt'],
                        ['File', '/var/www'],
                        ['File', '/root'],
                        ['File', '/home'],
                        ['File', '/usr/local'],
                        ['File', '/tmp/Package.list'],
                        ['Exclude Dir Containing', '.excludeme']]],
                      ['Client',
                       ['Name', 'client1-fd'],
                       ['Address', '127.0.0.1'],
                       ['FDPort', '9102'],
                       ['Catalog', 'MyCatalog'],
                       ['Password', 'verySecurePass'],
                       ['File Retention', '60 days'],
                       ['Job Retention', '6 months'],
                       ['AutoPrune', 'yes']],
                      ['Job',
                       ['Name', 'client1-files'],
                       ['Client', 'client1-fd'],
                       ['JobDefs', 'backup_importantly']]]

        self.assertListEqual(
            baculaParser('include_config.conf').asList(),
            check_list
        )

    @expectedFailure
    def test_pipe_include(self):
        check_list = []
        self.assertListEqual(
            baculaParser('pipe_include.conf').asList(),
            check_list
        )

    def test_oneline_syntax(self):
        check_list = [['Include',
                       ['Options', ['signature', 'MD5'], ['sparse', 'yes']],
                       ['File', '/dev/hd6']]]

        self.assertListEqual(
            baculaParser('oneline_syntax.conf').asList(),
            check_list
        )


if __name__ == "__main__":
    unittest.main()
