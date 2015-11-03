from django.contrib import admin

from elections_admin import models

class RaceAdmin(admin.ModelAdmin):
    list_filter = ['officeid','statepostal']
    list_display = ['__unicode__','officeid','officename','statepostal']

admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.Candidate)
admin.site.register(models.BallotPosition)
admin.site.register(models.CandidateResult)
admin.site.register(models.ReportingUnit)