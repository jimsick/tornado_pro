//获取图形验证码
var code = "";
function get_image_code() {
    var d = new Date().getTime();
    var pre_code = code;   //第一次pre_code为空  第二次per_code为上一次code的时间
    code = d; //现在的时间
    $(".get_image_code").attr("src", "/auth/captcha?pre_code="+pre_code+"&code="+code);  //向服务器请求
    $(".captcha-code").attr("value",code);  //取到code存放在隐藏的input中
}


$(document).ready(function(){
    get_image_code();
    //点击获取图形验证码
    $('#a_code').click(function () {
        get_image_code();
    });
});
