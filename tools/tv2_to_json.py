import sys
from pathlib import Path

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.classifiers.semantic_search import SemanticSearch

classifer = SemanticSearch()

classifer.convert_model_to_json(7)
classifer.compress_model(7)

