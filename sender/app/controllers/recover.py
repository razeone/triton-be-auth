import sendgrid

import config


channel = "recover"

subject = "Recover user password"
user_from = "recover@triton.dev"
recover_url = "http://" + config.HOSTNAME + "/user/#/reset/"

mailClient = sendgrid.SendGridClient(config.MAIL_KEY)


def handle_message(content):

    try:

        user_to = content["mail"]
        user_token = content["token"]

        mail = sendgrid.Mail()
        mail.add_to(user_to)
        mail.set_from(user_from)
        mail.set_subject(subject)
        mail.set_html(recover_url + user_token)
        mailClient.send(mail)

    except Exception as e:
        print(e)

