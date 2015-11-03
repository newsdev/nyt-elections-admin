import csv
import datetime
import logging
import os
import time

from django.core.management.base import BaseCommand, CommandError

from elections_admin import models

class Command(BaseCommand):

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):

        self.logger.info('ky_gov_csv writing KY governor\'s race CSV.')

        ru = models.ReportingUnit.objects.filter(level='subunit', statepostal='KY', officename='Governor')

        candidates = models.Candidate.objects.filter(candidateid__in=['5295','5266','5296'])

        unique_counties = {}
        for u in ru:
            unique_counties[u.reportingunitname] = {
                'precincts_reporting': u.precinctsreporting,
                'precincts_total': u.precinctstotal,
                'precincts_reporting_pct': u.precinctsreportingpct,
                'bevin': 0,
                'conway': 0,
                'curtis': 0
            }
        results = models.CandidateResult.objects.filter(
            reportingunitid__in=[z.reportingunitid for z in ru],
            candidateid=[z.candidateid for z in candidates])
        for r in results:
            unique_counties[r.reportingunitname][r.last.lower()] = r.votecount

        payload = []

        for county, data in unique_counties.items():
            data['county'] = county
            payload.append(data)

        payload = sorted(payload, key=lambda x: x['county'])

        timestamp = str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0]
        ARCHIVE_FILE_PATH = '%s%s' % (os.environ.get('ELEX_OUTPUT_FOLDER', '/tmp/'), '%s-2015_ky_gov.csv' % timestamp)
        FILE_PATH = '%s%s' % (os.environ.get('ELEX_OUTPUT_FOLDER', '/tmp/'), '2015_ky_gov.csv')
        with open(ARCHIVE_FILE_PATH, 'w') as writefile:
            fieldnames = ['county','precincts_reporting','precincts_total','precincts_reporting_pct','bevin','conway','curtis']
            writer = csv.DictWriter(writefile, fieldnames=fieldnames)
            writer.writeheader()
            for row in payload:
                writer.writerow(row)

        with open(FILE_PATH, 'w') as writefile:
            fieldnames = ['county','precincts_reporting','precincts_total','precincts_reporting_pct','bevin','conway','curtis']
            writer = csv.DictWriter(writefile, fieldnames=fieldnames)
            writer.writeheader()
            for row in payload:
                writer.writerow(row)