from telegram import Update, message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, MessageHandler, Filters
import requests
from time import sleep
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import os 
import glob

updater = Updater('5091364544:AAHeU-lM-mIqnCudchdaEAzmVEYfutLU14c')

# Hàm này để kiểm tra độ giống nhau giữa 2 chuỗi
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Hàm này để kiểm tra độ giống nhau giữa sub và tên
def similar_sub(a,b):
    diem = 0
    a = a.lower()
    b = b.lower()
    if "1080" in a and "1080" in b:
        diem += 0.5
    elif "720" in a and "720" in b:
        diem += 0.5
    elif "360" in a and "360" in b:
        diem += 0.5
    elif "2160" in a and "2160"in b:
        diem += 0.5
    pass

    if "webrip" in a and "webrip" in b:
        diem += 1
    elif "webdl" in a and "webdl" in b:
        diem += 1
    elif "web" in a and "web" in b:
        diem += 0.5
    else:
        pass

    if "hdrip" in a and "hdrip" in b:
        diem += 1
    elif "hdts" in a and "hdts" in b:
        diem += 1
    elif "hdtc" in a and "hdtc" in b:
        diem += 1
    elif "hd" in a and "hd" in b:
        diem += 0.5
    else:
        pass 

    if "bluray" in a and "bluray" in b:
        diem += 1
    if "cam" in a and "cam" in b:
        diem += 1
    if "brrip" in a and "brrip" in b:
        diem += 1
    if "nf" in a and "nf" in b:
        diem += 1
    
    for i in range(1,100):
        if i < 10:
            if f"e0{i}" in a and f"e0{i}" in b:
                diem += 2
            if f"s0{i}" in a and f"s0{i}" in b:
                diem += 2
        else:
            if f"e{i}" in a and f"e{i}" in b:
                diem += 2
            if f"s{i}" in a and f"s{i}" in b:
                diem += 2
    return diem
# Hàm này để xóa phần tử trung trong arr
def xoa_phan_tu_trung_trong_arr(arr):
    arr = list(dict.fromkeys(arr))
    return arr
# Hàm này để kiểm tra các phần tử trong tên của 2 chuỗi có trùng nhau không
def similar_title(a,b):
    arr_a = a.lower().split(" ")
    arr_b = b.lower().split(" ")
    xoa_phan_tu_trung_trong_arr(arr_a)
    xoa_phan_tu_trung_trong_arr(arr_b)
    diem = 0
    for i in arr_a:
        for j in arr_b:
            if i == j:
                diem += 1
    return diem
# Hàm này để xóa các kí tự đặc biệt
def xu_ly_chuoi(a_string):
    alphanumeric = ""
    for character in a_string:
        #  Thay xóa toàn bộ kí tự đặc biệt trừ dấu cách
        if character == " " or character == ".":
            alphanumeric += " "
            continue
        if character == "'":
            alphanumeric += "'"
            continue
        if character.isalnum():
            alphanumeric += character
    #  xóa hết những dấu cách thừa
    while True:
        if alphanumeric.find("  ") != -1:
            alphanumeric = alphanumeric.replace("  "," ")
        else:
            break

    return alphanumeric
