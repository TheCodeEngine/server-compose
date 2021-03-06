import click
from prettytable import PrettyTable


class Table(object):
	def __init__(self):
		super(Table, self).__init__()

	def listEqual(self, list):
		return True if all(x == list[0] for x in list) else False

	def tableArray(self, x, y, fx, fy):
		return [fy(y)+[fx(z,y) for z in x] for y in y]

	def renderTable(self, x, y,fx=None, fy=None, fi=None):
		fx = (lambda x,y: x) if fx is None else fx
		fy = (lambda y: [y]) if fy is None else fy
		lt = self.tableArray(x, y, fx, fy)
		lf, lr = lt[0], lt[1:]

		table = PrettyTable(lf)

		fi = (lambda l: table.add_row(l)) if fi is None else fi
		map(fi, lr)

		return table


class ClusterTable(Table):
	def __init__(self, cluster):
		super(ClusterTable, self).__init__()
		self.cluster = cluster

	def render(self, x=None, y=None):
		x = self.cluster.nodes if x is None else x
		y = self.cluster.wsrep_vars_values() if y is None else y
		table = self.__rendertable(x, y)
		return table

	def __rendertable(self, nodes, wsrep_vars):
		fx = (lambda x,y: x.getvar(y) if (y is not 'var') else x.getName())
		fy=(lambda x: [x])
		table = self.renderTable(nodes, wsrep_vars, fx=fx, fy=fy)
		table.align["var"] = "l"

		return table
