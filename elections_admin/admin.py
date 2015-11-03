from django.contrib import admin

from elections_admin import models

class RaceAdmin(admin.ModelAdmin):
    list_filter = ['officeid','statepostal']
    list_display = ['__unicode__','officeid','officename','statepostal']

class CandidateAdmin(admin.ModelAdmin):
    list_filter = ['party',]
    list_display =  ['__unicode__', 'ballotorder', 'polid', 'polnum', 'candidateid', 'party']

class CandidateResultAdmin(admin.ModelAdmin):
    list_per_page = 500
    search_fields = ['candidateid']
    list_filter = ['statepostal', 'is_ballot_position','officename','seatname','reportingunitname']
    list_display = ['__unicode__','votecount','reportingunit_votecount', 'reportingunit_votepct','race_votecount','race_votepct']

class ReportingUnitAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'statepostal', 'reportingunitname', 'officename', 'seatname']
    list_filter = ['statepostal', 'officename', 'seatname', 'level']

admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.BallotPosition)
admin.site.register(models.CandidateResult, CandidateResultAdmin)
admin.site.register(models.ReportingUnit, ReportingUnitAdmin)