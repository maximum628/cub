import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
import mongoengine

from cub.settings import CONTACT_ADMINS, EMAIL_HOST_USER, BASE_DIR
from backend.models.abstract import AbstractJSONDocument

class Contact(AbstractJSONDocument):

    meta = {
        'indexes': [{'fields': ['email']}]
    }

    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    content = mongoengine.StringField(required=True)
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def send_email(cls, sender, document, **kwargs):
        msg_html = render_to_string(
            '%s/backend/templates/email/contact/notify_team.html' % BASE_DIR,
            {'document': document})

        send_mail(
            subject='CUB - Feedback received',
            message='New Feedback was received.',
            html_message=msg_html,
            from_email='Connect Hub - CUB <%s>' % EMAIL_HOST_USER,
            recipient_list=CONTACT_ADMINS,
            fail_silently=True)


        msg_html = render_to_string(
            '%s/backend/templates/email/contact/confirm_user.html' % BASE_DIR,
            {'document': document})

        send_mail(
            subject='CUB - Feedback sent',
            message='We confirm we received your feedback message.',
            html_message=msg_html,
            from_email='Connect Hub - CUB <%s>' % EMAIL_HOST_USER,
            recipient_list=[document.email],
            fail_silently=True)

mongoengine.signals.post_save.connect(Contact.send_email, sender=Contact)
