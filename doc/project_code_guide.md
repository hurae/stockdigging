# Style Guide For This Project

---

## Name

1. 类名使用大驼峰命名，包名用一个小写单词
2. 局部变量、类变量、函数参数、文件名使用小写下划线
3. 常量名使用大写下划线
4. 不要使用python内置关键字命名。这是解释器所允许的，但不是被提倡的。实际作用是覆盖（shadowed）了原关键字。
5. 可能误用的关键词有str/map/dict/list/set

## Comment

1. 在函数定义的前一行，在类定义的前一行写注释
2. 函数注释要解释这个函数的作用，有必要时说明设计的思路；类注释要说明类的作用，有必要时说明类间关系
3. 每个文件的前两行说明该文件的性质和作用，以及包括的主要内容
4. 不要写在语句后面
5. 每个类，每个函数必须写注释
6. 写英文注释

## Git

1. 每天开始工作前先运行update，与远程同步，冲突提示推荐选择Merge
2. 每次完成一个小功能或一个小目标提交一次，描述清楚做了哪些改变
3. 每次commit应包含一次逻辑上相对独立的粒度较细的更改
4. 提交前运行格式化命令
5. 提交前查看所有错误提示（红色线）和警告（黄色线）以及语法错误（绿色线），要求提交的代码中不包含错误，要求尽量消除警告和语法错误
6. 若不慎提交了错误代码，修改后选择amend commit覆盖上次commit，但注意不要覆盖其他人的commit
7. commit时可以选择只提交部分修改后的文件，如果某文件包含符合提交要求的开发完成的功能，而另一修改过的包含尚未开发完成的代码，可以考虑只提交部分文件
8. 尽量不要使用commit and push命令，先commit到本地确认没有问题后再push，这样如果出现问题进行回滚或选择amend commit更加便捷，可保证尽量不污染远程的中心仓库
9. 写英文描述

## Tips

1. CTRL + SHIFT + A --> 打开Action菜单
2. CTRL + L         --> 添加/删除注释
3. CTRL + ALT + L   --> reformat code
4. CTRL + F         --> 查找
5. CTRL + R         --> 替换
6. SHOFT + F6       --> 重构（自动重命名所有相关联的变量名/函数名/类名/文件名等）