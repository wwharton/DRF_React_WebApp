# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WsbMeta(models.Model):
    index = models.IntegerField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    bears = models.IntegerField(blank=True, null=True)
    bulls = models.IntegerField(blank=True, null=True)
    boomers = models.IntegerField(blank=True, null=True)
    primaryk = models.AutoField(db_column='PK', unique=True, blank=True, null=False, primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WSB_meta'

