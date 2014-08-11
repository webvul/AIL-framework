#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of AIL framework - Analysis Information Leak framework
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Copyright (c) 2014 Alexandre Dulaunoy - a@foo.be

import ConfigParser
import argparse
import sys

configfile = '../packages/config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(configfile)

# Indexer configuration - index dir and schema setup
indexpath = cfg.get("Indexer", "path")
indexertype = cfg.get("Indexer", "type")

argParser = argparse.ArgumentParser(description='Fulltext search for AIL')
argParser.add_argument('-q', action='append', help='query to lookup (one or more)')
args = argParser.parse_args()

from whoosh import index
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

ix = index.open_dir(indexpath)

from whoosh.qparser import QueryParser
if args.q is None:
    argParser.print_help()
    exit(1)

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(" ".join(args.q))
    results = searcher.search(query, limit=None)
    for x in results:
        print x

