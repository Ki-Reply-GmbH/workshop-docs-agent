
import ast
from pathlib import Path
from typing import Iterator, Any, Optional, List, NotRequired
import re

def list_all_files(path: Path) -> Iterator[Path]:
	return path.rglob("*.py")

def document_files(path: str):
        
        treated_files: set[Path] = set()
        
        for file in list_all_files(Path(path)):

            if treated_files in treated_files:
                continue
            
            file_content: str
            with open(file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                
            file_content_lines = re.split(r'\r?\n')
            file_content = '\n'.join(file_content_lines)
            
            ast_result = ast.parse(file_content)
            visitor = MyNodeVisitor(filecontent=file_content, lines=file_content_lines)
            visitor.visit(ast_result)
            # print(visitor._module)
            
            
            
from pydantic import BaseModel, Field

class Elem(BaseModel):
	name: str
	doc: Optional[str]
	parent: Optional['Container']

class Container(Elem):
	children: List['Elem'] = Field(default_factory=lambda: [])
 
 
class ClassElem(Container):
	constructor: Optional['FunctionElem']
	functions: List['FunctionElem']= Field(default_factory=lambda: [])
 
class FunctionElem(Elem):
	body: str
     

class MyNodeVisitor(ast.NodeTransformer):

	
	def __init__(self, filecontent: str, lines:List[str]):
		self._filecontent = filecontent
		self._module = Container(name='module', doc=None, parent=None)
		self._current_node = self._module
		self._lines = lines

	def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
		print(f'function {node.name}')

		fct = FunctionElem(name=node.name, body=ast.unparse(node), doc=None, parent=self._current_node)
		self._current_node.children.append(fct)
		if isinstance(self._current_node, ClassElem):
			if fct.name == '__init__':
				self._current_node.constructor = fct
			else:
				self._current_node.functions.append(fct)
		return ast.NodeVisitor.generic_visit(self, node)


	def visit_ClassDef(self, node: ast.ClassDef) -> Any:
		print(f'class {node.name}')

		parent = self._current_node
		self._current_node = ClassElem(name=node.name, parent=parent, doc=None, constructor=None)
		parent.children.append(self._current_node)
		res = ast.NodeVisitor.generic_visit(self, node)
		self._current_node = parent
		return res



            
            
document_files('./resources')