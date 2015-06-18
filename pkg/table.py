import click
from prettytable import PrettyTable

class Table(object):
	def __init__(self):
		super(Table, self).__init__()

	def listEqual(self, list):
		return True if all(x == list[0] for x in list) else False


class ClusterTable(Table):
	def __init__(self, cluster):
		super(ClusterTable, self).__init__()
		self.cluster = cluster

	def render(self):
		self._render(self.cluster.nodes, self.cluster.wsrep_vars)

	def _render(self, nodes, wsrep_vars):

		table = PrettyTable(['Cluster Intigrity Var'] + nodes + ['Check'])
		table.align['Cluster Intigrity Var'] = "l"

		for status_key, status_value in wsrep_vars.items():
			for key, value in status_value.items():
				attr_list = self.__get_list_with_vars(key, nodes)

				status = self.__statusStringListEqual(attr_list) if status_key == 'cluster-integrity' else ''
				table.add_row([key] + attr_list + [status])
			table.add_row(self.__create_list_with_empty(self.cluster.count() + 2))
		print(table)

	def __statusStringListEqual(self, attr_list):
		ok_style = click.style('OK', fg='green')
		error_style = click.style('Error', bold=True, fg='red')

		return ok_style if self.listEqual(attr_list) else error_style

	def __get_list_with_vars(self, wsrep_var, nodes):
		attr_list = map(lambda x: x.get_var(wsrep_var), nodes)
		return attr_list

	def __create_list_with_empty(self, count):
		l = []
		for i in range(count):
			l.append('')
		return l