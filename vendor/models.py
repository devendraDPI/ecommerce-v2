from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification_email


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=256, unique=True)
    license = models.ImageField(upload_to='vendor/license')
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            state = Vendor.objects.get(pk=self.pk)
            if state.is_approved != self.is_approved:
                mail_template = 'account/email/admin-approval-email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    mail_subject = "Congratulations! Your shop has been approved"
                    send_notification_email(mail_subject, mail_template, context)
                else:
                    mail_subject = "We're sorry! Your shop is not eligible"
                    send_notification_email(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
