### Ubuntu环境使用python给具有透明通道的视频大量替换不同背景

​		前言：虽然用pr视频处理软件也能一个个为具有透明通道的视频替换不同的背景，但是如果要人工替换一百个一千个这个的视频，显然是让人奔溃的操作。本文记录如何在Ubuntu环境使用python给具有透明通道的视频大量替换不同背景，主要记录环境的配置和项目的使用用法。

#### 一、环境配置

##### 1.1 下载代码

​		脚本代码已经提交到GitHub上面，仓库地址为：https://github.com/huangjunxiong11/change_grounp1.1.0.git

​		脚本代码也粘贴在下面

```
import time
import shutil

import cv2
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

EXTRACT_FREQUENCY = 1


def extract(videopath, index=EXTRACT_FREQUENCY):
    video = cv2.VideoCapture()
    if not video.open(videopath):
        print("can not open the video")
        exit(1)
    count = 1
    while True:
        _, frame = video.read()
        if frame is None:
            break
        if count % EXTRACT_FREQUENCY == 0:
            index += 1
        count += 1
    video.release()
    print("Totally save {:d} pics".format(index - 1))
    a = index - 1
    return a


def copy_photo(photo_path, n):
    img = cv2.imread(photo_path, cv2.IMREAD_COLOR)
    path_photo = photo_path.split('.', 1)[0]

    try:
        os.mkdir(path_photo)
    except OSError:
        pass
    for i in range(n):
        name = path_photo + '/' + (str(i)).zfill(4) + '.png'
        cv2.imwrite(name, img)
    return path_photo


def become_video(fg_in_bg, name1):
    cap = cv2.VideoCapture(name1)
    fgs = int(cap.get(cv2.CAP_PROP_FPS))
    pictrue_in_filelist = os.listdir(fg_in_bg)
    pictrue_in_filelist.sort(key=lambda x: int(x[:-4]))
    name = fg_in_bg + "/" + pictrue_in_filelist[0]
    img = cv2.imread(name)
    h, w, c = img.shape
    size = (w, h)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_video = name1.split('.', 1)[0] + 'out.avi'
    video_writer = cv2.VideoWriter(out_video, fourcc, fgs, size)

    for i in range(len(pictrue_in_filelist)):
        pictrue_in_filename = fg_in_bg + "/" + pictrue_in_filelist[i]
        img12 = cv2.imread(pictrue_in_filename)
        video_writer.write(img12)
    video_writer.release()
    return out_video


def add_zm(fg_in_bg_avi, zm_video_path, i):
    clip1 = VideoFileClip(fg_in_bg_avi)
    clip3 = VideoFileClip(zm_video_path, has_mask=True)
    video = CompositeVideoClip([clip1, clip3])
    try:
        os.mkdir("out")
    except OSError:
        pass

    out_name = "out/" + zm_video_path.split('.', 1)[0] + "out"

    name = out_name + i + ".mp4"
    video.write_videofile(name, audio=True)  # 先不加音频
    video.close()
    return name


if __name__ == '__main__':

    start = time.clock()

    mova = 'youheng.mov'
    pictrue_path = "input"
    n = extract(mova)

    bg_list = os.listdir(pictrue_path)

    bg_list.sort(key=lambda x: int(x[2:-4]))

    for _ in bg_list:
        for_mat = _.split('.', 1)[-1]
        for_name = _.split('.', 1)[0]

        print("开始处理" + for_name)

        name1 = pictrue_path + '/' + _
        if for_mat == 'png' or for_mat == 'jpg':
            path_photo = copy_photo(name1, n)

            video = become_video(path_photo, mova)

            name = add_zm(mova.split('.', 1)[0] + 'out.avi', mova, for_name)

            shutil.rmtree(path_photo)
            os.remove(mova.split('.', 1)[0] + 'out.avi')  # 中间产物
            print("完成" + name)
        else:
            # 如果背景里面有视频
            pass

    end = time.clock()

    print('Running time: %s Seconds' % (end - start))

```



##### 1.2 创建虚拟环境并安装工具包

​		为了不影响不同项目之间工具包的使用，所以需要创建一个虚拟环境。在Ubuntu中，本人推荐使用anaconda的conda命令来创建。terminal命令为：

```
conda create -n envname python=3.6  # 创建python3.6版本名字为envname的虚拟环境
```

​		第二步进入虚拟环境，并且安装项目所需运行工具包

```
conda activate envname  # 进入虚拟环境
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  # 使用pip在清华镜像源下载安装工具包
```

#### 二、项目的使用方法

##### 2.1 资料准备

​		第一步，将具有透明通道的视频放到与脚本文件change_grounp.py的同级目录下，保证透明通道视频的格式是mov格式；第二步，将背景图片放到与change_grounp.py文件的同级目录input文件夹下，并保证图片的尺寸宽高大小与视频一样。

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

