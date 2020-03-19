### Ubuntu环境使用python给具有透明通道的视频大量替换不同背景

​		前言：虽然用pr视频处理软件也能一个个为具有透明通道的视频替换不同的背景，但是如果要人工替换一百个一千个这个的视频，显然是让人奔溃的操作。本文记录如何在Ubuntu环境使用python给具有透明通道的视频大量替换不同背景，主要记录环境的配置和项目的使用用法。

#### 一、环境配置

##### 1.1 下载代码

​		脚本代码已经提交到GitHub上面，仓库地址为：https://github.com/huangjunxiong11/change_grounp1.1.0.git



##### 1.2 创建虚拟环境并安装工具包

​		为了不影响不同项目之间工具包的使用，所以需要创建一个虚拟环境。在Ubuntu中，本人推荐使用anaconda的conda命令来创建。terminal命令为：

```shell
conda create -n envname python=3.6  # 创建python3.6版本名字为envname的虚拟环境
```

​		第二步进入虚拟环境，并且安装项目所需运行工具包

```shell
conda activate envname  # 进入虚拟环境
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  opencv-python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  moviepy
# 使用pip在清华镜像源下载安装工具包
```

#### 二、项目的使用方法

##### 2.1 资料准备

​		项目的目录结构示例：

```shell
root@u:~/Projects/git-pro/change_grounp1.1.0# tree
.
├── 2020-03-13output	# 输出成果目录
│   ├── 竖1shu1.mp4
│   ├── 竖1shu2.mp4
│   ├── 竖1shu3.mp4
│   ├── 竖2shu1.mp4
│   ├── 竖2shu2.mp4
│   └── 竖2shu3.mp4
├── change_grounp.py	# 脚本代码
├── data	# 输入数据目录结构
│   ├── 1	# 文件夹1
│   │   ├── input	# input文件夹存放所有背景图片
│   │   │   ├── 竖1.jpg
│   │   │   └── 竖2.jpg
│   │   ├── shu1.mov	# 存放在文件夹1里面的透明背景视频
│   │   └── shu2.mov	# 存放在文件夹1里面的透明背景视频
│   └── 2
│       ├── input
│       │   ├── 竖1.jpg
│       │   └── 竖2.jpg
│       └── shu3.mov
├── LICENSE
├── readme.md
└── requirement.txt

```

​		示例图片和视频可到网盘下载：链接：https://pan.baidu.com/s/1kRvAqtXDPVGfWIRJH6CgvQ 

提取码：srpy 

##### 2.2 运行程序

​		terminal命令如下：

```
python change_grounp.py
```

#### 三、结果展示

|                     背景图片                     |                         透明视频截图                         |                             结果                             |
| :----------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![右1](E:\迅雷下载\模特+背景\背景\右-横\右1.jpg) | ![透明视频截图右横1](C:\Users\huang\Pictures\透明视频截图右横1.png) | ![透明视频截图右横结果1](C:\Users\huang\Pictures\透明视频截图右横结果1.png) |
|                                                  |                                                              |                                                              |

