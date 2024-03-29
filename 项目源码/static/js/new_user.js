page_no = 1;
all_page_param = ' 1=1 ';
layui.use(['form', 'layer', 'laydate'], function () {

    $ = layui.jquery;
    var form = layui.form,
        layer = layui.layer,
        laydate = layui.laydate;
    //执行一个laydate实例
    // laydate.render({
    //     elem: '#start' //指定元素
    // });

    //执行一个laydate实例
    // laydate.render({
    //     elem: '#end' //指定元素
    // });


//监听提交(修改相关)
    form.on('submit(edit)', function (data) {
        console.log(JSON.stringify(data.field));
        $.ajax({
            url: "/old/edit",
            data: data.field,
            method: "POST",
            success: function (obj) {
                layer.closeAll();
                layer.msg("修改成功！", {icon: 6})
                get_old_data(page_no)
            },
            error: function (xhr, type, errorThrown) {

            }
        });

        return false;
    });

});
get_old_data(page_no);
max_page = 0;

function get_old_data(no) {
    page_no = no;
    $.ajax({
        url: "/user/list",
        data: {"page_size": 10, "page_no": page_no, "param": all_page_param},
        method: "POST",
        success: function (obj) {
            page_data = obj.data;
            page_list = obj.page_list;
            max_page = obj.max_page;
            show_data(page_data, page_no, page_list)
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function show_data(page_data, page_no, page_list) {
    console.log(page_data, page_no, page_list)
    list_data = '';
    for (var i = 0; i < page_data.length; i++) {
        item = page_data[i];
        list_data = list_data + '<tr>' +
            // '<td>' + (i + 1) + '</td>' +
            '<td>' + item[0] + '</td>' +
            '<td>' + item[1] + '</td>' +
            '<td>' + item[2] + '</td>' +
            '<td>' + item[3] + '</td>' +
            '<td>' + item[4] + '</td>' +
            '<td>' + item[5] + '</td>' +
            // '<td>' + item[6] + '</td>' +

            '<td class="td-manage">' +
            ' <a title="编辑"  onclick="user_edit(\'编辑\',\'' + item[0] + '\',' + item[1] + ',' + item[2] + ',' + item[3] + ',' + item[4] + ',' + item[5] + ')" href="javascript:;">' +
            '  <i class="layui-icon">&#xe63c;</i>' +
            '  </a>' +
            '        <a title="删除" onclick="user_del(this,\'' + item[0] + '\')" href="javascript:;">' +
            '  <i class="layui-icon">&#xe640;</i>' +
            '              </a>' +
            '            </td>' +
            '          </tr>'
    }
    if (page_no == 1) {
        page_str = ''
    } else {
        page_str = '<span class="prev" onclick="get_old_data(' + (page_no - 1) + ')">&lt;&lt;</span>';
    }
    for (var i = 0; i < page_list.length; i++) {
        item = page_list[i];
        if (item == page_no) {
            page_str = page_str + '<span class="current">' + item + '</span>'
        } else {
            page_str = page_str + '<span class="num" onclick="get_old_data(' + item + ')">' + item + '</span>'
        }
    }
    if (page_no != max_page) {
        page_str = page_str + ' <span class="next" onclick="get_old_data(' + (page_no + 1) + ')">&gt;&gt;</span>'
    }

    $("#old_data").html(list_data);
    $("#page_list").html(page_str);

}


function user_edit(title, a, b, c, d, e, f, g, h, i, w, he) {
    console.log(title, a, b, c, d, e, f, g, h, i, w, he)
    if (w == null || w == '') {
        w = 600
    }
    if (he == null || he == '') {
        he = 650
    }
    $('#id').val(a);
    $('#province').val(b);
    $('#confirm').val(c);
    $('#confirm_add').val(d);
    $('#heal').val(e);

    layer.open({
        type: 1,
        area: [w + 'px', he + 'px'],
        fix: false, //不固定
        maxmin: true,
        shadeClose: true,
        shade: 0.4,
        title: title,
        content: $('#old-edit')
    });
}

/*删除*/
function user_del(obj, ds) {
    layer.confirm('确认要删除吗？', function (index) {
        //发异步删除数据
        $(obj).parents("tr").remove();
        $.ajax({
            url: "/user/del",
            data: {"ds": ds},
            method: "DELETE",
            success: function (obj) {
                layer.msg('已删除!' + ds, {icon: 1, time: 1000});
            }
        });
    });
}

/*查询*/
function get_search() {
    param = ' 1=1 ';

    console.log(start)
    if (start != null && start != '') {
        param = param + " and ds>= '" + start + "'";
    }
    if (end != null && end != '') {
        param = param + " and ds<= '" + end + " 23:59:59'";
    }
    all_page_param = param;
    get_old_data(page_no)
}
function user_close(obj,ds) {
     
     layer.confirm('确认要修改吗？', function (index) { 
         //alert(index);
         $(obj).parents("tr").remove();
         $.ajax({
             url: "/user/revise",
             data: {"ds": ds},
             method: "DELETE",
             success: function (obj) {
                 layer.msg('已删除!' + ds, {icon: 1, time: 1000});
             }
         });
     });
 }