from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

class Reviews(models.Model):

  review_id = models.AutoField(max_length=200, primary_key = True)
  review_text = models.TextField(max_length=850, null=True)
  # user = models.OneToOneField(User, on_delete=models.CASCADE)
  to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='to_user', blank=True, null=True)
  brand_name = models.TextField(max_length=250, null=True)
  overall_sentiment = models.TextField(max_length=250, null=True)
  timestamp = models.DateTimeField(default=timezone.now)

class Phrases(models.Model):

  review = models.ForeignKey('reviews.Reviews', default=1, verbose_name="review_id", on_delete=models.SET_DEFAULT, related_name = 'from_review_id')
  phrase_text = models.TextField(max_length=250, null=True)
  sentiment = models.TextField(max_length=250, null=True)
  intention = models.TextField(max_length=350, null=True)
  aspect = models.TextField(max_length=150, null=True)
  
  # to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user', blank=True, null=True)
