import requests

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_notification(self, emails):
        for email in emails:
            message_id = email['message_id']
            subject = email['subject']
            body = email['body']
            from_email = email['from_email']
            # message = f"MessageId: {message_id}\nFrom: {from_email}\nSubject: {subject}\nBody: {body}"
            # payload = {
            #     "text": message
            # }

            # Slackのブロックキットを使用してメッセージを構築
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓*\n*From:* {from_email}\n*Subject:* {subject}\n*Message ID:* {message_id}"
                    }
                }
            ]

            # bodyの中の<br />を削除
            body = body.replace('<br />', '')

            body_split = []
            # bodyを3000文字ごとに分割
            for i in range(0, len(body), 3000):
                body_split.append(body[i:i + 3000])

            for i, body in enumerate(body_split):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{body}"
                    }
                })

            payload = {
                "blocks": blocks
            }

            response = requests.post(self.webhook_url, json=payload)
            if response.status_code != 200:
                raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
