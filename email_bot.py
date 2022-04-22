import email
import imaplib
import os
import pymysql.cursors


def connect():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='root',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con

##############################################
def read_file(filename):
     with open(filename, 'rb') as f:
        data_zip = f.read()
     return data_zip

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
    return 'OK'

def file_upload(my_id, filename):
    con = connect()
    data = read_file(filename)
    with con:
        cur = con.cursor()
        try:
            sql = ("""UPDATE status
                      SET soc_zip = %s
                      WHERE id = %s""")
            cur.execute(sql, (data, my_id))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")

def file_download(my_id, filename):
    con = connect()
    with con:
        cur = con.cursor()
        try:
            sql = ("""SELECT soc_zip
                      FROM status
                      WHERE id = %s""")
            cur.execute(sql, (my_id))
            data = cur.fetchone()[0]
            # con.commit()
            write_file(data, filename)
            print("Все нормально")
        except:
            print("Какой то кал")


def mail_reg():
    addr = "sasha.lorens@yandex.ru"  # Отправитель
    password = "LeNoVo_13572468"
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login(addr, password)
    return mail

def find_new_mail(mail):
    mail.list()
    mail.select("inbox")
    mail.select(readonly=False)
    term = u"Ваша прошивка".encode("utf-8")  ######
    mail.literal = term  ######
    result, data = mail.search("utf-8", "SUBJECT")  ###### ЭТО РАБОТАЕТ!!!!!!!!!!!!!!!!!!!!!!!
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    email.utils.parseaddr(email_message['From']) ### от кого имейл, влияет на запись в базу данных
    file_mail_download(email_message)
    mail.store(latest_email_id, '+FLAGS', r'\\DELETED')
    mail.expunge()



def file_mail_download(email_message):
    download_folder = r'C:\Users\sasha\PycharmProjects'
    print(' ')
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        att_path = os.path.join(download_folder, filename)

        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

# 
# download_folder = 'None'
# print(email.utils.parseaddr(email_message['From']))
# file_mail_download(email_message)
# print(email_message['Date'])    #################  Это не нужно в отличае от верхнего, так как нам по сути надо узнать почту и скачать вложение, а потом удалить письмо
# print(email_message['Subject']) #################
# print(email_message['Message-Id'])###############
