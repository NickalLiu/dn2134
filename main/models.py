# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=30)