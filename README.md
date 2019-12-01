# gdb_auto_scrpit
some script for gdb



**break**

- 用于及时开启PIE，也可以准确下断点
- 依赖
  - codebase功能，来自于[pwngdb](https://github.com/scwuaptx/Pwngdb)
  - checksec功能，来自于[pwntools](https://github.com/Gallopsled/pwntools)
- 用法
  - (gdb) source path_to_break.py 
  - 或者 echo "source path_to_break.py " >> ~/.gdbinit
- 下断方式
  - bk address [暂不支持symbol]
  - 例如
    - bk 0x888
