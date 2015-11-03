from __future__ import unicode_literals

from django.db import models


class BallotPosition(models.Model):
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    clean_description = models.TextField(blank=True, null=True)
    last = models.CharField(max_length=255, blank=True, null=True)
    candidateid = models.CharField(max_length=255, blank=True, null=True)
    polid = models.CharField(max_length=255, blank=True, null=True)
    ballotorder = models.CharField(max_length=255, blank=True, null=True)
    polnum = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    seatname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ballotposition'
        ordering = ["seatname", "last"]

    def __unicode__(self):
        if self.clean_name:
            return self.clean_name
        return "%s (%s)" % (self.seatname, self.last)


class Candidate(models.Model):
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    clean_description = models.TextField(blank=True, null=True)
    first = models.CharField(max_length=255, blank=True, null=True)
    last = models.CharField(max_length=255, blank=True, null=True)
    party = models.CharField(max_length=255, blank=True, null=True)
    candidateid = models.CharField(max_length=255, blank=True, null=True)
    polid = models.CharField(max_length=255, blank=True, null=True)
    ballotorder = models.CharField(max_length=255, blank=True, null=True)
    polnum = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidate'
        ordering = ["last", "first"]

    def __unicode__(self):
        if self.clean_name:
            return self.clean_name
        return "%s, %s" % (self.last, self.first)


class Race(models.Model):
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    clean_description = models.TextField(blank=True, null=True)
    accept_ap_calls = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    test = models.BooleanField()
    raceid = models.CharField(max_length=255, blank=True, null=True)
    statepostal = models.CharField(max_length=255, blank=True, null=True)
    statename = models.CharField(max_length=255, blank=True, null=True)
    racetype = models.CharField(max_length=255, blank=True, null=True)
    reportingunitid = models.CharField(max_length=255, blank=True, null=True)
    racetypeid = models.CharField(max_length=255, blank=True, null=True)
    officeid = models.CharField(max_length=255, blank=True, null=True)
    officename = models.CharField(max_length=255, blank=True, null=True)
    party = models.CharField(max_length=255, blank=True, null=True)
    seatname = models.CharField(max_length=255, blank=True, null=True)
    seatnum = models.CharField(max_length=255, blank=True, null=True)
    uncontested = models.BooleanField()
    lastupdated = models.CharField(max_length=255, blank=True, null=True)
    lastupdated_parsed = models.DateTimeField(blank=True, null=True)
    initialization_data = models.BooleanField()
    race_votecount = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'race'

    def __unicode__(self):
        if self.clean_name:
            return self.clean_name
        return "%s - %s" % (self.statepostal, self.officename)

class ReportingUnit(models.Model):
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    clean_description = models.TextField(blank=True, null=True)
    accept_ap_calls = models.BooleanField(default=True)
    race = models.ForeignKey(Race, blank=True, null=True)
    officeid = models.CharField(max_length=255, blank=True, null=True)
    officename = models.CharField(max_length=255, blank=True, null=True)
    racetype = models.CharField(max_length=255, blank=True, null=True)
    statepostal = models.CharField(max_length=255, blank=True, null=True)
    statename = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    reportingunitname = models.CharField(max_length=255, blank=True, null=True)
    reportingunitid = models.CharField(max_length=255, blank=True, null=True)
    fipscode = models.CharField(max_length=255, blank=True, null=True)
    lastupdated = models.CharField(max_length=255, blank=True, null=True)
    lastupdated_parsed = models.DateTimeField(blank=True, null=True)
    precinctsreporting = models.IntegerField()
    precinctsyotal = models.IntegerField()
    precinctsreportingpct = models.FloatField()
    raceid = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    seatname = models.CharField(max_length=255, blank=True, null=True)
    uncontested = models.BooleanField()
    reportingunit_votecount = models.IntegerField(default=0, blank=True, null=True)
    race_votecount = models.IntegerField(default=0, blank=True, null=True)
    race_votepct = models.FloatField(default=0.0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reportingunit'

    def __unicode__(self):
        if self.clean_name:
            return self.clean_name
        return "%s, %s - %s" % (self.statepostal, self.reportingunitname, self.racetype)


class CandidateResult(models.Model):
    accept_ap_calls = models.BooleanField(default=True)
    candidate = models.ForeignKey(Candidate, blank=True, null=True)
    reporting_unit = models.ForeignKey(ReportingUnit, blank=True, null=True)
    race = models.ForeignKey(Race, blank=True, null=True)
    racetype = models.CharField(max_length=255, blank=True, null=True)
    reportingunitid = models.CharField(max_length=255, blank=True, null=True)
    reportingunitname = models.CharField(max_length=255, blank=True, null=True)
    first = models.CharField(max_length=255, blank=True, null=True)
    last = models.CharField(max_length=255, blank=True, null=True)
    party = models.CharField(max_length=255, blank=True, null=True)
    candidateid = models.CharField(max_length=255, blank=True, null=True)
    polid = models.CharField(max_length=255, blank=True, null=True)
    ballotorder = models.CharField(max_length=255, blank=True, null=True)
    polnum = models.CharField(max_length=255, blank=True, null=True)
    officeid = models.CharField(max_length=255, blank=True, null=True)
    officename = models.CharField(max_length=255, blank=True, null=True)
    votecount = models.IntegerField()
    winner = models.BooleanField()
    is_ballot_position = models.BooleanField()
    raceid = models.CharField(max_length=255, blank=True, null=True)
    statepostal = models.CharField(max_length=255, blank=True, null=True)
    statename = models.CharField(max_length=255, blank=True, null=True)
    seatname = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    uncontested = models.BooleanField()
    reportingunit_votecount = models.IntegerField(default=0, blank=True, null=True)
    reportingunit_votepct = models.FloatField(default=0.0, blank=True, null=True)
    race_votecount = models.IntegerField(default=0, blank=True, null=True)
    race_votepct = models.FloatField(default=0.0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidateresult'
        ordering = ['statepostal', 'last', 'first']

    def __unicode__(self):
        if self.is_ballot_position:
            return "%s %s %s" % (self.last, self.statepostal, self.seatname)
        if self.seatname:
            return "%s %s %s %s" % (self.first, self.last, self.statepostal, self.seatname)
        if self.officename:
            return "%s %s (%s): %s" % (self.first, self.last, self.statepostal, self.officename)