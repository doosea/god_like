# git 学习笔记


[Git 教程](https://www.liaoxuefeng.com/wiki/896043488029600)   

## git 配置

    1. git config --global user.name "duhaipeng"
    2. git config --global user.email "duhaipeng@enn.cn" 
    3. git config --global core.editor vim
    4. git config  credential.helper store

## git 基本语法
    1. git init : 初始化本地仓库
    2. git add <file> : 添加本地文件到暂存区
    3. git commit -m <message>： 暂存区文件提交到本地仓库
    4. git status : 查看当前状态
    5. git log / git log --pretty=oneline : 查看提交日志
    6. git reset --hard HEAD^ : 回退到上一版本
       git reglog: 查看命令历史
       git reset --hard <commit_id>： 回退到指定版本
    7. git checkout -- <file> ： 丢弃工作区的修改,把文件回退到最后一次的状态，git commit 或git add
       git checkout: 版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原” 
    8. git reset HEAD <file> : 丢弃暂存区的文件
    
    
## 远程仓库
    1. git remote add origin <git repository url>: 其中origin为远程库的名字
    2. git push -u origin master: 提交本地到远程, 首次提交，加上-u参数，
        git push -u orgin master = git push origin master + git branch --set-upstream-to=origin/master master
    3. git colne <git repository url> : clone 远程仓库到本地
    
## 分支管理
    1. git branch : 查看当前分支
       git branch -a : 查看本地与远程的所有分支
    2. git checkout -b dev : 创建并切换 dev 分支
        = git branch dev + git checkout dev 
    3. git merge <branch-name>: 合并分支到当前分支
    4. git branch -d <branch-name> : 删除分支
        - git push origin --delete [branch_name]: 删除远程分支
    5. git log --graph --pretty=oneline --abbrev-commit : 查看分支合并图
    6. git merge --no-ff -m "merge with no-ff" dev1:  
    7. git stash : 把当前修改的内容存起来
       git stash list :  查看stash 的内容
       git stash pop : 恢复暂存的内容
        = git stash apply +  git stash drop:
    8. git cherry-pick <commit-id>: 复制一个特定的提交到当前分支
    
    9. git rebase -i [start-commit-id] [end-commit-id]: 合并多个commit 
        git config core.editor vim : 修改git 编辑器为vim


## 标签管理
标签总是和某个commit挂钩。如果这个commit既出现在master分支，又出现在dev分支，那么在这两个分支上都可以看到这个标签。

    1. git tag : 查看所有标签
    2. git tag <tagname>: 为最近的提交打标签
    3. git show <tagname>: 查看标签的详细信息
    4. git tag -a <tagname> -m "msg"： 指定标签信息
       
    因为创建的标签都只存储在本地，不会自动推送到远程。所以，打错的标签可以在本地安全删除。
    5. git tag -d <tagename> ： 删除本地标签
    6. git push origin <tagname> : 推送某个标签到远程
    7. git push origin --tags: 推送全部未推送过的本地标签
    8. git push origin :refs/tags/<tagname>:　可以删除一个远程标签

## git 命令补充
### 1. 文件的四种状态：
- Untracked: 未跟踪， 显示红色
- Unmodify: 未被修改，（已经被git管理的文件），　显示白色
- Modified: 修改的（已经被git管理的文件）， 显示蓝色
- Staged： 暂存状态
   ```
    新建文件--->Untracked

    使用add命令将新建的文件加入到暂存区--->Staged
    
    使用commit命令将暂存区的文件提交到本地仓库--->Unmodified
    
    如果对Unmodified状态的文件进行修改---> modified
    
    如果对Unmodified状态的文件进行remove操作--->Untracked
   ```
   
        

### 2. 各个操作区之间的转换

```
            add                          commit                push
工作区  --------------->   暂存区（Stage） ------->   本地仓库   ------->   远程仓库
工作区  <---------------   暂存区（Stage） <-------   本地仓库   <-------   远程仓库
           restore                        reset                 pull
    git checkout -- file

ps： git checkout 既可以切换分支，又可以更改文件。 后来拆分成了git switch  和 git restore
```
1. `工作区 < == > 暂存区`
    - `git add file` : 工作区 == > 暂存区
    - `git restore --staged file` :暂存区 == > 工作区，  撤销 git add 的记录， 从暂存区回到工作区，但是不改变文件的内容
    - `git restore file` : 暂存区 == > 工作区， 撤销工作区的修改，使之回到原始的状态（修改之后未add的修改全都舍弃）
   
    - `git rm --cached file` : 删除暂存区或分支上的文件, 但是本地还有, 文件状态由Staged ==> Untracked
    - `git rm (-f) file` : 删除暂存区或分支上的文件, 同时工作区也不需要这个文件了(谨慎使用)
    
    - `git checkout -- file` :  == `git restore file` 
    
2. `暂存区 < == > 本地仓库`
    - `git commit -m "mesage" `: 暂存区 == > 本地仓库
    - `git reset  HEAD^ ` : 本地仓库 == > 暂存区, 取消上一次的提交， 变化add之前的状态。(上次提交有错误)
    - `git reset --soft  HEAD^ ` : 本地仓库 == > 暂存区, 取消上一次的提交， 变化add 之后， commit之前的状态（上次提交没错误，修改commit msg）
    - `git reset HEAD -- file` : 本地仓库 == > 暂存区， 拉取最近一次提交到版本库的文件到暂存区  该操作不影响工作区
    - `git reset 版本号 -- file` : 本地仓库 == > 暂存区， 拉取提交到版本库某个版本下的文件到暂存区  该操作不影响工作区
 
3. 版本回退
    - `git reflog`: 查找回退版本的commit id
    - `git reset --hard commit_id` : 回退本地分支
    - `git push -f`: 强退本地分支到远程   