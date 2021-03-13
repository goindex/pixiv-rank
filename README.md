# pixiv-rank

## 安装Python依赖

```bash
pip3 install -r requirements.txt
```

## 获取REFRESH_TOKEN

[@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) 或 [OAuth with Selenium/ChromeDriver](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)

## 修改REFRESH_TOKEN

```bash
vim rank.py

REFRESH_TOKEN = "YOUR TOKEN"
```

## 运行

```bash
python3 rank.py
```

## 致谢

Pixiv API：[PixivPy](https://github.com/upbit/pixivpy)
