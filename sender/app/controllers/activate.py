import sendgrid

import config


channel = "activate"

mail_template = "4fc98bc0-7187-49f4-9bd1-7b18d105577b"

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
        mail.add_filter("templates", "enable", "1")
        mail.add_filter("templates", "template_id", mail_template)
        mail.add_substitution(":url", activate_url + user_token)
        mail.set_html(activate_url + user_token)
        status = mailClient.send(mail)

        print(status)

    except Exception as e:
        print(e)

