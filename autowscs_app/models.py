from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Careerpath(models.Model):
    careerpathid    = models.CharField(db_column='careerPathID', primary_key=True, max_length=4)  # Field name made lowercase.
    careerpathname  = models.CharField(db_column='careerPathName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'careerpath'


class Webservicelist(models.Model):
    webserviceid    = models.CharField(db_column='webServiceID', primary_key=True, max_length=10)  # Field name made lowercase.
    name            = models.CharField(db_column='webServiceName',max_length=100, blank=True, null=True)
    reputation      = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    price           = models.FloatField(blank=True, null=True)
    duration        = models.IntegerField(blank=True, null=True)
    provider        = models.CharField(max_length=50, blank=True, null=True)
    url             = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'webservicelist'


class Initialgoalparameter(models.Model):
    transactionid = models.BigIntegerField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    iorg = models.CharField(max_length=10)
    parameterid = models.ForeignKey('Parameterlist', models.DO_NOTHING, db_column='parameterID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'initialgoalparameter'
        unique_together = (('transactionid', 'iorg', 'parameterid'),)


# class Knowledgeforcareerpath(models.Model):
#     careerpathid = models.ForeignKey(Careerpath, models.DO_NOTHING, db_column='careerPathID', primary_key=True)  # Field name made lowercase.
#     knowledgeid = models.ForeignKey('Knowledgelist', models.DO_NOTHING, db_column='knowledgeID')  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'knowledgeforcareerpath'
#         unique_together = (('careerpathid', 'knowledgeid'),)


class Parameterlist(models.Model):
    parameterid = models.CharField(db_column='parameterID', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='parameterName', max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'parameterlist'


# class Lhs(models.Model):
#     ruleid = models.IntegerField(primary_key=True)
#     courseid = models.CharField(max_length=10)

#     class Meta:
#         managed = False
#         db_table = 'lhs'
#         unique_together = (('ruleid', 'courseid'),)


class Inputparameter(models.Model):
    webserviceid    = models.ForeignKey(Webservicelist, models.DO_NOTHING, db_column='webServiceID', primary_key=True)  # Field name made lowercase.
    parameterid     = models.ForeignKey(Parameterlist, models.DO_NOTHING, db_column='parameterID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'inputparameter'
        unique_together = (('webserviceid', 'parameterid'),)


class Outputparameter(models.Model):
    webserviceid = models.ForeignKey(Webservicelist, models.DO_NOTHING, db_column='webServiceID', primary_key=True)  # Field name made lowercase.
    parameterid = models.ForeignKey(Parameterlist, models.DO_NOTHING, db_column='parameterID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'outputparameter'
        unique_together = (('webserviceid', 'parameterid'),)

class Result(models.Model):
    transactionid = models.BigIntegerField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    stage = models.IntegerField()
    webserviceid = models.BigIntegerField(db_column='webServiceID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'result'
        unique_together = (('transactionid', 'stage', 'webserviceid'),)


# class Rhs(models.Model):
#     ruleid = models.IntegerField(primary_key=True)
#     courseid = models.CharField(max_length=10)

#     class Meta:
#         managed = False
#         db_table = 'rhs'
#         unique_together = (('ruleid', 'courseid'),)


class Ruleinfo(models.Model):
    ruleid = models.IntegerField(primary_key=True)
    support = models.FloatField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    lift = models.FloatField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ruleinfo'


class ParameterHierarchy(models.Model):
    parentParameterID   = models.CharField(max_length=10, db_column='parentParameterID')
    childParameterID    = models.CharField(max_length=10, db_column='childParameterID')  # Field name made lowercase.
    noOfDepth           = models.IntegerField(db_column='noOfDepth')
    noOfChildren        = models.IntegerField(db_column='noOfChildren')


    class Meta:
        managed = True
        db_table = 'parameterhierarchy'
