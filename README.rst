ueditor4tornado 集成了Ueditor 1.4.3实现了部分上传的文件接口： 1.图片上传 2.文件上传 3.涂鸦板上传

目前为简单实现，使用本地文件系统作为存储。在非NAS存储的场景下只支持单实例运行。

使用方法：

pip install ueditor4tornado

在IOLoop.instance().start()之前调用 ueditor4tornado.registerHandler(application,withStatics=True) 如果statics文件使用nginx服务的情况：设置withStatics=false

HTML的配置在sample/templates/ueditor.html有示例。

不清楚的情况可以直接运行本项目下的sample工程查看效果。