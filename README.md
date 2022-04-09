# WebRunner

### 介绍
*   实现一整套web测试项目
*   定义了测试用例层
*   调度策略和执行，日志，都使用pytest。未来会自己实现
*   重载selenium核心类
*   拆分POM模型，实现Page完成功能，component实现页面功能封装，model完成数据驱动
*   mock构造测试场景
*   支持多进程，不支持多线程


**核心类：driver**
*   实现平滑切换项目，依赖session
*   find方法实现
*   增加_pom_方法实现特殊功能


**核心类：session**
*   主要用来实现window_handle的切换。
*   定义指定操作捕获新增未处理窗口
*   操作上，如果点击产生新窗口，必须处理完新窗口，再开启其他page
*   实现page.func级别的切换


**浏览器特点**
1.  打开新页面 target='_blank' 属性的，浏览器会自动切换到tab，但是句柄不切换。selenium无法直接操作。
2.  不管是tab，还是弹窗，一个浏览器只有一个session。其他的多窗口，tab，都属于句柄。



