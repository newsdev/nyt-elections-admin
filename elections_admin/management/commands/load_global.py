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
        self.logger.info('load_global starting at %s.' % start)

        date = options.get('date', None)

        if date:

            TABLE_LIST = [
                postgres.Candidate,
                postgres.CandidateResult,
                postgres.Race,
                postgres.ReportingUnit,
                postgres.BallotPosition
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

            unique_candidates = {}
            unique_ballotpositions = {}

            for c in candidate_results:
                if c.is_ballot_position:
                    if not unique_ballotpositions.get(c.candidateid, None):
                        unique_ballotpositions[c.candidateid] = {"last": c.last, "candidateid": c.candidateid, "polid": c.polid, "ballotorder": c.ballotorder, "polnum": c.polnum, "seatname": c.seatname, "description": c.description}
                else:
                    if not unique_candidates.get(c.candidateid, None):
                        unique_candidates[c.candidateid] = {"first": c.first, "last": c.last, "candidateid": c.candidateid, "polid": c.polid, "ballotorder": c.ballotorder, "polnum": c.polnum, "party": c.party}

            candidates = [postgres.Candidate(**v) for v in unique_candidates.values()]
            ballotpositions = [postgres.BallotPosition(**v) for v in unique_ballotpositions.values()]

            ###
            ### LOGGING
            ###
            self.logger.info("load_global parsed %s candidates." % len(candidates))
            self.logger.info("load_global parsed %s ballot positions." % len(ballotpositions))
            self.logger.info("load_global parsed %s races." % len(races))
            self.logger.info("load_global parsed %s reporting units." % len(reportingunits))
            self.logger.info("load_global parsed %s candidate results." % len(candidate_results))
            parse_end = datetime.datetime.now()
            self.logger.info('load_global finished parsing at %s.' % parse_end)
            self.logger.info('load_global starting inserts at %s.' % datetime.datetime.now())

            loader.ELEX_PG_CONNEX.connect()
            loader.ELEX_PG_CONNEX.drop_tables(TABLE_LIST, safe=True)
            loader.ELEX_PG_CONNEX.create_tables(TABLE_LIST, safe=True)

            with loader.ELEX_PG_CONNEX.atomic():
                for idx in range(0, len(candidates), 1000):
                    postgres.Candidate.insert_many([c.__dict__['_data'] for c in candidates[idx:idx+1000]]).execute()

            with loader.ELEX_PG_CONNEX.atomic():
                for idx in range(0, len(ballotpositions), 1000):
                    postgres.BallotPosition.insert_many([c.__dict__['_data'] for c in ballotpositions[idx:idx+1000]]).execute()

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
            self.logger.info("load_global inserted %s candidates." % len(candidates))
            self.logger.info("load_global inserted %s ballot positions." % len(ballotpositions))
            self.logger.info("load_global inserted %s races." % len(races))
            self.logger.info("load_global inserted %s reporting units." % len(reportingunits))
            self.logger.info("load_global inserted %s candidate results." % len(candidate_results))
            end = datetime.datetime.now()
            self.logger.info('load_gloabal finished inserts at %s.' % end)
            self.logger.info("load_global time overall: %s seconds." % float(str(end - start).split(':')[-1]))
            self.logger.info("load_global time parsing: %s seconds." % float(str(parse_end - start).split(':')[-1]))
            self.logger.info("load_global time loading: %s seconds." % float(str(end - parse_end).split(':')[-1]))
            self.logger.info('load_global finshed at %s.' % end)

        else:
            self.logger.critical('load_global error please specify an election date. Format: YYYY-MM-DD')
