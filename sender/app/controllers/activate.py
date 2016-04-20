import sendgrid

import config


channel = "activate"

subject = "Activate user account"
user_from = "activate@triton.dev"
activate_url = "http://" + config.HOSTNAME + "/v1/auth/activate/"

mailClient = sendgrid.SendGridClient(config.MAIL_KEY)


def handle_message(content):

    try:

        user_to = content["mail"]
        user_token = content["token"]

        mail = sendgrid.Mail()
        mail.add_to(user_to)
        mail.set_from(user_from)
        mail.set_subject(subject)
        mail.set_html(activate_url + user_token)
        mailClient.send(mail)

    except Exception as e:
        print(e)

