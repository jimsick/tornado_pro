# coding:utf8

from libs.db.dbsession import dbSession
from models.article.article_model import (
    Tag,
    Category,
    Comment,
    Article,
    ArticleToTag,
    UserLikeArticle,
    SecondComment,
)
from libs.flash.flash_lib import flash

ct_dict = {
    "category": Category,
    "tag": Tag,
}

def article_list_lib(self):
    """01.文章列表页"""
    articles = dbSession.query(Article).order_by(Article.createtime.desc()).all()
    comments = dbSession.query(Comment).order_by(Comment.createtime.desc()).all()
    tags = Tag.all()
    categorys = Category.all()
    return articles, comments, tags, categorys

def get_tags_categorys_lib(self):
    """02.返回标签和分类"""
    tags = Tag.all()
    categorys = Category.all()
    return tags, categorys


def add_article_lib(self, article_id, title, content, desc, category, thumbnail, tags):
    """03增加文章"""
    print title, content, desc
    if category is None or tags is None:
        return {'status': False, 'msg': '请选择分类和标签'}
    if title is None or content is None or desc is None:
        return {'status': False, 'msg': '请输入文章或内容'}
    if article_id != '':
        article = Article.by_id(article_id)
        article.tags = []
    else:
        article = Article()
    article.content = content
    article.title = title
    article.desc = desc
    article.category_id = category
    for tag in tags:
        tag = Tag.by_id(tag)
        article.tags.append(tag)
    article.user_id = self.current_user.id
    self.db.add(article)
    self.db.commit()
    if article_id is not None:
        return {'status': True, 'msg': '文档修改成功'}
    return {'status': True, 'msg': '文档上传成功'}


def add_category_tag_lib(self, category_name, tag_name):
    """04增加分类或者标签"""
    try:
        """固定调用"""
        # if category_name is not None:
        #     category = Category.by_name(category_name)
        #     if category is None:
        #         return {'status': False, 'msg': '分类已存在'}
        #     else:
        #         category = Category()
        #     category.name = category_name
        #     self.db.add(category)
        #     self.db.commit()
        #     return {'status': True, 'msg': '分类添加成功'}
        # if tag_name is not None:
        #     tag = Tag()
        #     if tag.by_name(category_name):
        #         return {'status': False, 'msg': '标签已存在'}
        #     tag.name = tag_name
        #     self.db.add(tag)
        #     self.db.commit()
        #     return {'status': True, 'msg': '标签添加成功'}
        # return {'status': False, 'msg': '标签或分类添加失败'}
        """动态调用"""
        if category_name is not None:
            modelname = "category"
            value = category_name
            tip = "分类"
        if tag_name is not None:
            modelname = "tag"
            value = tag_name
            tip = "标签"
        model = ct_dict[modelname]()
        if model.by_name(value):
            # flash(self, tip+'已存在', 'error')
            return {'status': False, 'msg': tip+'已存在'}
        model.name = value
        self.db.add(model)
        self.db.commit()
        return {'status': True, 'msg': tip+'添加成功'}
    except Exception as e:
        return {'status': False, 'msg': '标签或分类添加失败'}


def del_category_tag_lib(self, c_uuid, t_uuid):
    """05删除分类或者标签"""
    try:
        if c_uuid is not None:
            category = Category.by_uuid(c_uuid)
            if category is None:
                flash(self, '分类不存在', 'error')
                return {'status': False}
            if category.articles:
                flash(self, '分类下存在文章，清先删除文章再删除此分类', 'error')
                return {'status': False}
            self.db.delete(category)
            self.db.commit()
            flash(self, '分类删除成功', 'success')
            return {'status': True}
        if t_uuid is not None:
            tag = Tag.by_uuid(t_uuid)
            if tag:
                flash(self, '标签不存在', 'error')
            self.db.delete(tag)
            self.db.commit()
            flash(self, '标签删除成功', 'success')
            return {'status': True}
        flash(self, '标签或分类删除失败', 'error')
        return {'status': False}
    except Exception as e:
        flash(self, '标签或分类删除失败', 'error')
        return {'status': False}


def article_content_lib(self, article_id):
    """06文章明细"""
    if article_id is None:
        return {'status': False, 'msg': '缺少文章ID'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}
    article.readnum += 1
    self.db.add(article)
    self.db.commit()
    return {'status': True, 'msg': '获取到文章', 'data': article}


def add_comment_lib(self, content, article_id):
    """07文章评论添加"""
    if article_id is None:
        return {'status': False, 'msg': '缺少文章ID'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}
    comment = Comment()
    comment.content = content
    comment.article_id = article_id
    comment.user_id = self.current_user.id
    self.db.add(comment)
    self.db.commit()
    return {'status': True, 'msg': '评论提交成功'}


def add_second_comment_lib(self, commont_id, content):
    """08文章二级评论添加"""
    if commont_id is None:
        return {'status': False, 'msg': '缺少评论ID'}
    comment = Comment.by_id(commont_id)
    if comment is None:
        return {'status': False, 'msg': '评论不存在'}
    secondComment = SecondComment()
    secondComment.content = content
    secondComment.comment_id = commont_id
    secondComment.user_id = self.current_user.id
    self.db.add(secondComment)
    self.db.commit()
    return {'status': True, 'msg': '二级评论提交成功'}


def add_like_lib(self, article_id):
    """09点赞添加"""
    if article_id is None:
        return {'status': False, 'msg': '文章ID不存在'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章ID不正确'}
    if self.current_user in article.user_likes:
        article.user_likes.remove(self.current_user)
        self.db.add(article)
        self.db.commit()
        return {'status': True, 'msg': '您已经取消点赞了'}
    article.user_likes.append(self.current_user)
    self.db.add(article)
    self.db.commit()
    return {'status': True, 'msg': '点赞成功'}


# 文章搜索
def search_article_lib(self, category_id, tag_id):
    if tag_id is not None:
        tag = Tag.by_id(tag_id)
        articles =  tag.articles
    if category_id is not None:
         category = Category.by_id(category_id)
         articles = category.articles
    comments = dbSession.query(Comment).order_by(Comment.createtime.desc()).all()
    tags = Tag.all()
    categorys = Category.all()
    return articles, comments, tags, categorys


# 文章编辑页面文章列表
def articles_modify_list_lib(self):
    articles = Article.all()
    return articles


# 文章修改
def articles_modify_lib(self, article_id):
    if article_id is None:
        return {'status': False, 'msg': '文章ID不存在'}
    article = Article.by_id(article_id)
    tags, categorys = get_tags_categorys_lib(self)
    return article, categorys, tags


# 文章删除
def articles_delete_lib(self, article_id):
    if article_id is None:
        return {'status': False, 'msg': '文章ID不存在'}
    article = Article.by_id(article_id)
    if article is not None:
        self.db.delete(article)
        self.db.commit()
    return Article.all()