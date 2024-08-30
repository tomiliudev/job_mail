from YahooMail import YahooMail
from SlackNotifier import SlackNotifier
import os

def main():
    my_mail = os.getenv('MY_MAIL')
    my_mail_password = os.getenv('MY_MAIL_PASSWORD')
    yahooMail = YahooMail(my_mail, my_mail_password)

    emails = []
    domain_list = ['lassic.co.jp', 'levtech.jp']
    for domain in domain_list:
        emails = yahooMail.search_yahoo_mail(domain)
        if emails:
            emails.extend(emails)

    my_webhook_url = os.getenv('MY_WEBHOOK_URL')
    slack_notifier = SlackNotifier(my_webhook_url)
    slack_notifier.send_notification(emails)

if __name__ == "__main__":
    main()
