$(function(){
    //设置样式
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/dawn");
    editor.renderer.setOption('showGutter', false);
    editor.renderer.setOption('showPrintMargin', false);
    editor.renderer.setOption('showLineNumbers', false);
    editor.getSession().setUseWrapMode(true);
    editor.gotoLine(0);
    /*
    editor.setValue("```model\r\ntable `user` comment '用户信息'\r\n" +
        "field `id` bigint auto_increment pk comment '用户id'\r\n" +
        "field `login_name` varchar(20) not null uk comment '登录名'\r\n" +
        "field `user_name` varchar(20) not null comment '用户姓名'\r\n" +
        "field `age` tinyint not null default 0 comment '性别'\r\n" +
        "---\r\n" +
        "\r\n" +
        "table `class` comment '班级信息'\r\n" +
        "field `id` bigint auto_increment pk comment '班级id'\r\n" +
        "field `class_name` varchar(50) not null comment '班级名称'\r\n" +
        "---\r\n" +
        "\r\n" +
        "table `address` comment '住址'\r\n" +
        "field `id` bigint pk not null comment '住址id'\r\n" +
        "field `address` varchar(255) not null comment '住址'\r\n" +
        "---\r\n" +
        "\r\n" +
        "relation `user`->n-n<-`class`\r\n" +
        "relation `user`->1-n<-`address`\r\n" +
        "```");*/
})