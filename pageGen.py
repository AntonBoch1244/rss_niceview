#!/usr/bin/env python2
# -+- coding: utf-8 -+-

# pageGen.py
#
# Copyright (C) 2017 Anton Bochkarev Alekseevich <AntonBoch12.44@gmail.com>
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Generation Templates for now useless SHOWED STRUCT OF PAGE [WIP!] TODO: MAKE NOT USELESS
cards = file("templates/_TPL_Cards.html", "r", -1)
mainPage = file("templates/_TPL_Main.html", "r", -1)
# TODO: MAKE DOWNLOAD IT FROM AF=INET|I6NET
input_data = file("DataIn/lenta.rss", "r", -1) # for now generating from local file [For now from Lenta.RU site]
# TODO: USER GETTING INFORMATION FROM LOCAL WEBSERVER
result = file("lenta.rss.html", "w") # for now generating to local file [With same contents as input]

import re
# FOR TODOs R#24 and R#26
import urllib2
import BaseHTTPServer

XML_DATA = input_data.readline()
XML_ENCODING = re.findall(r".*?encoding=\"(?P<encode>.*?)\".*", XML_DATA)[0]

RSS_DATA = input_data.read()
ch = re.findall(r".*?<channel>(?P<channel>.*?)</channel>.*", RSS_DATA, re.DOTALL)[0]
_title = re.findall(r".*?<title>(?P<title>.*?)</title>(?P<aftT>.*?)", ch, re.DOTALL)
RSS_title = _title[0][0]
resgener = "<!DOCTYPE html><html><head><title>" + RSS_title + "</title><style>body { margin: 0; background: #AAA; } .news_card { margin: 50px 25px; border: 1px; border-radius: 3px; border-style: solid; border-color: rgba(127, 127, 127, 0.75); background-color: #dfdfdf; box-shadow: 0px 0px 20px 10px rgba(128, 128, 128, 40); } .news-headline { font-family: monospace; font-size: 2.5em; padding-left: 20px; width: 80%; } .news-textline { font-family: monospace;font-size: 1.5em; padding-left: 20px; width: 80%; } img { margin-right: 60px; width: 100%; }</style><meta charset=\"" + XML_ENCODING + "\"/></head><body>"
_items = re.findall(r"<item>(?P<title>.*?)</item>", ch, re.DOTALL)
for item in _items:
	rss_title = re.findall(r".*<title>(?P<this>.*?)</title>(?P<secondLy>.*)", item, re.DOTALL)
	rss_link = re.findall(r".*<link>(?P<this>.*?)</link>(?P<secondLy>.*)", rss_title[0][1], re.DOTALL)
	resgener += "<div class=\"news_card\"><table><tr><td><table><tr><td class=\"news-headline\"><a href=\"" + rss_link[0][0] + "\">" + rss_title[0][0] + "</a></td></tr><tr><td class=\"news-textline\">"
	rss_description = re.findall(r".*<description>(?P<this>.*?)</description>(?P<secondLy>.*)", rss_link[0][1], re.DOTALL)
	normalize = re.findall(r"<!\[CDATA\[(?P<CDATA>.*?)\]\]>", rss_description[0][0], re.DOTALL)[0]
	resgener += normalize + "</td></tr></table></td>"
	try:
		rss_enclosure_url = re.findall(r"<enclosure url=\"(?P<url>.*?) .*?/>", rss_description[0][1], re.DOTALL)
		resgener += "<td><img src=\"" + rss_enclosure_url[0] + "/></td>"
	except:
		
		pass
	resgener += "</tr></table></div>"
resgener += "</body></html>"

result.write(resgener)
result.close()
