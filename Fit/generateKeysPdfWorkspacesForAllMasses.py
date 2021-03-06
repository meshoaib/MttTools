#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import division
import os, math, subprocess, shutil, sys, tempfile

if sys.version_info<(2,6,0):
  sys.stderr.write("You need python 2.6 or later to run this script\n")
  sys.exit(1)

import optparse

parser = OptionParser()
parser.add_option("", "--b-tag", dest="btag", type = int)
parser.add_option("-i", "--input", dest="i", type = str)
parser.add_option("-s", "--signal", dest="signal", type = str)

(args, pos) = parser.parse_args()

tmpfile = tempfile.NamedTemporaryFile(dir = '/scratch/', delete = True)

for m in range(500, 2001, 250):
  if m == 1750:
    continue
  tmpfile.write("./generateKeysPdfWorkspaces -m %d --b-tag %d -i %s --signal %s\n" % (m, args.btag, args.i, args.signal % m))

tmpfile.flush()

args = ["parallel", "-u", "-a", tmpfile.name, "-j", "6"] 
subprocess.call(args)

tmpfile.close()
