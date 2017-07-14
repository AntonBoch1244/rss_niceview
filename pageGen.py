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

cards = file("templates/_TPL_Cards.html", "r", -1)
mainPage = file("templates/_TPL_Main.html", "r", -1)
styleSheet = file("templates/assets/_TPL_NewsStyle.css", "r", -1)

# TODO: MAKE DOWNLOAD IT FROM AF=INET|I6NET
input_data = file("DataIn/lenta.rss", "r", -1) # for now generating from local file

# TODO: USER GETTING INFORMATION FROM LOCAL WEBSERVER
result = file("lenta.rss.html", "w") # for now generating to local file [With same contents as input]

import re

# FOR TODOs R#25 and R#28
# import urllib2
# import BaseHTTPServer

XML_DATA = input_data.readline()
XML_ENCODING = re.findall(r".*?encoding=\"(?P<encode>.*?)\".*", XML_DATA)[0]

input_data.seek(0)
RSS_DATA = input_data.read()


def CDATAUnpack(some_data):
	return re.findall(r"<!\[CDATA\[(?P<CDATA>.*?)\]\]>", some_data, re.DOTALL)[0]


def normalized(data):
	normalize = data
	for nop in range(0, 255, 1): normalize = re.sub("&lt;", "<", normalize, re.DOTALL)
	for nop in range(0, 255, 1): normalize = re.sub("&gt;", ">", normalize, re.DOTALL)
	for nop in range(0, 255, 1): normalize = re.sub("&#39;", "'", normalize, re.DOTALL)
	for nop in range(0, 255, 1): normalize = re.sub("&nbsp;", "", normalize, re.DOTALL)
	for nop in range(0, 255, 1): normalize = re.sub("&quot;", "\"", normalize, re.DOTALL)
	for nop in range(0, 255, 1): normalize = re.sub("&amp;", "&", normalize, re.DOTALL)
	return normalize


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
_title = re.findall(r".*?<title>(?P<title>.*?)</title>(?P<aftT>.*?)", ch, re.DOTALL)[0][0]
RSS_title = _title

if RSS:
	_items = re.findall(r"<item>(?P<title>.*?)</item>", ch, re.DOTALL)
	_Entrys = None
if ATOM:
	_items = None
	_Entrys = re.findall(r"<entry>(?P<title>.*?)</entry>", ch, re.DOTALL)

try:
	if _items is None and _Entrys is not None: raise Exception("RSS IS WRONG!")
	newscards = ""
	for item in _items:
		rss_title = re.findall(r".*<title>(?P<this>.*?)</title>.*", item, re.DOTALL)[0]
		try:
			ttl = CDATAUnpack(rss_title)
		except:
			ttl = rss_title
		rss_title = normalized(ttl)
		rss_link = normalized(re.findall(r".*<link>(?P<this>.*?)</link>.*", item, re.DOTALL)[0])
		rss_description = re.findall(r".*<description>(?P<this>.*?)</description>.*", item, re.DOTALL)[0]
		try:
			rss_description = normalized(CDATAUnpack(rss_description))
		except:
			rss_description = normalized(rss_description)
		try:
			rss_enclosure_url = re.findall(r"<enclosure url=\"(?P<url>.*?)\" .*?/>", item, re.DOTALL)[0]
			rss_enclosure_data = rss_enclosure_url
		except:
			rss_enclosure_url = "#"
			rss_enclosure_data = "Not available."
			pass
		cards.seek(0)
		newscards += cards.read()\
			.format(
			rss_link = rss_link,
			ttl = rss_title,
			rss_description = rss_description,
			rss_enclosure_url = rss_enclosure_url,
			rss_enclosure_data = rss_enclosure_data)
except:
	if RSS:
		print("No Items")
	pass

try:
	if _Entrys is None and _items is not None: raise Exception("ATOM IS WRONG!")
	newscards = ""
	for entry in _Entrys:
		ATOM_title = re.findall(r".*<title>(?P<this>.*?)</title>.*", entry, re.DOTALL)
		try:
			ttl = CDATAUnpack(ATOM_title[0])
		except:
			ttl = ATOM_title[0]
		ATOM_title = normalized(ttl)
		ATOM_link = normalized(re.findall(r".*<link .*? href=\"(?P<this>.*?)\".*/>.*", entry, re.DOTALL)[0])
		ATOM_description = re.findall(r".*<summary.*?>(?P<this>.*?)</summary>.*",
		                              entry,
		                              re.DOTALL)[0]
		try:
			ATOM_description = normalized(CDATAUnpack(ATOM_description))
		except:
			ATOM_description = normalized(ATOM_description)
		try:
			ATOM_image_url = re.findall(r"<image>(?P<url>.*?)</image>", entry, re.DOTALL)[0]
			ATOM_image = ATOM_image_url
		except:
			ATOM_image_url = ""
			ATOM_image = "Not available."
			pass
		cards.seek(0)
		newscards += cards.read()\
			.format(
			rss_link = ATOM_link,
			ttl = ATOM_title,
			rss_description = ATOM_description,
			rss_enclosure_url = ATOM_image_url,
			rss_enclosure_data = ATOM_image)
except:
	if ATOM:
		print("No Entrys")
	pass

resgener = mainPage.read()\
	.format(
	title = RSS_title,
	styleSheet = styleSheet.read(),
	XML_ENCODING = XML_ENCODING,
	newscards = newscards)

styleSheet.close()
cards.close()
mainPage.close()
result.write(resgener)
result.close()
