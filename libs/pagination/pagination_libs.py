#coding=utf-8
from math import ceil

class Pagination(object):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.

        #: the current page number (1 indexed)   当前页
        self.page = page
        #: the number of items to be displayed on a page.每页要显示多少条记录。
        self.per_page = per_page
        #: the total number of items matching the query， 符合查询条件的总记录数
        self.total = total
        #: the items for the current page， 当前页的记录
        self.items = items

    @property
    def pages(self):
        """The total number of pages
        计算一共多少页
        """
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages


    @property
    def prev_num(self):
        """Number of the previous page.
        计算上一页
        """
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists
        是否有上一页
        """
        return self.page > 1


    @property
    def has_next(self):
        """True if a next page exists.
        是否有下一页
        """
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page
        计算下一页
        """
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=1, left_current=1,
                   right_current=2, right_edge=1):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:
        一个迭代器，返回页数列表。
            left_edge=2  省略号左边显示2页，
            left_current=2 当前页左边显示2页
            right_current=2 当前页右边显示2页
            right_edge=2 省略号右边显示2页


        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
