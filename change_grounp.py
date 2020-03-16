import time
import shutil

import cv2
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip


def extract(videopath, index=1):
    video = cv2.VideoCapture()
    if not video.open(videopath):
        print("can not open the video")
        exit(1)
    while True:
        _, frame = video.read()
        if frame is None:
            break
        index += 1
    video.release()
    print("Totally save {:d} pics".format(index - 1))
    a = index - 1
    return a


def copy_photo(photo_path, n):
    img = cv2.imread(photo_path, cv2.IMREAD_COLOR)
    a_list = photo_path.split('.', 1)[0]
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


def add_zm(fg_in_bg_avi, zm_video_path, i, video_name, output):
    clip1 = VideoFileClip(fg_in_bg_avi)
    clip3 = VideoFileClip(zm_video_path, has_mask=True)
    video = CompositeVideoClip([clip1, clip3])
    try:
        os.mkdir(output)
    except OSError:
        pass
    video_name = video_name.split('/', 2)[-1]
    name = output + '/' + i + video_name + ".mp4"
    video.write_videofile(name, audio=True)  # 先不加音频
    video.close()
    return name


def run(pictrue_path, mova, output):
    start = time.clock()
    pictrue_path = pictrue_path
    mova = mova
    n = extract(mova)

    bg_list = os.listdir(pictrue_path)

    for _ in bg_list:
        for_mat = _.split('.', 1)[-1]
        pictrue_name = _.split('.', 1)[0]
        video_name = mova.split('.', 1)[0]

        name1 = pictrue_path + '/' + _
        if for_mat == 'png' or for_mat == 'jpg':
            path_photo = copy_photo(name1, n)

            video = become_video(path_photo, mova)

            name = add_zm(mova.split('.', 1)[0] + 'out.avi', mova, pictrue_name, video_name, output)

            shutil.rmtree(path_photo)
            os.remove(mova.split('.', 1)[0] + 'out.avi')  # 中间产物
            print("处理完成" + name)
        else:
            # 如果背景里面有视频
            pass

    end = time.clock()

    print('总共耗时: %s 分钟' % ((end - start) % 60))


def sort_list(unlist):
    mov_list = []
    file_list = []
    for _ in unlist:
        if ".mov" in _:
            mov_list.append(_)
        else:
            file_list.append(_)
    sorted_list = file_list + mov_list
    return sorted_list


if __name__ == '__main__':

    for parent, dirnames, filename in os.walk("data"):

        for dirname in dirnames:
            print("开始处理文件夹:", dirname)
            dirname_path = "data/" + dirname
            file_name = os.listdir(dirname_path)

            # todo 将乱序的列表分成两个列表
            file_name = sort_list(file_name)

            timeout = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            output = timeout + "output"
            pictrue_path = dirname_path + "/" + file_name[0]

            for j in range(len(file_name) - 1):
                # print(j)
                mova = dirname_path + "/" + file_name[j + 1]
                run(pictrue_path=pictrue_path, mova=mova, output=output)
        break
    print("全部完成")
