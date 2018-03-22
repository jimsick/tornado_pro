#coding=utf-8

# flask中的flash

def flash(self, message, category='message'):
    """先调用flash"""
    flashes = self.session.get('_flashes', [])
    flashes.append((category, message))  #[('error', '保存失败'),('ok', '分类保存了')]
    self.session.set('_flashes', flashes)  # 设置弹出话



def get_flashed_messages(self, with_categories=False, category_filter=[]):
    """后调用get_flashed_messages"""
    flashes = self.flashes
    if flashes is None:
        self.flashes = flashes = self.session.get('_flashes', [])  # 获取缓存并赋值
        del self.session['_flashes']  # 删除缓存
    if category_filter:
        flashes = list(filter(lambda f: f[0] in category_filter, flashes))
    if not with_categories:  # 是否启用分类
        return [x[1] for x in flashes]
    return flashes


#html页面代码与flask相同
#普通闪现
# {% for message in get_flashed_messages() %}
#     <p style="background-color: #bce8f1">{{ message }}</p>
# {% end %}
#
# 分类闪现
# {% for  category, message in get_flashed_messages(with_categories=True) %}
#     {% if category == 'error' %}
#         <p style="background-color: red">{{ message }}</p>
#     {% elif category == 'success'%}
#         <p style="background-color: green">{{ message }}</p>
#     {% end %}
# {% end %}

#过滤闪现
# <!--  过滤闪现 -->
#        {% for  message in get_flashed_messages(category_filter=["error"]) %}
#            <p style="background-color: red">{{ message }}</p>
#        {% end %}
#
#        {% for  message in get_flashed_messages(category_filter=["success"]) %}
#            <p style="background-color: #bce8f1">{{ message }}</p>
#        {% end %}

#弹窗
# { %
# for category, message in get_flashed_messages(with_categories=True) %}
# { % if category == 'error' %}
# < script
# type = "text/javascript" >
# swal({
#     'title': '错误',
#     'text': '{{ message }}',
#     'type': 'error',
#     'showCancelButton': false,
#     'showConfirmButton': false,
#     'timer': 2000
# });
# < / script >
# { % elif category == 'success' %}
# < script
# type = "text/javascript" >
# swal({
#     'title': '正确',
#     'text': '{{ message }}',
#     'type': 'success',
#     'showCancelButton': false,
#     'showConfirmButton': false,
#     'timer': 2000,
# })
# < / script >
# { % end %}
# { % end %}
