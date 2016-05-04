import sendgrid

import config


channel = "recover"

mail_template = "7016339e-6067-4464-86a1-5180c3eb3724"

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
        mail.add_filter("templates", "enable", "1")
        mail.add_filter("templates", "template_id", mail_template)
        mail.add_substitution(":url", recover_url + user_token)
        mail.set_html(recover_url + user_token)
        status = mailClient.send(mail)

        print(status)

    except Exception as e:
        print(e)

