import xml.etree.ElementTree as ET
import html2text,re,csv

content = ''
with open ('./JURIST_Commentary_2000_2020/2015.xml','r+', encoding='utf-8') as fp:
    content = fp.read()
fp.close()

all_commentary_result = []
escape_illegal_xml_characters = lambda x: re.sub(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]', '', x)
parser = ET.XMLParser(encoding="utf-8")
root = ET.fromstring(escape_illegal_xml_characters(content), parser=parser)
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

with open ('2015_commentary_summary.csv','w+') as commentary_csv:
    writer = csv.writer(commentary_csv)
    writer.writerow(['Title','Datetime','Tags', 'Author', 'Affiliation','Link'])
    writer.writerows(all_commentary_result)
commentary_csv.close()