//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}

$(document).ready(function () {
    //上传文件
    $("#upload_btn").click(function () {
        event.preventDefault();
        console.log($('#input_files_id'))
        console.log('-------------------==================-----------------');
        var formdata = new FormData();
        var files_upload = $('#input_files_id')[0];
        for (var i = 0; i < files_upload.files.length; i++) {
            console.log(files_upload.files[i]);
            formdata.append("importfile", files_upload.files[i]);
        }
        console.log('-------------------==================-----------------');
        console.log(formdata);
        $.ajax({
            'url': "/files/files_up_load",
            'type': "POST",
            'data': formdata,
            'headers':{
               'X-XSRFTOKEN': get_cookie('_xsrf')
            },
            'cache': false,
            'processData': false,
            'contentType': false,
            'success': function (data) {
                if (data['status'] != 200) {
                    alert(data['msg']);
                } else {
                    var show_path = document.getElementById('show_path');
                    show_path.innerHTML = '';
                    for (var i = 0; i < data['data'].length; i++) {
                        var filename = data['data'][i]['data'];
                        var msg = data['data'][i]['msg'];
                        var html = '';
                        html += '<div class="images item ">';
                        html += '<div class="item">' + filename + '</div><br/>';
                        html += '<p>' + msg + '</p>';
                        show_path.innerHTML += html;
                    }
                }
            }
        });
    });
});

 //点击删除文件按钮函数
$(document).ready(function () {
        var files_delete = $('.files_delete');
       //循环遍历所有的标签，绑定事件
       for (var i = 0; i < files_delete.length; ++i) {
           files_delete[i].onclick = function () {
               var uuid = this.getAttribute('data-id');
                event.preventDefault();
                $.ajax({
                    'url': '/files/files_delete',
                    'type': 'post',
                    'headers':{
                       'X-XSRFTOKEN': get_cookie('_xsrf')
                    },
                    'data': {
                        'uuid': uuid
                    },
                    'success': function (data) {
                        if (data['status'] == 200) {
                            swal({
                                'title': '正确',
                                'text': data['msg'],
                                'type': 'success',
                                'showCancelButton': false,
                                'showConfirmButton': false,
                                'timer': 1000,
                            },function () {
                               location.reload();
                            });
                        }else{
                            swal({
                                'title': '错误',
                                'text': data['msg'],
                                'type': 'error',
                                'showCancelButton': false,
                                'showConfirmButton': false,
                                'timer': 1000,
                            })
                        }
                    }
                })
           }
       }
});
//彻底删除文件
$(document).ready(function () {
        var files_delete = $('.files_delete');
       //循环遍历所有的标签，绑定事件
       for (var i = 0; i < files_delete.length; ++i) {
           files_delete[i].onclick = function () {
               var uuid = this.getAttribute('data-id');
                event.preventDefault();
                $.ajax({
                    'url': '/files/files_delete',
                    'type': 'post',
                    'headers':{
                       'X-XSRFTOKEN': get_cookie('_xsrf')
                    },
                    'data': {
                        'uuid': uuid
                    },
                    'success': function (data) {
                        if (data['status'] == 200) {
                            swal({
                                'title': '正确',
                                'text': data['msg'],
                                'type': 'success',
                                'showCancelButton': false,
                                'showConfirmButton': false,
                                'timer': 1000,
                            },function () {
                               location.reload();
                            });
                        }else{
                            swal({
                                'title': '错误',
                                'text': data['msg'],
                                'type': 'error',
                                'showCancelButton': false,
                                'showConfirmButton': false,
                                'timer': 1000,
                            })
                        }
                    }
                })
           }
       }
});



