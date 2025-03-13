# compilers
XETEXC  := /usr/bin/xelatex  # 使用XeLaTex引擎
BIBTEXC := /usr/bin/bibtex   # 参考文献处理工具
LATEXC  := /usr/bin/pdflatex # PDFLaTeX引擎

# paths
PROJECT_ROOT := $(shell pwd)
OUTPUT_DIR := $(PROJECT_ROOT)/out

# sources
PAPER_BUILD_SOURCE := $(PROJECT_ROOT)/latex/main.tex

define _clean =
	-@rm -f $(OUTPUT_DIR)/*.{aux,bbl,blg,out,toc}
	-@rm -rf $(OUTPUT_DIR)/references
	-@rm -f $(PROJECT_ROOT)/latex/*.{aux,fdb_latexmk,fls,log}
	-@rm -f $(PROJECT_ROOT)/*.{aux,fdb_latexmk,fls,log,xdv,toc}
endef

all : paper clean
	@xdg-open ./out/main.pdf

paper : $(PAPER_BUILD_SOURCE)
	@mkdir -p $(OUTPUT_DIR)
	@$(XETEXC) --output-directory=$(OUTPUT_DIR) $(PAPER_BUILD_SOURCE)	# 首次编译
ifdef configbib
	@cp -r ./latex/references/ $(OUTPUT_DIR)/							# 复制参考文献
	@cd $(OUTPUT_DIR) && $(BIBTEXC) main.aux							# 处理参考文献
endif
	@$(XETEXC) --output-directory=$(OUTPUT_DIR) $(PAPER_BUILD_SOURCE)	# 二次编译
	@$(XETEXC) --output-directory=$(OUTPUT_DIR) $(PAPER_BUILD_SOURCE)	# 三次编译
	@$(XETEXC) --output-directory=$(OUTPUT_DIR) $(PAPER_BUILD_SOURCE)	# 四次编译
	$(_clean)

preview:
	@xdg-open ./out/main.pdf

clean :
	$(_clean)

debug :
	@echo $(OUTPUT_DIR)
	@echo $(PROJECT_ROOT)
	@echo $(LATEXC)
	@echo $(PAPER_BUILD_SOURCE)

help:
	@echo -e "\e[36m\nLatex 项目命令帮助：\e[0m"
	@echo -e "  \e[32mmake paper\e[0m       \e[36m编译论文主文档\e[0m"
	@echo -e "  \e[32mmake paper \e[1;33mconfigbib=1\e[0m  \e[36m编译并处理参考文献\e[0m"
	@echo -e "  \e[32mmake clean\e[0m       \e[36m清理临时编译文件\e[0m"
	@echo -e "  \e[32mmake debug\e[0m       \e[36m显示调试信息\e[0m"
	@echo -e "  \e[32mmake help\e[0m        \e[36m显示本帮助信息\e[0m"

.PHONY : debug paper preview help
