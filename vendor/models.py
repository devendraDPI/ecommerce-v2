from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification_email
from datetime import time, date, datetime


DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]


TIME = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p'))
        for h in range(24) for m in (0, 30)]


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

    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        today_operating_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        is_open_ = None
        for i in today_operating_hours:
            if not i.is_closed:
                start_time = str(datetime.strptime(i.from_hour, '%I:%M %p').time())
                end_time = str(datetime.strptime(i.to_hour, '%I:%M %p').time())
                is_open_ = start_time < current_time < end_time
        return is_open_

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


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=TIME, max_length=16, blank=True)
    to_hour = models.CharField(choices=TIME, max_length=16, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()