# Hàm này để ngắt bỏ chất lượng, tập, năm
def ngat_bo(name):
    # Ngắt bỏ chất lượng trở về sau
    if name.lower().find("1080p") != -1:
        name_seach = name[:name.lower().find("1080p")]
    elif name.lower().find("2160p") != -1:
        name_seach = name[:name.lower().find("2160p")]
    elif name.lower().find("720p") != -1:
        name_seach = name[:name.lower().find("720")]
    elif name.lower().find("360p") != -1:
        name_seach = name[:name.lower().find("360")]
    elif name.lower().find("webrip") != -1:
        name_seach = name[:name.lower().find("webrip")]
    elif name.lower().find("web-dl") != -1:
        name_seach = name[:name.lower().find("web-dl")]
    elif name.lower().find("web-hd") != -1:
        name_seach = name[:name.lower().find("web-hd")]
    elif name.lower().find("bluray") != -1:
        name_seach = name[:name.find("bluray")]
    else:
        name_seach = name

    # Ngắt bỏ năm trở về sau
    numbers = []
    # Lấy số trong string và xuất ra mảng
    for word in name_seach.split(" "):
        if word.isdigit():
            numbers.append(int(word))
    # Ngắt bỏ từ phần năm 1900 -> 2100 trở về sau. Lấy phần trước
    for i in numbers:
        for j in range(1900,2100):
            if i == j:
                name_seach = name_seach[:name_seach.find(str(i))]
                break
    # Ngắt bỏ mùa và tập
    if name_seach.lower().find("s0") != -1:
        name_seach = name_seach[:name_seach.lower().find("s0")]
    elif name_seach.lower().find("s1") != -1:
        name_seach = name_seach[:name_seach.lower().find("s1")]
    elif name_seach.lower().find("s2") != -1:
        name_seach = name_seach[:name_seach.lower().find("s2")]
    elif name_seach.lower().find("s3") != -1:
        name_seach = name_seach[:name_seach.lower().find("s3")]
    elif name_seach.lower().find("s4") != -1:
        name_seach = name_seach[:name_seach.lower().find("s4")]
    elif name_seach.lower().find("s5") != -1:
        name_seach = name_seach[:name_seach.lower().find("s5")]
    elif name_seach.lower().find("s6") != -1:
        name_seach = name_seach[:name_seach.lower().find("s6")]
    elif name_seach.lower().find("s7") != -1:
        name_seach = name_seach[:name_seach.lower().find("s7")]
    else:
        pass

    if name_seach.lower().find("e0") != -1:
        name_seach = name_seach[:name_seach.lower().find("e0")]
    elif name_seach.lower().find("e1") != -1:
        name_seach = name_seach[:name_seach.lower().find("e1")]
    elif name_seach.lower().find("e2") != -1:
        name_seach = name_seach[:name_seach.lower().find("e2")]
    elif name_seach.lower().find("e3") != -1:
        name_seach = name_seach[:name_seach.lower().find("e3")]
    elif name_seach.lower().find("e4") != -1:
        name_seach = name_seach[:name_seach.lower().find("e4")]
    elif name_seach.lower().find("e5") != -1:
        name_seach = name_seach[:name_seach.lower().find("e5")]
    elif name_seach.lower().find("e6") != -1:
        name_seach = name_seach[:name_seach.lower().find("e6")]
    elif name_seach.lower().find("e7") != -1:
        name_seach = name_seach[:name_seach.lower().find("e7")]
    elif name_seach.lower().find("e8") != -1:
        name_seach = name_seach[:name_seach.lower().find("e8")]
    elif name_seach.lower().find("e9") != -1:
        name_seach = name_seach[:name_seach.lower().find("e9")]
    else:
        pass

    return name_seach
# Hàm này để seach và lấy dữ liệu từ subscence rồi sắp xếp
def subscene_seach_title(name,update,context):
    dictionnary_title_subscene = []
    name_seach = xu_ly_chuoi(name)
    name_seach = ngat_bo(name_seach)
    name_seach = name_seach.strip()
    update.message.reply_text(name_seach + " Seaching...")
    try:
        html = requests.post("https://subscene.com/subtitles/searchbytitle", data={'query' : name_seach})
        text = BeautifulSoup(html.text,'html.parser')
        body_text = text.find('body')
        list_title = body_text.find('div',{"id" : "content"}).findAll('li')
        # Add vào mảng
        for element in list_title:
            try:
                subtle_count = element.find('div',{"class" : "subtle count"}).text
            except:
                subtle_count = element.find('span',{"class" : "subtle count"}).text
            name_of_title = element.find('div',{"class" : "title"}).text.strip()
            temp = {
            "name" : name_of_title,
            "subtle count" : int(subtle_count.replace("\r\n\r\n\t\t","")[:subtle_count.replace("\r\n\r\n\t\t","").find(" subtitles")]),
            "link" : ("https://subscene.com" + element.find('div',{"class" : "title"}).a.get("href")),
            "similar" : similar_title(name_seach,xu_ly_chuoi(name_of_title)) + similar_title(xu_ly_chuoi(name),xu_ly_chuoi(name_of_title)) + similar(xu_ly_chuoi(name).replace(" ","").lower(),xu_ly_chuoi(name_of_title).replace(" ","").lower())
            }
            dictionnary_title_subscene.append(temp)
        
        # Sắp xếp để tìm kiếm tỷ mỷ

        if dictionnary_title_subscene == [] :
            update.message.reply_text("❌ Không tìm thấy chủ đề")
            return
        max_arr = []
        min_arr = []
        # Chia ra 2 mảng, 1 mảng có số lượng bản sub > 40, và 1 mảng số sub <= 60
        # Sau đó sắp sếp từng phần tử trong mỗi mảng rồi gộp lại
        for element in dictionnary_title_subscene:
            if element["subtle count"] > 40:
                max_arr.append(element)
            else:
                min_arr.append(element)

        dictionnary_title_subscene = []

        if len(max_arr) >= 2:
            for i in range(len(max_arr)):
                for j in range(len(max_arr)):
                    if max_arr[i]["similar"] > max_arr[j]["similar"]:
                        temp = max_arr[i]
                        max_arr[i] = max_arr[j]
                        max_arr[j] = temp
            for k in max_arr:
                dictionnary_title_subscene.append(k)
        elif len(max_arr) == 1:
            dictionnary_title_subscene.append(max_arr[0])

        if len(min_arr) >= 2:
            for i in range(len(min_arr)):
                for j in range(len(min_arr)):
                    if min_arr[i]["similar"] > min_arr[j]["similar"]:
                        temp = min_arr[i]
                        min_arr[i] = min_arr[j]
                        min_arr[j] = temp
            for k in min_arr:
                dictionnary_title_subscene.append(k)
        elif len(min_arr) == 1:
            dictionnary_title_subscene.append(min_arr[0])
        return dictionnary_title_subscene
    except:
        update.message.reply_text("❌ Không tìm thấy chủ đề")

