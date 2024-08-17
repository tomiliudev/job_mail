import imaplib
import email
from email.header import decode_header

class YahooMail:
    IMAP_SERVER = 'imap.mail.yahoo.co.jp'

    def __init__(self, email_account, password):
        self.email_account = email_account
        self.password = password

    def get_subject(self, email_message):
        subject = email_message['subject']
        if subject:
            decoded_header = decode_header(subject)[0]
            subject = decoded_header[0].decode(decoded_header[1]) if isinstance(decoded_header[0], bytes) else decoded_header[0]
        else:
            subject = None
        return subject

    def get_body(self, email_message):
        body = ''
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == 'text/plain' or content_type == 'text/html':
                    try:
                        body = part.get_payload(decode=True).decode()
                        break  # 最初に見つかった本文を使用
                    except Exception as e:
                        print(f'Error decoding part: {e}')
        else:
            content_type = email_message.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                try:
                    body = email_message.get_payload(decode=True).decode()
                except Exception as e:
                    print(f'Error decoding message: {e}')
        return body

    def search_yahoo_mail(self, domain):
        try:
            with imaplib.IMAP4_SSL(self.IMAP_SERVER) as client:
                client.login(self.email_account, self.password)
                client.select('inbox')

                # 検索条件: from:domain、未読メール、受信日時が2024年8月1日以降
                status, messages = client.search(None, f'FROM "@{domain}" UNSEEN SINCE 01-Aug-2024')

                # メールが見つかった場合、件名と本文を取得し一つの構造体に格納する
                emails = []
                if status == 'OK':
                    for num in messages[0].split():
                        status, data = client.fetch(num, '(RFC822)')
                        if status == 'OK':
                            email_message = email.message_from_bytes(data[0][1])

                            # メッセージIDを取得
                            message_id = email_message['Message-ID']

                            # 件名を取得
                            subject = self.get_subject(email_message)

                            # 本文を取得
                            body = self.get_body(email_message)

                            # 送信者のメールアドレスを取得
                            from_email = email.utils.parseaddr(email_message['From'])[1]

                            # 件名と本文を辞書に格納
                            email_data = {
                                'message_id': message_id,
                                'subject': subject,
                                'body': body,
                                'from_email': from_email
                            }
                            emails.append(email_data)
                    return emails

                return None  # メールが見つからない場合
        except imaplib.IMAP4.error as e:
            print(f'IMAP error: {e}')
            return None
