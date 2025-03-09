# 我的 Latex 中文排版模板

## 安装说明

- 安装 VSCode 插件 Latex Workshop
- 在写 Latex 时，如果 `main.tex` 文件里的导入宏包处发生错误，大概率是系统少装了宏包，少啥装啥即可

## 目录说明

- `.vscode`：VSCode 配置文件，配置 Latex Workshop 插件的编译缓存默认输出路径为 `./build`（相对于 `latex` 目录）
- `latex`：存放 LaTeX 书写需要的所有文件
    - `build`：存放编译缓存文件，为 Latex Workshop 插件自动生成，如果开了自动保存，该文件会一直更新
    - `code`：存放文章书写需要的代码文件
    - `figure`：存放文章书写需要的图片文件
    - `references`：存放参考文献文件
    - `*.tex`：存放 LaTeX 源文件，`main.tex` 为主文件，一般来说：
        - `Summary.tex`：摘要
        - `Content.tex`：目录
        - `Premise.tex`：假设
        - `Notation.tex`：符号表
        - `Appendix.tex`：附录
- `out`：存放编译后的 PDF 文件
- `project`：存放项目文件，该文件夹存放实验性的代码，当代码检验成功后再放入 `code` 文件夹中

## Make 命令

- `make`：编译 PDF 文件，预览 PDF 文件，删除编译缓存文件
- `make help`：显示所有命令信息

> [!IMPORTANT]
> 引用文献时，命令需要使用 `make paper config=1`
