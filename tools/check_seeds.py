import sys
from pathlib import Path
project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))
from helpers import settings

for domain_set_name, domain_set in settings.DOMAINS_SETS.items():
    for domain_name, domain_definition in domain_set.items():
        for domain_name2, domain_definition2 in domain_set.items():
            if domain_name == domain_name2: break
            overlap = set(domain_definition['name_modern']) & set(domain_definition2['name_modern'])
            if overlap:
                print(f'In "{domain_set_name}" domains "{domain_name}" and "{domain_name2}" share the following seed words {overlap}')
