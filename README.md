# hnucm-notice

## 功能

查询并打印HNUCM研究生院官网的最新通知。

每次运行后，会获取官网的最新通知，并将“新标题”与本地的“旧标题”对比。若有新通知，则突出显示，并用“新标题”覆盖“旧标题”。

* [通知公告](https://yjsy.hnucm.edu.cn/zsxx/tzgg.htm)
* [硕士生招生](https://yjsy.hnucm.edu.cn/zsxx/ssszs.htm)
* [招生简章](https://yjsy.hnucm.edu.cn/zsxx/zsjz.htm)
* [博士生招生](https://yjsy.hnucm.edu.cn/zsxx/bsszs.htm)

## 使用

1. 克隆项目，安装依赖：

   ```
   git clone https://github.com/shujuecn/hnucm-notice.git
   pip3 install requests
   pip3 install lxml
   ```

2. 修改预设，定制查询：

   ```python
   # auto-hnucm.py
   # 查询开关（1：开启  0：关闭）
   main(
     tzgg=1,     # 通知公告
     ssszs=1,    # 硕士生招生
     zsjz=0,     # 招生简章
     bsszs=0     # 博士生招生
   )
   ```

3. 打开文件，运行项目：

   ```bash
   cd hnucm-notice
   python3 auto-hnucm.py
   ```

## 演示

### macOS

* ![](https://p.ipic.vip/zc7lik.png)

## 致谢

[GitHub Copilot](https://github.com/features/copilot) 和 [ChatGPT](https://openai.com/blog/chatgpt/) 在整个开发过程中一直陪伴在我们身边，提供了宝贵的指导意见。没有它们，本项目将难以完成。在此，我们对它们表示由衷的感谢。

