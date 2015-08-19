# win_texmake
Compile tex to pdf, open with acrobat reader

本程序做的事情：
- 记住 acrobat 的窗口位置、当前所在页码等
- 关闭 acrobat，编译 tex
- 重新打开生成的 pdf
- 回到关闭前的状态

## Usage
- Edit texmake.ini
- Run command
```bash
make
```
or
```bash
python texmake.py
```

#### simple way
- Just copy texmake.ini, texmake.py, Makefile to working directory.
Then run command.
- See https://github.com/bssthu/win_texmake/releases/latest , download demo_simple.zip

#### more complex way
- See https://github.com/bssthu/win_texmake/releases/latest , download demo_shadow.zip

#### change output directory
- Change output_directory in texmake.ini
- Or run command
```bash
make output-directory=../build
```
- Or run command
```bash
python --output-directory=../build
```

## License
GPLv3
