import http
from requests_html import HTMLSession
import pytube 
from pytube.cli import on_progress 
import json
import cv2
import os

label = dict()

def isVerticalType(target):
    cap =cv2.VideoCapture(target)
    i=0
    if cap.isOpened():
        ret, frame = cap.read()
        h,w,c = frame.shape
        return True if h/w>1.5 else False


def download(url, id, save_dir="./downloads"):
    yt = pytube.YouTube(url, on_progress_callback=on_progress) 
    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    filepath = stream.download(save_dir,timeout=60,max_retries=10)
    if isVerticalType(filepath):
        label[id]={'path':filepath, 
        'url':link,
        'publish_date':yt.publish_date.isoformat(timespec='microseconds'), 
        'fps':stream.fps,
        'resolution':stream.resolution,
        'duration':'{}s'.format(stream._monostate.duration),
        'bitrate':stream.bitrate,
        'audio_code':stream.audio_codec,
        'filesize':stream.filesize
        }
    else:
        os.remove(filepath)

    
if __name__=='__main__':
    if 1:
        s = HTMLSession()
        urls={'all':['https://youtube.com/playlist?list=PLWo1h5t1i9PHtpcwXa04EWQri_ZZeTFGY',
        'https://youtube.com/playlist?list=PLuba0X9cgD2cM6o5yl4thoQQuhP862v_l',
        'https://youtube.com/playlist?list=PLdm8N0POyDI4Vlb3bKlKu5q9ba1VDn0m7',
        'https://youtube.com/playlist?list=PLNW3_Pxm06W6GBVvtSGTF8qPz09fjNtmP',
        'https://youtube.com/channel/UCpn5KH6S-9rGcy1EAWxjLTQ/videos'
        'https://www.youtube.com/c/%EA%B4%91%EA%B3%A0%EB%AF%B8%ED%95%99feelaboutad/videos',
        'https://www.youtube.com/playlist?list=PLhM6iMzmZ3ZJItTHLtLhef80Ij_yA4o_b'],

        'vertical':['https://www.youtube.com/playlist?list=PLeoS9W7oCJo2_hnWRzaCp_cGRPMxwfjrB',
        'https://www.youtube.com/playlist?list=PLXE_5U9O5x1_zDJxIUkWtYdEIIBSnAlKj',
        'https://www.youtube.com/channel/UCJDpLrc6rkPr3iU_Ts8kUXg/videos',
        'https://www.youtube.com/c/Kloudbeer/videos',
        'https://www.youtube.com/channel/UCJDpLrc6rkPr3iU_Ts8kUXg/videos',
        'https://www.youtube.com/channel/UCNEaMUMVrxlhNo8xXi-UVCQ/videos',
        'https://www.youtube.com/user/loveitmichaa/videos',
        'https://www.youtube.com/channel/UCrtuDhLDDImfGD7rinAlLjQ/videos',
        'https://www.youtube.com/user/my500videos/videos'
        ]
        }
      
        total=0
        i=0
        save_dir = './downloads'
        with open('file_list.txt', 'w') as faillist:
            faillist.write('down load fail list. \n')
            for url in urls['vertical']:
                r = s.get(url)
                r.html.render(sleep=0, keep_page = True, scrolldown = 10)
                length= len(r.html.find('a#video-title'))
                total+=length
                for links in r.html.find('a#video-title'):
                    link = next(iter(links.absolute_links))
                    print('link:{}'.format(link))
                    try:
                        download(link,i,save_dir)
                        i+=1
                        print(fr' number of videos:{i}/{total}')
                    except http.client.IncompleteRead as e:
                        print('fail: {} \n'.format(link))
                        faillist.write('link: {}\n'.format(link))
            print(fr'total videos:{i}/{total}')

        json_object = json.dumps(label, indent = 2)
        with open("videos_info.json", "w") as outfile:
            outfile.write(json_object)

    else:
        download('https://youtu.be/MMeHulqHvLo')

   


