import abc
import re
import socket
from tornado import escape
all_tags = re.compile(r'((?:{{\s*[^{]+\s*}})|(?:{%\s*[^{%]+\s*%}))')
expr_tags = re.compile(r'\s*([^{]+?)\s*}}')
unary_tags = re.compile(r"^\s*(safe|include|if|for|end|else|elif)\s+(.+?)?\s*%}")

def render(path, scope, response=None):
	if 'response' not in scope:
		scope['response'] = response
	if 'base_url' not in scope:
		scope['base_url'] = socket.gethostbyname(socket.gethostname())
	with open(path) as f:
		tokens = all_tags.split(f.read())
		_current_nodes = [GroupNode()]
		for token in tokens:
			if token[:2] == "{{":
				groups = expr_tags.match(token[2:])
				_current_nodes[-1].add_child(ExpressionNode(groups.group(1)))
			elif token[:2] == "{%":
				groups = unary_tags.match(token[2:])
				if groups.group(1) == "include":
					_current_nodes[-1].add_child(IncludeNode(groups.group(2)))
				elif groups.group(1) == "safe":
					_current_nodes[-1].add_child(SafeNode(groups.group(2)))
				elif groups.group(1) == "if":
					if_node = IfNode(groups.group(2))
					_current_nodes[-1].add_child(if_node)
					_current_nodes.append(if_node)
				elif groups.group(1) == "else":
					_current_nodes[-1].else_child()
				elif groups.group(1) == "elif":
					_current_nodes[-1].elif_child(groups.group(2))
				elif groups.group(1) == "for":
					for_node = ForNode(groups.group(2))
					_current_nodes[-1].add_child(for_node)
					_current_nodes.append(for_node)
				elif groups.group(1) == "end":
					if len(_current_nodes) > 0:
						_current_nodes.pop()
					else:
						raise SyntaxError("Too many end tags")
			else:
				if len(token) > 0:
					_current_nodes[-1].add_child(TextNode(token))
	if len(_current_nodes) < 2:
		return _current_nodes[0].eval(scope)
	else:
		raise SyntaxError("Unclosed for or if loop")

class Node(metaclass=abc.ABCMeta):
	def __init__(self, token=None):
		self._token = token

	@abc.abstractmethod
	def eval(self, scope):
		return ""
	
class GroupNode(Node):
	def __init__(self):
		super().__init__()
		self._children = []

	def add_child(self,child):
		self._children.append(child)

	def eval(self, scope):
		text = ""
		for child in self._children:
			text += child.eval(scope)
		return text

class ForNode(GroupNode):
	def __init__(self, statement):
		super().__init__()
		self._statement = statement

	def eval(self, scope):
		text = ""
		args = self._statement.split(' ')
		for x in eval(args[2], {}, scope):
			scope[args[0]] = x
			for child in self._children:
				text += child.eval(scope)
		return text
	
	
class IfNode(GroupNode):
	def __init__(self, statement):
		super().__init__()
		self._children = [[]]
		self._statements = [statement]

	def add_child(self,child):
		self._children[-1].append(child)

	def else_child(self):
		self._children.append([])

	def elif_child(self, statement):
		self._statements.append(statement)
		self._children.append([])
		
	def eval(self, scope):
		text = ""
		run_else = True
		for statement in enumerate(self._statements):
			if eval(statement[1], {}, scope):
				run_else = False
				for child in self._children[statement[0]]:
					text += child.eval(scope)
		if len(self._children) != len(self._statements) and run_else:
			for child in self._children[-1]:
				text += child.eval(scope)
		return text

class ExpressionNode(Node):
	def eval(self, scope):
		try:
			replacement = str(eval(self._token, {}, scope))
		except NameError:
			replacement = ""
		return escape.xhtml_escape(replacement)
		
class TextNode(Node):
	def eval(self, scope):
		return self._token

class IncludeNode(Node):
	def eval(self, scope):
		return render(self._token, scope)

class SafeNode(Node):
	def eval(self, scope):
		try:
			replacement = str(eval(self._token, {}, scope))
		except NameError:
			replacement = ""
		return replacement
