# 藏文翻译
将简体中文翻译成，使用西藏大学提供的翻译支持：[阳光臧汉双向翻译](http://mt.utibet.edu.cn/mt) 
支持翻译单个词，或者 Android strings.xml 资源文件

# 使用方法
**简单的关键词翻译
```python
translate_tibet("机器人")
```
**翻译 Android strings.xml 资源文件，其中第二个参数 'string' 表示要翻译的 xml tag name
```python
in_file = os.path.join(os.path.expanduser('~'), 'Downloads/strings.xml')
out_file = os.path.join(os.path.expanduser('~'), 'Downloads/strings_tibet.xml')
translate_xml_file(in_file, 'string', translate_tibet, out_file)
```
# 依赖环境
- python3
- requests
- BeautifulSoup
- xml.etree.cElementTree
