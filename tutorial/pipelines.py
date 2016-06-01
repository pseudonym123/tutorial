# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lxml import etree

class TutorialPipeline(object):
    def __init__(self):
        self.outFile = open('items_xml.html', 'wb')
        self.page = etree.Element(u'html')
        self.xmldoc = etree.ElementTree(self.page)
        etree.SubElement(self.page, u'head')
        self.bodyElt = etree.SubElement(self.page, u'body')
        self.all_contents = {}


    def close_spider(self, spider):
        # self.xmldoc.write(self.outFile)
        # self.outFile.write(etree.tostring(self.xmldoc, encoding="utf-8", xml_declaration=True))
        ff = sorted(self.all_contents)
        ff_size = len(ff)
        start_pos = 0 if (ff_size < 50) else (ff_size - 50)
        for index in ff:
            if index >= start_pos:
                self.outFile.write(self.all_contents[index]['title'] + self.all_contents[index]['contents'])
        print "pipeline write to file"

    def __del__(self):
        print "pipeline exit"

    def process_item(self, item, spider):
        if item is None:
            return None

        title = etree.SubElement(self.bodyElt, u'h1', id=item['id'])
        title.text = item['title']
        contents = etree.SubElement(self.bodyElt, u'div')
        contents.text = item['contents']
        self.all_contents[int(item['id'])] = {'title':item['title'].encode('utf-8'), 'contents':item['contents'].encode('utf-8')}
        return item
