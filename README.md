## 提取日志

- 在 `settings.py` 内进行设置；

- `access.log` 放在 `./access_login` 目录下；

- `gateway.log` 放在 `./gateway_login` 目录下；

- 运行 `pipeline.py`：

  1. 按天切割 access 日志

  2. 按天合并 gateway 日志

  3. 按天生成 access csv 文件

  4. 按天生成 gateway csv 文件

  5. 按行行切割 csv 文件
