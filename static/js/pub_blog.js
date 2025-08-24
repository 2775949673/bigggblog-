window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    // 设置CSRF令牌到AJAX请求头
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
            }
        }
    });

    $("#submit-btn").click(function(event){
        console.log("点击了提交按钮");
        event.preventDefault();
        event.stopPropagation();

        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        
        // 添加表单验证
        if (!title || !content) {
            alert("标题和内容不能为空");
            return;
        }

        $.ajax({
            url: '/blog/pub',
            type: 'POST',
            dataType: 'json',
            data: {
                title: title,
                category: category,
                content: content
            },
            success: function(result){
                if(result.code == 200){
                    window.location.href = '/blog/detail/' + result.data.blog_id;
                } else {
                    alert(result.message);
                }
            },
            error: function(xhr, status, error) {
                if (xhr.status === 405) {
                    alert("请求方法不正确，请刷新页面重试");
                } else if (xhr.responseText) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        alert(response.message || "请求失败");
                    } catch (e) {
                        alert("服务器错误: " + xhr.statusText);
                    }
                } else {
                    alert("网络错误，请检查连接");
                }
                console.error("AJAX错误:", status, error, xhr.responseText);
            }
        });
    });
}