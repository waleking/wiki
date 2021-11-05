SELECT category.cat_title, page.page_title
from categorylinks join page on page.page_id = categorylinks.cl_from join category on categorylinks.cl_to = category.cat_title
where categorylinks.cl_type = 'subcat';
