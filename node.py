#nodetype: tag, attr, text
class Node:
	def __init__(self):
		self.children = []
		self.depth = 0

class ElementNode(Node):
	def __init__(self, tag):
		super().__init__()
		
		self.tag = tag
		self.attrs = {}

		if tag in [ "area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr" ]:
			self.isSingleton = True
		else:
			self.isSingleton = False

		if not self.isSingleton:
			self.text = ""
			self.textIndex = -1

	def createChild(self, childTag):
		child = ElementNode(childTag)
		child.parent = self
		child.depth = self.depth + 1
		self.children.append(child)

		return child

	def createAttr(self, attr, val):
		self.attrs[attr] = val

	def writeText(self, txt):
		if self.isSingleton:
			return
		else:
			self.text = txt
			child = TextNode(txt)
			child.parent = self
			child.depth = self.depth + 1

			if self.textIndex < 0:
				self.textIndex = len(self.children)
			self.children.append(child)

			return child

	def html(self):
		text = ("  " * self.depth) + "<{}".format(self.tag)
		
		for attr, val in self.attrs.items():
			if val is None:
				text += ' {}'.format(attr)
			else:
				text += ' {}="{}"'.format(attr, val)
		
		text += ">\n"
		
		if len(self.children) > 0:
			for child in self.children:
				text += child.html()
		
		if not self.isSingleton:
			text += ("  " * self.depth) + "</{}>\n".format(self.tag)
		
		return text

class AttrNode(Node):
	def __init__(self):
		pass

class TextNode(Node):
	def __init__(self, text):
		super().__init__()
		self.text = text

	def html(self):
		return ("  " * self.depth) + self.text + "\n"
