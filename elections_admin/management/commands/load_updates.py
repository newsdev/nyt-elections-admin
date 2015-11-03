import datetime
import logging
from optparse import make_option

from elex.parser import api
from elex import loader
from elex.loader import postgres
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--date',
            dest='date',
            help='Run the loader for a given electiondate. YYYY-MM-DD'),
        )

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):

        ###
        ### LOGGING
        ###
        start = datetime.datetime.now()
        self.logger.info('load_updates starting at %s.' % start)

        date = options.get('date', None)

        if date:

            TABLE_LIST = [
                postgres.CandidateResult,
                postgres.Race,
                postgres.ReportingUnit,
            ]

            candidate_results = []
            races = []
            reportingunits = []

            e = api.Election(electiondate=date, testresults=False, liveresults=True, is_test=False)

            for race in e.get_races(omitResults=False, level="ru", test=False):
                for ru in race.reportingunits:
                    ru.aggregate_vote_count('votecount', 'reportingunit_votecount')
                race.aggregate_vote_count('reportingunit_votecount', 'race_votecount')

                for ru in race.reportingunits:
                    for c in ru.candidates:
                        c.aggregate_pcts(race.race_votecount, ru.reportingunit_votecount)
                        candidate_results.append(c)

                    ru.aggregate_pcts(race.race_votecount)
                    del ru.candidates
                    reportingunits.append(ru)

                del race.candidates
                del race.reportingunits
                races.append(race)

            ###
            ### LOGGING
            ###
            self.logger.info("load_updates parsed %s races." % len(races))
            self.logger.info("load_updates parsed %s reporting units." % len(reportingunits))
            self.logger.info("load_updates parsed %s candidate results." % len(candidate_results))
            parse_end = datetime.datetime.now()
            self.logger.info('load_updates finished parsing at %s.' % parse_end)
            self.logger.info('load_updates starting inserts at %s.' % datetime.datetime.now())

            loader.ELEX_PG_CONNEX.connect()
            loader.ELEX_PG_CONNEX.drop_tables(TABLE_LIST, safe=True)
            loader.ELEX_PG_CONNEX.create_tables(TABLE_LIST, safe=True)

            with loader.ELEX_PG_CONNEX.atomic():
                for idx in range(0, len(races), 1000):
                    postgres.Race.insert_many([c.__dict__ for c in races[idx:idx+1000]]).execute()

            with loader.ELEX_PG_CONNEX.atomic():
                for idx in range(0, len(candidate_results), 1000):
                    postgres.CandidateResult.insert_many([c.__dict__ for c in candidate_results[idx:idx+1000]]).execute()

            with loader.ELEX_PG_CONNEX.atomic():
                for idx in range(0, len(reportingunits), 1000):
                    postgres.ReportingUnit.insert_many([c.__dict__ for c in reportingunits[idx:idx+1000]]).execute()

            ###
            ### LOGGING
            ###
            self.logger.info("load_updates inserted %s races." % len(races))
            self.logger.info("load_updates inserted %s reporting units." % len(reportingunits))
            self.logger.info("load_updates inserted %s candidate results." % len(candidate_results))
            end = datetime.datetime.now()
            self.logger.info('load_gloabal finished inserts at %s.' % end)
            self.logger.info("load_updates time overall: %s seconds." % float(str(end - start).split(':')[-1]))
            self.logger.info("load_updates time parsing: %s seconds." % float(str(parse_end - start).split(':')[-1]))
            self.logger.info("load_updates time loading: %s seconds." % float(str(end - parse_end).split(':')[-1]))
            self.logger.info('load_updates finshed at %s.' % end)

        else:
            self.logger.critical('load_updates error please specify an election date. Format: YYYY-MM-DD')
