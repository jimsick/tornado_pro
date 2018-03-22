
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");  //正则取出csrf
    return xsrf_cookies[1]
}

//点击忘记密码，通过邮箱重设密码
$(document).ready(function(){
    $('#modify_passsword').click(function () {
        swal({
            'title': '请输入邮箱',             //提示框标题
            'text': '输入绑定的邮箱',            //提示内容
            'type':'input',            //提示类型，有：success（成功），error（错误），warning（警告），input（输入）
            'showCancelButton': true,       //是否显示“取消”按钮。
            'animation': 'slide-from-top',  //提示框弹出时的动画效果，如slide-from-top（从顶部滑下）等
            'closeOnConfirm': false,        //确认按钮被关闭后，Alert也被关闭，设为false将自动调用下面的函数——也就是启动后续Alert。
            //closeOnCancel: false          // 作用与closeOnConfirm类似
            'showLoaderOnConfirm': true,        //
            'inputPlaceholder': '输入邮箱',  //
            //confirmButtonColor: '#DD6B55',  // 确认用途的按钮颜色，自定
            'confirmButtonText': '确定',      //定义确定按钮文本内容
            'cancelButtonText': '取消'        //定义取消按钮文本内容
            //timer	设置自动关闭提示框时间（毫秒）。
            //html	是否支持html内容。
        },function (inputValue) {
            if(inputValue == ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            $.ajax({
               'url': '/auth/send_password_email',
                'type': 'post',
                'data': {
                   'email': inputValue
                },
                'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
                },
                'success': function (data) {
                   if(data['status'] == 200){
                       swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1500,
                         'closeOnConfirm': false
                        },function () {
                           // window.location = '/auth/regist';
                           window.location = '/';
                        });
                   }else {
                        swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1500
                        });
                   }
                }
            });
        });
    });
});



//提交登录请求
$(document).ready(function(){
    $('#submit_login').click(function () {
        event.preventDefault();
        var remember = '';
        $.each($('input:checkbox'),function(){
            if(this.checked){
                remember = $(this).val();
            }else{
                remember = '';
            }
        });
        $.ajax({
            'url': '/auth/user_login',
            'type': 'post',
            'data': {
               'name': $('#name').val(),
               'password':  $('#password').val(),
               'code':  $('#code').val(),
               'captcha':  $('#captcha').val(),
               'remember':  remember
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
               if(data['status'] == 200){
                   swal({
                    'title': '正确',
                    'text': data['msg'],
                    'type': 'success',
                    'showCancelButton': false,
                    'showConfirmButton': false,
                    'timer': 1500,
                    'closeOnConfirm': false
                    },function () {
                       window.location = '/account/user_profile';
                    });
               }else {
                    swal({
                    'title': '错误',
                    'text': data['msg'],
                    'type': 'error',
                    'showCancelButton': false,
                    'showConfirmButton': false,
                    'timer': 1500
                    });
                    get_image_code();
               }
            }
        });
    });
});

