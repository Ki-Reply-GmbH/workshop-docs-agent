
from pydantic import BaseModel, Field
import ast
from pathlib import Path
from typing import Iterator, Any, Optional, List, NotRequired, Union
import re

from langchain.prompts import load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv()
import os

def extract_md_blocks(text: str) -> List[str]:
	pattern = r"```(?:\w+\s+)?(.*?)```"
	matches = re.findall(pattern, text, re.DOTALL)
	return [block.strip() for block in matches]


llm = ChatOpenAI(
	model_name="gpt-4o",  # type: ignore
	openai_api_key=os.environ["OPENAI_KEY"],  # type: ignore
	openai_organization="org-Mxa66lw5lFVUrdKlbb4gJYsv",  # type: ignore
	temperature=0.3,
	streaming=True,
	max_retries=10,
	verbose=True)


class GroupDir(BaseModel):
	files: List[str]
	path: str

def list_all_files(path: Path) -> Iterator[GroupDir]:
	ext = ['.py']
	subfolders: List[str] = []
	files: List[str] = []

	path = path.absolute()

	for f in os.scandir(path):
		if f.is_dir():
			subfolders.append(f.path)
		if f.is_file():
			if os.path.splitext(f.name)[1].lower() in ext:
				files.append(f.name)

	if files:
		try:
			idx = files.index('__init__.py')
		except:
			idx = -1

		if idx >= 0:
			files = files[0:idx] + files[idx+1:] + [files[idx]]

		yield GroupDir(files=files, path=str(path.absolute()))

	for dir in subfolders:
		new_path = Path.joinpath(path, dir)

		for r in list_all_files(new_path):
			yield r


def document_files(path: str):

	

	for module in list_all_files(Path(path)):
		treated_files: dict[str, str | None] = {}
	
		for filename in module.files:
			if treated_files.get(filename, None):
				continue
			
			file = Path.joinpath(Path(module.path), filename)

			visited_nodes: set[str] = set()
			visitor:MyNodeVisitor| None = None
			while True:
				file_content: str
				with open(file, 'r', encoding='utf-8') as f:
					file_content = f.read()

				file_content_lines = re.split(r'\r?\n', file_content)
				file_content = '\n'.join(file_content_lines)

				ast_result = ast.parse(file_content)
				visitor = MyNodeVisitor(filecontent=file_content, lines=file_content_lines)
				visitor.visit(ast_result)

				def _pick(elem: Elem | None) -> Elem | None:
					if not elem or elem.get_id() in visited_nodes:
						return None

					if isinstance(elem, Container):
						for subelem in reversed(elem.children):
							res = _pick(subelem)
							if res:
								return res

					return elem

				def _add_doc(doc: str, to_document: Elem):
					blocs = extract_md_blocks(doc)
					if blocs:
						if len(blocs) > 1:
							raise Exception(f'Too many blocs in {doc}')

						doc = blocs[0]

					to_document.doc = doc

					line = to_document.node_line - 1
					col = to_document.node_col - 1

					def _stringify(lines: List[str]) -> str:
						str = ''
						for line in lines:
							str = str + line + '\n'
						return str

					def _ident_docs(doc: str):
						parts = doc.splitlines()
						parts = [p.strip() for p in parts]
						res = ''
						for part in parts:
							if res:
								res += f'\n{file_content_lines[line][:col]}{part}'
							else:
								res = part
						return res

					new_content = _stringify(file_content_lines[0:line]) + file_content_lines[line][:col+1] + \
						f'"""{_ident_docs(doc)}\n{file_content_lines[line][:col]}"""\n' + file_content_lines[line][:col] + file_content_lines[line][col:] + '\n' + _stringify(file_content_lines[line+1:])

					with open(file, 'w', encoding='utf-8') as nf:
						nf.write(new_content)

				to_document = _pick(visitor._module)
				if not to_document:
					break

				visited_nodes.add(to_document.get_id())
				if to_document.doc:
					continue # already documented
				
				print("picked ", to_document.get_id())
				if isinstance(to_document, FunctionElem):
					if isinstance(to_document.parent, ClassElem):

						prompt = load_prompt(path='class_method_prompt.json')
						chain = prompt | llm | StrOutputParser()
						doc = chain.invoke({
							'method': to_document.body,
							'context': file_content,
							'class_name': to_document.parent.name
						})

						_add_doc(doc, to_document)
					else:
						prompt = load_prompt(path='method_prompt.json')
						chain = prompt | llm | StrOutputParser()
						doc = chain.invoke({
							'method': to_document.body,
							'context': file_content
						})

						_add_doc(doc, to_document)
				elif isinstance(to_document, ClassElem):
					if to_document.constructor:
						prompt = load_prompt(path='class_constructor_prompt.json')
						chain = prompt | llm | StrOutputParser()
						doc = chain.invoke({
							'constructor': to_document.constructor.body,
							'class_name': to_document.name,
							'context': file_content
						})

						_add_doc(doc, to_document)
						
					prompt = load_prompt(path='class_prompt.json')
					chain = prompt | llm | StrOutputParser()
					doc = chain.invoke({
						'class_body': to_document.body,
						'context': file_content
					})

					_add_doc(doc, to_document)

				elif to_document is visitor._module and visitor._module:
	
					if filename == '__init__.py':
						all_docs = [f'# {k}\n{v}' for k, v in treated_files.items() if v]
						doc_global = '\n\n'.join(all_docs)
						# document the module (= the sub directory)
					elif len(visitor._module.children) > 1:
						prompt = load_prompt(path='module_prompt.json')
						chain = prompt | llm | StrOutputParser()
						doc = chain.invoke({
							'context': file_content
						})

						_add_doc(doc, to_document)
					pass

			if not visitor or not visitor._module:
				raise Exception()

			doc = visitor._module.children[0].doc if len(visitor._module.children) == 1 else visitor._module.doc
			treated_files[filename] = doc

