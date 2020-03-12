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
