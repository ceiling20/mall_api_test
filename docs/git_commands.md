 Git 查用命令速查表
---
## 基本操作
| 命令               | 作用                  | 实例                                                               | 
|------------------|---------------------|------------------------------------------------------------------|
| `git clone`      | 克隆远程仓库到本地           | `git clone https://github.com/ceiling20/api-automation-test.git` |  
| `git add`        | 添加文件更改到暂存区          | `git add ./git add test.py`                                      |
| `git commit -m ` | 把暂存区文件提交到到本地仓库并附加消息 | `git commit -m "update"`                                         |    
| `git push `      | 将本地提交推送到远程仓库        | `git push origin main`                                           |
| `git pull `      | 将远程仓库代码拉取到本地并合并     | `git pull origin main`                                           |
## 分支管理
| 命令           | 作用          | 实例                                                                                  | 
|--------------|-------------|-------------------------------------------------------------------------------------|
| `git branch` | 列出、创建、删除分支  | `git branch feature-asd`(创造asd分支) `git branch`(列出分支) `git branch -d main`(删除main分支) |
| `git switch` | 切换分支、恢复文件   | `git switch main`(切换main分支) `git switch -c main`(创造并切换到main分支)                      |
| `git merge`  | 合并其他分支到当前分支 | `git merge main`                                                                    |
## 状态和日志
| 命令            | 作用             | 实例                  | 
|---------------|----------------|---------------------|
| `git status ` | 查改当前工作区和暂存区的状态 | `git status`        |
| `git log`     | 查看提交历史         | `git log --oneline` |
## 💡 使用小贴士
- `git add .` 会把当前目录下所有修改加入暂存区，适合批量提交。
- 提交前用 `git status` 确认文件状态，避免误提交。
- 分支操作前，先切换到目标分支再执行 `git switch` 或 `git merge`，防止误操作。