# encoding=utf8
'''
Created on 2016-08-18

@author: jingyang <jingyang@nexa-corp.com>

Usage:
    fab staging deploy
    fab prod deploy
'''
from fabric.api import local
from fabric.context_managers import lcd, cd
from fabric.operations import put, run
from fabric.state import env


PROJECT_NAME = "liucheng"
PROJECT_DIR = "/pypro/liucheng/"  # project dir on server


def staging():
    env.user = "coblan"
    env.hosts = ["10.0.2.250"]


def prod():
    env.user = "coblan"
    env.hosts = ["enjoyst.com"]


def archive():
    with lcd(".."):
        local("git archive -o deploy/{}.tar.gz HEAD".format(PROJECT_NAME))


def upload():
    with cd(PROJECT_DIR):
        put("{}.tar.gz".format(PROJECT_NAME), ".")


def extract():
    with cd(PROJECT_DIR):
        run("tar xf {}.tar.gz".format(PROJECT_NAME))


def deploy():
    archive()
    upload()
    extract()
