import time
import shutil

import cv2
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip


def get_n(file_video):
    cap = cv2.VideoCapture(file_video)
    if cap.isOpened():
        FrameNumber = cap.get(7)
        return int(FrameNumber)


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


def add_zm(fg_in_bg_avi, zm_video_path, pictrue_name, video_name, output):
    clip1 = VideoFileClip(fg_in_bg_avi)
    clip3 = VideoFileClip(zm_video_path, has_mask=True)
    video = CompositeVideoClip([clip1, clip3])
    try:
        os.mkdir(output)
    except OSError:
        pass
    video_name = video_name.split('/', 2)[-1]
    name = output + '/' + pictrue_name + video_name + ".mp4"
    video.write_videofile(name, audio=True)  # 先不加音频
    video.close()
    return name


def run(pictrue_path, mova, output, result_list):
    pictrue_path = pictrue_path
    mova = mova
    n = get_n(mova)
    # 删除掉复制的图片文件夹
    bg_list = os.listdir(pictrue_path)
    bg_list, file_name1 = sort_file(bg_list)
    for _ in file_name1:
        rm_name = pictrue_path + "/" + _
        try:
            shutil.rmtree(rm_name)
        except OSError:
            pass

    for _ in bg_list:
        for_mat = _.split('.', 1)[-1]
        pictrue_name = _.split('.', 1)[0]
        video_name = mova.split('.', 1)[0]

        # 判断接下来要处理的视频是不是已经处理完毕了
        v = video_name.split('/', 2)[-1]
        re = pictrue_name + v + ".mp4"
        if re not in result_list:

            name1 = pictrue_path + '/' + _
            if for_mat == 'png' or for_mat == 'jpg':
                path_photo = copy_photo(name1, n)

                video = become_video(path_photo, mova)

                name = add_zm(fg_in_bg_avi=video, zm_video_path=mova,
                              pictrue_name=pictrue_name, video_name=video_name, output=output)

                shutil.rmtree(path_photo)
                os.remove(video)  # 中间产物
                print("处理完成" + name)
            else:
                # 如果背景里面有视频
                pass


def sort_list(unlist):
    mov_list = []
    file_list = []
    avi_list = []

    for _ in unlist:
        if ".mov" in _:
            mov_list.append(_)
        elif '.avi' in _:
            avi_list.append(_)
        else:
            file_list.append(_)
    sorted_list = file_list + mov_list
    return sorted_list, avi_list


def sort_file(unlist):
    jpg_file = []
    file_list = []
    for _ in unlist:
        if "." in _:
            jpg_file.append(_)
        else:
            file_list.append(_)
    return jpg_file, file_list


if __name__ == '__main__':

    start = time.clock()

    timeout = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    output = timeout + "output"

    # 是否有没有生成视频
    try:
        result_list = os.listdir(output)
    except OSError:
        result_list = []
        pass

    for parent, dirnames, filename in os.walk("data"):

        for dirname in dirnames:
            print("开始处理文件夹:", dirname)
            dirname_path = "data/" + dirname
            file_name = os.listdir(dirname_path)

            # 将乱序的列表分成两个列表,并删除avi中间文件
            file_name, avi_name = sort_list(file_name)
            for _ in avi_name:
                rm_avi = dirname_path + "/" + _
                try:
                    os.remove(rm_avi)
                except OSError:
                    pass

            pictrue_path = dirname_path + "/" + file_name[0]

            for j in range(len(file_name) - 1):
                # print(j)
                mova = dirname_path + "/" + file_name[j + 1]
                run(pictrue_path=pictrue_path, mova=mova, output=output, result_list=result_list)
        break
    print("全部完成")
    end = time.clock()
    print('总共耗时: %s 分钟' % ((end - start) / 60))
