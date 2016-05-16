#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import app

if __name__ == "__main__":
    app.run()
