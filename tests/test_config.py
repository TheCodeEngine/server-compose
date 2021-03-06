from pkg.config import Config
import os
import sys

def test_init():
    c = Config(files=('/etc/mysql/debian123.cnf', '/etc/mysql/my123.cnf'))
    assert c is not None

def test_load():
    test_file_1 =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files/debian.cfg")
    c = Config(files=(test_file_1, '/etc/mysql/my123.cnf'))
    cfgs = c.load()
    assert test_file_1 is not None
    assert cfgs is not None


def test_load_empty_list():
    c = Config(files=('/etc/mysql/my123.cnf',))
    cfgs = c.load()
    assert len(cfgs) is 0


def test_search_var():
    test_file_1 =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files/debian.cfg")
    test_file_2 =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files/debian2.cfg")
    c = Config(files=(test_file_1, '/etc/mysql/my123.cnf', test_file_2))
    cfgs = c.load()

    var = c.search('client', 'password')
    assert var == ['meinpassword', 'meinpassword']

    var = c.search_first('client', 'password')
    assert var == 'meinpassword'

    var = c.search('client', 'ttet')
    assert var == [None, None]
