linux 查用命令表
---
| 命令      | 作用            | 例子                                                                        |
|---------|---------------|---------------------------------------------------------------------------|
| ls      | 显示所有文件（包括隐藏）  | ls -l                                                                     |
| cd      | 进入路径          | cd testcase/                                                              |
| pwd     | 查询当前路径        | pwd                                                                       |
| mkdir   | 创建文件夹         | mkdir test                                                                |
| rm      | 删除文件          | rm test.txt rm -rf test                                                   |
| cp      | 复制文件          | cp aaa.txt bbb.txt                                                        |
| mv      | 重命名/剪切        | mv aaa.txt bbb.txt/mv test/aaa.txt testcase/aaa.txt                       |
| cat     | 显示文件全文        | cat aaa.txt                                                               |
| less    | 查看文件          | less -N aaa.txt                                                           |
| head    | 查看文件最前面几行     | head -n 20 aaa.txt                                                        |
| tail    | 查看文件最后几行      | tail -n 20 aaa.txt                                                        |
| grep    | 查看是否有包含xxx的文件 | grep -r "error"  .                                                        |
| ps      | 查看进程          | ps aux                                                                    |
| kill    | 杀死进程          | kill -9 pid                                                               |
| chmod   | 给文件赋权         | chmod 777 aaa.txt chmod -w aaa.txt                                        |
| netstat | 查看监听端口        | netstat -tlnp                                                             |  
| curl    | 查看网址内容，下载文件   | curl http://example.com/api 查看响应/curl -O http://example.com/file.zip 下载文件 |