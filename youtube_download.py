
from requests_html import HTMLSession
import pytube 
from pytube.cli import on_progress 

def download(url):
    yt = pytube.YouTube(url, on_progress_callback=on_progress) 
    print(yt.streams) 
    save_dir = "./downloads" 
    yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(save_dir)


    
if __name__=='__main__':
    if 1:
        s = HTMLSession()
        urls = ['https://youtube.com/playlist?list=PLWo1h5t1i9PHtpcwXa04EWQri_ZZeTFGY',
        'https://youtube.com/playlist?list=PLuba0X9cgD2cM6o5yl4thoQQuhP862v_l',
        'https://youtube.com/playlist?list=PLdm8N0POyDI4Vlb3bKlKu5q9ba1VDn0m7',
        'https://youtube.com/playlist?list=PLNW3_Pxm06W6GBVvtSGTF8qPz09fjNtmP',
        'https://youtube.com/channel/UCpn5KH6S-9rGcy1EAWxjLTQ/videos'
        ]
      
        total=0
        for url in urls:
            r = s.get(url)
            r.html.render(sleep=0, keep_page = True, scrolldown = 1000)
            length= len(r.html.find('a#video-title'))
            total+=length
            for links in r.html.find('a#video-title'):
                link = next(iter(links.absolute_links))
                download(link)
        print(fr' number of videos:{total}')

    else:
        download('https://youtu.be/MMeHulqHvLo')

   


