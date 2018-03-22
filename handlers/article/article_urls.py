from article_handler import (
    ArticleListHandler,
    AddArticleHandler,
    AddCategoryTagHandler,
    DelCategoryTagHandler,
    ArticleContentHandler,
    AddCommentHandler,
    AddSecondCommentHandler,
    AddLikeHandler,
    SearchByCategoryTagHandler,
    ArticleModifyListHandler,
    ArticleModifyHandler,
    ArticleDeleteHandler,
)

article_urls = [
    (r'/article/article_list', ArticleListHandler),
    (r'/article/add_article', AddArticleHandler),
    (r'/article/add_category_tag', AddCategoryTagHandler),
    (r'/article/del_category_tag', DelCategoryTagHandler),
    (r'/article/article', ArticleContentHandler),
    (r'/article/addcomment', AddCommentHandler),
    (r'/article/addsecondcomment', AddSecondCommentHandler),
    (r'/article/addlike', AddLikeHandler),
    (r'/article/search', SearchByCategoryTagHandler),
    (r'/article/article_modify_manage', ArticleModifyListHandler),
    (r'/article/article_modify', ArticleModifyHandler),
    (r'/article/article_delete', ArticleDeleteHandler),
]