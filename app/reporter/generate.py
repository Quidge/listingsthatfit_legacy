import logging
from sqlalchemy.orm.exc import NoResultFound
from app.reporter import reporter_jinja_env as jinja_env
from app.models import Item
from app.reporter.utils import compile_item_with_measurements as compress

logger = logging.getLogger(__name__)


def output_forum_post(list_of_items, metadata=None):
	template = jinja_env.get_template('styleforum/basic_multi_item.txt')
	print(template.render(items=list_of_items, metadata=metadata))


def single_item_measurements_report(ebay_item_id):
	try:
		i = Item.query.filter(Item.ebay_item_id == ebay_item_id).one()
	except NoResultFound:
		raise NoResultFound((
			'Could not find an Item instance with ebay ID <{}> in the database.').format(
			ebay_item_id))
	template = jinja_env.get_template('styleforum/single_item_forum_post.txt')
	return template.render(item=i, measurements=i.measurements)


def generate_forum_post_w_msmts(
	list_of_items,
	template='/styleforum/multi_item_w_msmts.txt',
	metadata=None):
	"""Takes list of rows with (<Item>, <ItemMeasurement>) instances, compresses it to
	a dict of {item : {various: msmt, various2: msmt}}, and renders as text appropriate
	for a Styleforum post.

	Parameters
	----------
	list_of_items : list
		list of tuples in form (and order): (<Item instance>, <ItemMeasurement instance>)
	metadata : dict
		in form {
			'total_search_count': Item.query.count(),
			'result_count': len(compressed),
			'measurements_provided': measurement dict
		}

	Returns
	-------
	rendered template

	"""
	items_dict = compress(list_of_items)
	template = jinja_env.get_template(template)

	logger.debug('Rendering jinja template using template={}'.format(template))
	return template.render(items=items_dict, metadata=metadata)