def subscene_seach_sub(link,name,update,context):
    try:
        html = requests.get(link + "/vietnamese")
        text = BeautifulSoup(html.text,'html.parser')
        tbody_text = text.find('tbody')
        arr_list_sub = tbody_text.findAll('tr')
        # add sub việt vào mảng
        dictionnary_sub_subscene = []
        print(arr_list_sub)
        for element in arr_list_sub:
            try:
                name_of_sub = element.find("td", {"class" : "a1"}).a.text.replace("\n\r\n\t\t\t\t\t\tVietnamese\r\n\t\t\t\t\t\n\r\n\t\t\t\t\t\t","").replace(" \r\n\t\t\t\t\t\n","")
                temp = {
                "name" : name_of_sub,
                "link" : ("https://subscene.com" + element.find("td", {"class" : "a1"}).a.get("href")),
                "uploader" : element.find("td", {"class" : "a5"}).a.text.replace("\r\n\t\t\t\t","").replace("\r\n\t\t\t",""),
                "comment" : element.find("td", {"class" : "a6"}).text.replace("\n\r\n","").replace("\xa0\t\t\t\t\n",""),
                "similar" : similar(xu_ly_chuoi(name),xu_ly_chuoi(name_of_sub)) + similar_sub(xu_ly_chuoi(name),xu_ly_chuoi(name_of_sub))
                }
                check_trung = False
                for one in dictionnary_sub_subscene:
                    if one["name"] == temp["name"] and one["uploader"] == temp["uploader"]:
                        check_trung = True
                if check_trung == False:
                    dictionnary_sub_subscene.append(temp)
            except:
                pass
            
        
        #sắp xếp theo smilar
        for i in range(len(dictionnary_sub_subscene)):
            for j in range(len(dictionnary_sub_subscene)):
                if dictionnary_sub_subscene[i]["similar"] > dictionnary_sub_subscene[j]["similar"]:
                    temp = dictionnary_sub_subscene[i]
                    dictionnary_sub_subscene[i] = dictionnary_sub_subscene[j]
                    dictionnary_sub_subscene[j] = temp

        return dictionnary_sub_subscene
    except:
        update.message.reply_text("❌ Không tìm thấy bản sub Tiếng Việt")

def subscene_download(link,update,context):
    try:
        html = requests.get(link)
        text = BeautifulSoup(html.text,'html.parser')
        body_text = text.find('body')
        try:
            link_download = "https://subscene.com" + body_text.find('a',{"class" : "button positive"}).get("href")
        except:
            link_download = "https://subscene.com" + body_text.find('div',{"class" : "download"}).a.get("href")
        return link_download
    except:
        update.message.reply_text('❌ Không tìm thấy link download')

