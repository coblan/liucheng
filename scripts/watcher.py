#!python2
# -*- encoding:utf8 -*-
import sys
import signal
import sip
sip.setapi('QString', 2)
from PyQt4.QtCore import QFileSystemWatcher,QCoreApplication
import os.path
import shutil
from datetime import datetime



target=[(r'D:\coblan\webcode\build\fields.pack.js','../src/static/js/fields.pack.js'),
        (r'D:\coblan\webcode\build\table.pack.js','../src/static/js/table.pack.js'),
        (r'D:\coblan\webcode\build\table_mb.pack.js','../src/static/js/table_mb.pack.js'),
        (r'D:\coblan\webcode\build\uis.pack.js','../src/static/js/uis.pack.js'),
        (r'D:\coblan\webcode\build\uis_mb.pack.js','../src/static/js/uis_mb.pack.js'),
        (r'D:\coblan\webcode\build\fields_mb.pack.js','../src/static/js/fields_mb.pack.js'),
        (r'D:\coblan\webcode\build\ex_inputs.pack.js','../src/static/js/ex_inputs.pack.js'),
        (r'D:\coblan\webcode\js\exfun.js','../src/static/js/exfun.js'),
        (r'D:\coblan\webcode\js\i18n.js','../src/static/js/i18n.js'),]

files = {}
for src ,dst in target:
    norm_src = os.path.normpath(src)
    files[norm_src] = dst


class MyWatch(QFileSystemWatcher):
    def __init__(self, parent=None):
        super(MyWatch,self).__init__(parent)
        for src,dst in files.items():
            self.addPath(src)
            print('init copy file {src} to {dst}'.format(src=src,dst=dst))
            shutil.copy2(src, dst)
        self.fileChanged.connect(self.on_file_changed)

    def on_file_changed(self,f):
        print('[{time}] file changed :{file}'.format(file=f,time=datetime.now()))
        dst = files.get(f)
        if dst:
            shutil.copy2(f, dst)
            print('copy file {src} to {dst}'.format(src=f,dst=dst))


if __name__=='__main__':
    app=QCoreApplication(sys.argv)
    wat=MyWatch()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
