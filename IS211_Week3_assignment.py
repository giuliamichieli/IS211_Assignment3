import sys, argparse, os
from urllib.request import urlopen
import csv
from datetime import *
import re
import operator

def downloadData(url):
    file_name = 'data.csv'
    f = open('data.csv','wb')
    header = 'req_file,datetime,browser,req_status,req_size\n'.encode('utf-8')
    f.write(header)
    response = urlopen(url).read().decode('utf-8')
    f.write(response.encode('utf-8'))
    f.close()
    return file_name
    """
    response = urlopen(url).read().decode('utf-8')
    file_name = 'data.csv'
    open(file_name, 'wb').write(response.encode('utf-8'))
    return file_name
    """

def processData(data):
    source = open(data)
    data = csv.DictReader(source)
    images = {}
    image = re.compile('((i?)(jpg|gif|png)$)', flags=re.IGNORECASE)
    browsers = {}
    browser = re.compile('((i?)(MSIE|chrome|firefox|safari))', flags=re.IGNORECASE)
    not_image = 0
    hours = dict.fromkeys([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 0)
    for row in data:

        try: # see if hit was image
            image_found = image.search(row['req_file']).group().lower()
            if not image_found in images: images[image_found] = 1
            else: images[image_found] += 1
        except:
            not_image += 1 #means requested file was not an image

        browser_found = browser.search(row['browser']).group().lower() # get browser used for hit
        if not browser_found in browsers: browsers[browser_found] = 1
        else: browsers[browser_found] += 1

        hit_timestamp_str = row['datetime'] # get hour of hit
        hit_hour = (datetime.strptime(hit_timestamp_str, '%Y-%m-%d %H:%M:%S')).hour
        hours[hit_hour] += 1
        desc_hours = dict(sorted(hours.items(), key=operator.itemgetter(1),reverse=True))

    #print (images)
    #print (browsers)
    #print (hours)

    total_images = sum(images.values())
    img_perc = (total_images/(total_images + not_image) * 100)
    print ('\nImage requests account for %2.2f %% of all requests \n' % img_perc)

    most_used_browser = str(max(browsers, key=browsers.get))
    print ('Most used browser is %s \n' % most_used_browser)

    for h in desc_hours:
        print ("Hour %s has %d hits" % (str(h).zfill(2),desc_hours[h]))
    

def main(url):
    try:
        csvData = downloadData(url)
    except Exception as e:
        print ("Exception occured downloading file: ", e)
        sys.exit()
    processData(csvData)
    os.remove(csvData)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--url",dest="url",nargs=1, help='URL Required. Usage: python IS211_Week3_assignment.py --url URL_FOR_DATA')
    args = parser.parse_args()
    url=args.url[0]
    if url.find('http://') < 0: url = 'http://' + url
    main(url)