class Elem(BaseModel):
	name: str
	doc: Optional[str]
	parent: Optional['Container']
	node_line: int
	node_col: int

	def get_id(self) -> str:
		return self.parent.get_id() + '.' + self.name if self.parent else self.name

	@staticmethod
	def get_node(container: 'Elem', id: str) -> Optional['Elem']:
		parts = id.split('.')
		if len(parts) < 2:
			if container.name == id:
				return container
			return None

		if container.name != parts[0]:
			return None

		if isinstance(container, Container):
			for child in container.children:
				res = Elem.get_node(child, '.'.join(parts[1:]))
				if res:
					return res

		return None


class Container(Elem):
	children: List['Elem'] = Field(default_factory=lambda: [])


class ClassElem(Container):
	constructor: Optional['FunctionElem']
	body: str
	functions: List['FunctionElem'] = Field(default_factory=lambda: [])


class FunctionElem(Container):
	body: str
	node_line: int
	node_col: int

class MyNodeVisitor(ast.NodeTransformer):

	def __init__(self, filecontent: str, lines: List[str]):
		self._filecontent = filecontent
		self._module: Optional[Container] = None
		self._current_node = self._module
		self._lines = lines
	
	def visit_Module(self, node: ast.Module):
		if self._module:
			raise Exception()

		self._current_node = self._module = Container(name='module', doc=ast.get_docstring(node), parent=None, node_col=1, node_line=1)
		return ast.NodeVisitor.generic_visit(self, node)
	
	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
		if not self._current_node:
			raise Exception()

		parent = self._current_node
		fct = FunctionElem(
			name=node.name,
			body=ast.unparse(node),
			doc=ast.get_docstring(node),
			parent=self._current_node,
			node_line=node.body[0].lineno,
			node_col=node.body[0].col_offset)

		if isinstance(self._current_node, ClassElem):
			if fct.name == '__init__':
				self._current_node.constructor = fct
			else:
				self._current_node.functions.append(fct)
				self._current_node.children.append(fct)
		else:
			self._current_node.children.append(fct)

		self._current_node = fct
		res = ast.NodeVisitor.generic_visit(self, node)
		self._current_node = parent
		return res

	def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
		if not self._current_node:
			raise Exception()

		parent = self._current_node
		fct = FunctionElem(
			name=node.name,
			body=ast.unparse(node),
			doc=ast.get_docstring(node),
			parent=self._current_node,
			node_line=node.body[0].lineno,
			node_col=node.body[0].col_offset)

		if isinstance(self._current_node, ClassElem):
			if fct.name == '__init__':
				self._current_node.constructor = fct
			else:
				self._current_node.functions.append(fct)
				self._current_node.children.append(fct)
		else:
			self._current_node.children.append(fct)

		self._current_node = fct
		res = ast.NodeVisitor.generic_visit(self, node)
		self._current_node = parent
		return res

	def visit_ClassDef(self, node: ast.ClassDef) -> Any:
		if not self._current_node:
			raise Exception()

		parent = self._current_node
		class_elem = ClassElem(name=node.name, body=ast.unparse(node), parent=parent, doc=None, constructor=None, node_line=node.body[0].lineno, node_col=node.body[0].col_offset)
		self._current_node = class_elem
		parent.children.append(self._current_node)
		res = ast.NodeVisitor.generic_visit(self, node)
		self._current_node = parent

		class_elem.doc = ast.get_docstring(node)
		return res


document_files('./resources')
