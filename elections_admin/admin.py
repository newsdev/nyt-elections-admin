from django.contrib import admin

from elections_admin import models

admin.site.register(models.Race)
admin.site.register(models.Candidate)
admin.site.register(models.BallotPosition)
admin.site.register(models.CandidateResult)
admin.site.register(models.ReportingUnit)