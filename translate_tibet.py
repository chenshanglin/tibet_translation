import logging
import os
import requests
import sys
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

def init_log():
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  handler = logging.StreamHandler(sys.stdout)
  handler.setFormatter = logging.Formatter('%(name)s %(message)s')
  logger.addHandler(handler)

def gen_tibet_postdata(key):
  return ("src=" + key + "&lang=ct").encode('utf-8')

def translate_tibet(key):
  host = "http://mt.utibet.edu.cn/mt"
  data = gen_tibet_postdata(key)

  logging.debug('Chinese to Tibet post data: '.encode('utf-8') + data)

  response = requests.post(host, data=data)
  soup = BeautifulSoup(response.text, "html5lib")
  rst_dom = soup.find(name="textarea", attrs={"id":"txt2", "name" : "tgt"})

  logging.debug(rst_dom)

  return rst_dom.get_text()

def translate_xml_node(node, translate_func):
    if node is None:
      return

    logging.debug(ET.tostring(node, encoding='utf-8').decode('utf-8'))

    if node.text and len(node.text) > 0:
      logging.debug("text: " + node.text)
      try:
        tr = translate_func(node.text)
        node.text = tr
      except:
        logging.error("translate failed: " + node.text)

    if node.tail and len(node.tail) > 0:
      logging.debug("tail: " + node.tail)
      try:
        tr = translate_func(node.tail)
        node.tail = tr
      except:
        logging.error("translate failed: " + node.tail)

    for sub_node in node:
      translate_xml_node(sub_node, translate_func)

def translate_xml(xml_text, tag, translate_func):
  root = ET.fromstring(xml_text)

  for elem in root.iter(tag=tag):
    translate_xml_node(elem, translate_func)

  return root

def translate_xml_file(in_file, tag, translate_func, out_file = None):
  tree = ET.ElementTree(file=in_file)

  for elem in tree.iter(tag=tag):
    translate_xml_node(elem, translate_func)

  tree.write(out_file, xml_declaration=True, encoding='utf-8')

#init_log()
logging.basicConfig(level=logging.ERROR)

# Examples
# translate simple words
# print(translate_tibet("机器人"))

# translate android strings.xml
in_file = os.path.join(os.path.expanduser('~'), 'Downloads/strings.xml')
out_file = os.path.join(os.path.expanduser('~'), 'Downloads/strings_tibet.xml')
translate_xml_file(in_file, 'string', translate_tibet, out_file)
