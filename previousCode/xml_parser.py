import xml.etree.ElementTree as ET
import html2text
from pprint import pprint
import json, os, csv, re

escape_illegal_xml_characters = lambda x: re.sub(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]', '', x)
all_news = []
all_commentary = []
for root, dirs, files in os.walk("."):
    for name in files:
        if '.xml' in name:
            if "News" in root:
                all_news.append(os.path.join(root, name))
            if "Commentary" in root:
                all_commentary.append(os.path.join(root, name))


def commentary_parsing(root):
    count = 0
    while root[0][count].tag != 'item':
        count += 1
    assert root[0][-1].tag == 'item'
    for item in root[0][count:]:
        tags = []
        affiliation = ''
        author = ''
        for child in item:
            if child.tag == 'title':
                title = child.text
            elif child.tag == 'link':
                link = child.text
            elif child.tag == 'pubDate':
                date = child.text
            elif child.tag == 'category':
                if child.text != 'Uncategorized' and 'affiliation' not in child.text.lower() and 'author' not in child.text.lower():
                    tags.append(child.text)
                elif 'affiliation:' in child.text.lower():
                    affiliation = re.sub("affiliation:", "", child.text, flags=re.I)
                elif 'author:' in child.text.lower():
                    author = re.sub("author:", "", child.text, flags=re.I)
        all_tags = ', '.join(tags)
        result = [title,date,all_tags,author,affiliation,link]
        all_commentary_result.append(result)

all_commentary_result = []
for i in all_commentary:
    try:
        root = ET.parse(i).getroot()
        commentary_parsing(root)
    except:
        content = ''
        with open (i,'r+', encoding='utf-8') as fp:
            content = fp.read()
        fp.close()
        parser = ET.XMLParser(encoding="utf-8")
        root = ET.fromstring(escape_illegal_xml_characters(content), parser=parser)
        commentary_parsing(root)
        continue

with open ('all_commentary_summary.csv','w+') as commentary_csv:
    writer = csv.writer(commentary_csv)
    writer.writerow(['Title','Datetime','Tags', 'Author', 'Affiliation','Link'])
    writer.writerows(all_commentary_result)
commentary_csv.close()

# with open ('all_news_summary.csv','w+') as news_csv:
#     writer = csv.writer(news_csv)
#     writer.writerow(['Title','Datetime','Tags','Link'])
#     writer.writerows(all_news_result)
# news_csv.close()



# result_dict = {}
# for child in root[0][12:]:
#     date = child[2].text[5:11]
#     title = child[0].text.strip('\n').strip('\t').strip('\n')
#     content = h.handle(child[6].text).replace('\n','')
#     if date not in result_dict:
#         result_dict[date] = {}
#     result_dict[date][title] = content

# with open('this_day_final.json', 'w') as fp:
#     json.dump(result_dict, fp, indent=2)
