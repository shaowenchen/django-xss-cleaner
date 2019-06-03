==================
django-xss-cleaner
==================

django-xss-cleaner 是一个基于 bleach 的 django XSSFilter 工具，实现了对 GET 和 POST 请求参数的 XSS 白名单过滤功能。包中内置了部分白名单 HTML 标签、属性设置，同时也支持自定义扩展。


settings.py 安装和配置说明
-----------------------------

1. 安装中间件

   添加中间件 "xss_cleaner.middlewares.CleanXssMiddleware" 到 settings 中

  ::

    MIDDLEWARE_CLASSES = (
       'xss_cleaner.middlewares.CleanXssMiddleware',
       ...
    )

  建议将 CleanXssMiddleware 尽量的靠前放置，最好是第一个。这是为了保证后端获取的数据都通过了 XSS 过滤，避免 XSS 向量被注入。


2. [可选]配置Clean XSS级别

  默认配置为 'HIGHT'，可选参数：['LOW', 'HIGH']

  ::

    XSS_LEVEL = 'HIGH'

  如果设置为 ‘HIGHT’ ，允许的标签和属性为
  ::

    {
        'tags': ['a', 'img', 'strong', 'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'ul', 'ol', 'tr', 'th', 'td', 'li'],
        'attributes': {'a': ['href', 'title', 'target'], 'img': ['width', 'height', 'src']},
        'styles': [],
        'strip': False,
        'strip_comments': False
    }

  如果设置为 'LOW' ，允许的标签和属性为
  ::

    {
        'tags': ['a', 'img', 'br', 'strong', 'b', 'code', 'pre', 'p', 'div', 'em', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'ul', 'ol', 'tr', 'th', 'td', 'hr', 'li', 'u'],
        'attributes': {'a': ['href', 'title', 'target'], 'img': ['width', 'height', 'src', 'alt'],
                  '*': ['class', 'style']},
        'styles': [],
        'strip': False,
        'strip_comments': False
    }

  参数的含义，在下面会有介绍。

3. [可选]自定义新增白名单

  增量式添加新的标签和属性到白名单。
  ::

    BLEACH_WHITE_LIST = {
        'tags': [],
        'attributes': {},
        'styles': [],
        'strip': False,
        'strip_comments': False
    }

  参数说明：

  -  tags (list)  – 允许的标签，不在白名单的标签被转义
  -  attributes (dict)  – 允许的属性，不在白名单的属性被删除
  -  styles (list) – 允许的样式，不在白名单的样式被删除
  -  strip (bool) – 是否剔除转义后的字符
  -  strip_comments (bool) – 是否剔除 HTML comments


  BLEACH_WHITE_LIST 中的标签、属性、样式，将会以增量的形式增加在 Clean XSS 级别允许的白名单上。如果设置了 strip、strip_comments ，将覆盖默认设置。

4. [可选]是否打印或记录转义

  为了方便调试，记录 XSS Filter 的信息，提供一个开关:

    ::

       BLEACH_SHOW = True

  默认值为 True，可选值为 [True ，False]

  如果是本地开发，转换日志将直接 print 在 Console。如果是线上，将打印为 warning  日志。


xss_cleaner 豁免装饰器
------------------------

xss_cleaner 包提供了两个装饰器，用于豁免 XSS Filter 处理。

- escape_clean，提供 View 级别的豁免。

  ::

    from cleanxss.decorators import escape_clean
     @escape_clean
     def home(request):
        pass

- escape_clean_param，提供参数级别的豁免。

  ::

    from cleanxss.decorators import escape_clean_param
     @escape_clean_param('param1', 'param2')
     def home(request):
        pass




xss_cleaner 处理示例
-----------------------

下面使用的是默认配置： XSS_LEVEL= ‘HIGH'


 ::

    转义非白名单标签
    XSS Clean: Transfer  <b><i>an example</i></b>  To  &lt;b&gt;&lt;i&gt;an example&lt;/i&gt;&lt;/b&gt;

     删除非白名单样式
    XSS Clean: Transfer  <p class="foo" style="color: red; font-weight: bold;">blah blah blah</p>  To  <p>blah blah blah</p>

     删除非白名单属性
    XSS Clean: Transfer  <img click="de"  alt="an example" width=500>  To  <img width="500">

     自动补全，规范化 HTML
    XSS Clean: Transfer  <a href=http://abc.com>my text; a b b  To  <a href="http://abc.com">my text; a b b</a>


下面使用的是默认配置： XSS_LEVEL= LOW'

  ::

    转义非白名单标签
    XSS Clean: Transfer  <b><i>an example</i></b>  To  <b>&lt;i&gt;an example&lt;/i&gt;</b>

    删除非白名单样式
    XSS Clean: Transfer  <p class="foo" style="color: red; font-weight: bold;">blah blah blah</p>  To  <p class="foo" style="">blah blah blah</p>

    删除非白名单属性
    XSS Clean: Transfer  <img click="de"  alt="an example" width=500>  To  <img alt="an example" width="500">

    自动补全，规范化 HTML
    XSS Clean: Transfer  <a href=http://abc.com>my text; a b b  To  <a href="http://abc.com">my text; a b b</a>
