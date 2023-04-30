import re
import xml.etree.ElementTree as ET

from . import settings
from pathlib import Path

TEI_NAMESPACE = '{http://www.tei-c.org/ns/1.0}'


class Corpus:
    """
    Encapsulate the complete set of article files.

    Each entry has an id, which correspond the relative path to its xml.
    """

    def __init__(self):
        self.path = settings.CORPUS_PATH

    def read_ids(self):
        # [...]/kp-editions/eb07/XML/a2/kp-eb0702-000101-9822-v1.xml
        path = Path(self.path)
        ret = [
            str(Path(p).relative_to(path))
            for p in path.glob('**/*.xml')
        ]
        return ret

    def decode_id(self, aid):
        # eb07/TXT/a3/kp-eb0703-024907-8798-v1.txt
        ret = re.search(r'kp-eb(?P<edition>\d\d)(?P<volume>\d\d)-(?P<page>\d\d\d\d)\d\d-', aid)
        ret = {
            k: int(re.sub(f'^0+', f'', v))
            for k, v in ret.groupdict().items()
        }
        return ret

    def read_metadata(self, aid):
        xml = Path(self.path, aid).read_text()
        root = ET.fromstring(xml)
        ret = {
            'title': self.clean_title(root.findall(f'.//{TEI_NAMESPACE}title[@level="a"]')[0].text),
            'terms': self.get_terms_from_dom(root)
        }
        return ret

    def read_body_and_metadata(self, aid):
        ret = self.read_metadata(aid)
        ret['body'] = self.read_body(aid)
        ret.update(self.decode_id(aid))
        ret['aid'] = aid
        return ret

    def get_terms_from_dom(self, root):
        # <term ref="fast:1205830">Ethiopia</term>
        ret = [
            {
                'label': term.text,
                'ref': term.attrib['ref']
            }
            for term in root.findall(f'.//{TEI_NAMESPACE}term[@ref]')
        ]

        return ret

    def clean_title(self, title):
        ret = title
        ret = re.sub(r'(?s)\([^)]*\)', r'', ret)
        ret = ret.strip()
        return ret

    def read_body(self, aid):
        ret = ''
        path = str(aid).replace('XML', 'TXT').replace('.xml', '.txt')
        path = Path(self.path, path)
        if path.exists():
            ret = path.read_text()
            # remove the header
            ret = re.sub(r'(?s)^.*===\+\s*', r'', ret)

        return ret
