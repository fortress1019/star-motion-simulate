# Pygame 天体运动模拟

## 简介

这是一个天体运动模拟程序。

**⚠ 注意！该项目在 *Windows* 上运行时需要 100% 的缩放比例。如果缩放比例不正确可能会导致体验不佳。**

准备：

```
# macOS
python3 -m pip install pyini pygame

# Windows
python -m pip install pyini pygame
```

## 版本信息

⚠ 注意：目前仍未发布正式版。如果您要体验最新的代码效果：

下载方法一(***推荐***)：`git clone https://github.com/dddddgz/star-motion-simulate`

下载方法二：使用 [GitHub Desktop](https://desktop.github.com) 去下载

下载方法三：点击 Code 按钮，然后点击“Download Zip”下载此项目的 `zip` 版本。  

> 如果以上方法都不可行，请[创建一个 Issue](https://github.com/dddddgz/star-motion-simulate/issues/new/choose)

## 项目设置

### 语言设置

如果你希望更改游戏的语言，则你可以打开 `config/config.ini`，找到 `[language]`下的 `default` 选项，将它更改为你希望显示语言（如 `zh-CN`）。

### 加载模拟

按下面的步骤执行：

1. 打开 `simulation` 文件夹
2. 选择一个你想要使用的文件
3. 复制它的文件名（*不要复制后缀名*）
4. 打开 `config/config.ini`
5. 找到 `[simulation]` 下的 `file` 部分
6. 粘贴文件名
7. 运行程序（如果程序已经在运行，关闭再运行它）

> 你也可以在 `simulation` 文件夹下新建属于你自己的模拟。如果你认为它不错，可以 Fork 这个项目，然后[提交 Pull Request](https://github.com/dddddgz/star-motion-simulate/pulls)

## 操作说明

> 这个部分介绍在程序运行起来后，如何操作它。

- 放大 / 缩小：鼠标滚轮 / + 和 - 键
- 移动视角：鼠标拖动 / ↑↓←→
- 暂停：空格键
- 导出为图片：Ctrl+S 组合键