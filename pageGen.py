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

input_data.seek(0)
RSS_DATA = input_data.read()


def CDATAUnpack(some_data):
	return re.findall(r"<!\[CDATA\[(?P<CDATA>.*?)\]\]>", some_data, re.DOTALL)[0]

try:
	ch = re.findall(r".*?<channel.*?>(?P<channel>.*?)</channel>.*", RSS_DATA, re.DOTALL)[0]
	print("RSS Detected!")
	RSS = True
	ATOM = False
except IndexError:
	ch = re.findall(r".*?<feed.*?>(?P<channel>.*?)</feed>.*", RSS_DATA, re.DOTALL)[0]
	print("ATOM Detected!")
	RSS = False
	ATOM = True
_title = re.findall(r".*?<title>(?P<title>.*?)</title>(?P<aftT>.*?)", ch, re.DOTALL)
RSS_title = _title[0][0]
resgener = "<!DOCTYPE html>"\
           "<html>"\
           "<head>"\
           "<title>" + RSS_title + "</title>"\
                                   "<style>"\
                                   "body { "\
                                   "margin: 0; "\
                                   "background: #AAAAAA; "\
                                   "} "\
                                   ".news_card { "\
                                   "margin: 50px 25px; "\
                                   "border: 1px; "\
                                   "border-radius: 3px; "\
                                   "border-style: solid; "\
                                   "border-color: rgba(127, 127, 127, 0.75); "\
                                   "background-color: #dfdfdf; "\
                                   "box-shadow: 0px 0px 20px 10px rgba(128, 128, 128, 40); "\
                                   "} "\
                                   ".news-headline { "\
                                   "font-family: serif; "\
                                   "font-size: 2em; "\
                                   "padding-left: 20px; "\
                                   "text-align: justify;"\
                                   "} "\
                                   ".news-textline { "\
                                   "font-family: serif; "\
                                   "font-size: 1.5em; "\
                                   "padding-left: 20px; "\
                                   "text-align: justify;"\
                                   "} "\
                                   "img { "\
                                   "height: calc(100% - 80px); "\
                                   "width: calc(100% - 20px); "\
                                   "box-shadow: 0px 0px 8px 2px rgba(128, 128, 128, 40); "\
                                   "}"\
                                   "</style>"\
                                   "<meta charset=\"" + XML_ENCODING + "\"/>"\
                                                                       "</head>"\
                                                                       "<body>"
if RSS:
	_items = re.findall(r"<item>(?P<title>.*?)</item>", ch, re.DOTALL)
	_Entrys = None
if ATOM:
	_items = None
	_Entrys = re.findall(r"<entry>(?P<title>.*?)</entry>", ch, re.DOTALL)

try:
	for item in _items:
		rss_title = re.findall(r".*<title>(?P<this>.*?)</title>.*", item, re.DOTALL)
		try:
			ttl = CDATAUnpack(rss_title[0])
		except:
			ttl = rss_title[0]
		rss_link = re.findall(r".*<link>(?P<this>.*?)</link>.*", item, re.DOTALL)
		resgener +=\
			"<div class=\"news_card\">"\
			"<table>"\
			"<tr>"\
			"<td>"\
			"<table>"\
			"<tr>"\
			"<td class=\"news-headline\">"\
			"<a href=\"" + rss_link[0] + "\">" + ttl + "</a>"\
			                                           "</td>"\
			                                           "</tr>"\
			                                           "<tr>"\
			                                           "<td class=\"news-textline\">"
		rss_description = re.findall(r".*<description>(?P<this>.*?)</description>.*",
		                             item,
		                             re.DOTALL)
		try:
			normalize = CDATAUnpack(rss_description[0])
		except:
			normalize = rss_description[0]
		for nop in range(0, 255, 1): normalize = re.sub("&lt;", "<", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&gt;", ">", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&#39;", "'", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&nbsp;", "", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&quot;", "\"", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&amp;", "&", normalize, re.DOTALL)
		resgener += normalize + "</td></tr></table></td>"
		try:
			rss_enclosure_url = re.findall(r"<enclosure url=\"(?P<url>.*?)\" .*?/>", item, re.DOTALL)
			resgener += "<td style=\" width:40%; \"><a href=\"" + rss_enclosure_url[0] + "\"><img src=\"" + rss_enclosure_url[0] + "\"/></a></td>"
		except:
			pass
		resgener += "</tr>"\
		            "</table>"\
		            "</div>"
except:
	if RSS:
		print("No Items")
	pass

try:
	for entry in _Entrys:
		ATOM_title = re.findall(r".*<title>(?P<this>.*?)</title>.*", entry, re.DOTALL)
		try:
			ttl = CDATAUnpack(ATOM_title[0])
		except:
			ttl = ATOM_title[0]
		rss_link = re.findall(r".*<link .*? href=\"(?P<this>.*?)\".*/>.*", entry, re.DOTALL)
		resgener +=\
			"<div class=\"news_card\">"\
			"<table>"\
			"<tr>"\
			"<td>"\
			"<table>"\
			"<tr>"\
			"<td class=\"news-headline\">"\
			"<a href=\"" + rss_link[0] + "\">" + ttl + "</a>"\
			                                           "</td>"\
			                                           "</tr>"\
			                                           "<tr>"\
			                                           "<td class=\"news-textline\">"
		rss_description = re.findall(r".*<summary.*?>(?P<this>.*?)</summary>.*",
		                             entry,
		                             re.DOTALL)
		try:
			normalize = CDATAUnpack(rss_description[0])
		except:
			normalize = rss_description[0]
		for nop in range(0, 255, 1): normalize = re.sub("&lt;", "<", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&gt;", ">", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&#39;", "'", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&nbsp;", "", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&quot;", "\"", normalize, re.DOTALL)
		for nop in range(0, 255, 1): normalize = re.sub("&amp;", "&", normalize, re.DOTALL)
		resgener += normalize + "</td></tr></table></td>"
		try:
			rss_enclosure_url = re.findall(r"<image>(?P<url>.*?)</image>", entry, re.DOTALL)
			resgener += "<td style=\" width:40%; \"><img src=\"" + rss_enclosure_url[0] + "\"/></td>"
		except:
			pass
		resgener += "</tr>"\
		            "</table>"\
		            "</div>"
except Exception as x:
	if ATOM:
		print("No Entrys, {}".format(x))
	pass

resgener += "</body>"\
            "</html>"

result.write(resgener)
result.close()