def send_file(link,update,context):
    try:
        os.system("cd sub && wget --timeout=10 -O temp.zip {0} && unzip temp.zip && rm temp.zip".format(link))
        list = glob.glob("sub/*")
        for i in list:
            os.system('curl -v -F "chat_id=-749568985" -F document=@"{0}" https://api.telegram.org/bot5091364544:AAHeU-lM-mIqnCudchdaEAzmVEYfutLU14c/sendDocument'.format(i))
    except:
        update.message.reply_text("❌ Gửi file không thành công")
    sleep(5)
    os.system('rm sub/*')

def xauchuoi(update,context,start):
    try:
        data = ''
        for i in range(start,len(context.args)):
            data += context.args[i] + " "
        data = data[:len(data)-1]
        return data
    except:
        data = ''
        return data

def quickdownload(update,context):
    try:
        name = xauchuoi(update,context,0)

        dictionnary_title_subscene = subscene_seach_title(name,update,context)
        update.message.reply_text("👉 Tên chủ đề: " + dictionnary_title_subscene[0]["name"] + "\n🔗 Link:" + dictionnary_title_subscene[0]["link"])

        dictionnary_sub_subscene = subscene_seach_sub(dictionnary_title_subscene[0]["link"],name,update,context)
        update.message.reply_text("👉 Tên bản sub: " + dictionnary_sub_subscene[0]["name"] + "\n🔗 Link: " +dictionnary_sub_subscene[0]["link"])

        link_download = subscene_download(dictionnary_sub_subscene[0]["link"],update,context)
        update.message.reply_text("🔗 Link download sub (bản zip chính hãng): " + link_download)

        send_file(link_download,update,context)
    except:
        update.message.reply_text("❌ Download thất bại, vui lòng thử lại")
def currentdownload(update,context):
    name = xauchuoi(update,context,0)
    dictionnary_title_subscene = subscene_seach_title(name,update,context)
    for i in range(len(dictionnary_title_subscene)):
        dictionnary_title_subscene_out = """
📍  Số thứ tự: {0}
✅ Tên chủ đề: {1}
📃 Số bản sub: {2}
✒ Điểm: {6}
🔗 Link: {3}
👉 Lệnh: /gettitle {4} {5}
""".format(i+1,dictionnary_title_subscene[i]["name"],dictionnary_title_subscene[i]["subtle count"],dictionnary_title_subscene[i]["link"],dictionnary_title_subscene[i]["link"],name,dictionnary_title_subscene[i]["similar"])
        update.message.reply_text(dictionnary_title_subscene_out)
        sleep(1.5)
    update.message.reply_text("❗ Số thứ tự càng nhỏ thì tỉ lệ recoment chủ đề đó của chúng tôi càng lớn")

def gettitle(update,context):
    link = context.args[0]
    name = xauchuoi(update,context,1)
    dictionnary_sub_subscene = subscene_seach_sub(link,name,update,context)
    for i in range(len(dictionnary_sub_subscene)):
        dictionnary_sub_subscene_out = """
📍  Số thứ tự: {0}
✅ Tên bản sub: {1}
🔼 Người đăng: {2}
📃 Miêu tả: {3}
🔗 Link: {4}
👉 Lệnh: /getsub {5}
""".format(i+1,dictionnary_sub_subscene[i]["name"],dictionnary_sub_subscene[i]["uploader"],dictionnary_sub_subscene[i]["comment"],dictionnary_sub_subscene[i]["link"],dictionnary_sub_subscene[i]["link"])
        update.message.reply_text(dictionnary_sub_subscene_out)
        sleep(1.5)
    update.message.reply_text("❗ Số thứ tự càng nhỏ thì tỉ lệ recoment bản sắp đó của chúng tôi càng lớn")

def getsub(update,context):
    link = context.args[0]
    link_download = subscene_download(link,update,context)
    update.message.reply_text("🔗 Link download sub (bản zip chính hãng): " + link_download)

    send_file(link_download,update,context)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Hệ thống đang sẵn sàng")


updater.dispatcher.add_handler(CommandHandler('quickdownload', quickdownload))
updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CommandHandler('currentdownload',currentdownload))
updater.dispatcher.add_handler(CommandHandler('gettitle',gettitle))
updater.dispatcher.add_handler(CommandHandler('getsub',getsub))


updater.start_polling()
updater.idle()