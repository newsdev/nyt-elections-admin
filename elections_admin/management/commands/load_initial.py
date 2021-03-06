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
        self.logger.info('load_initial starting at %s.' % start)

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

            e = api.Election(electiondate=date, testresults=False, liveresults=True, is_test=False)

            for race in e.get_races(omitResults=True, level="ru", test=False):
                for c in race.candidates:
                    candidate_results.append(c)
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
            self.logger.info("load_initial parsed %s candidates." % len(candidates))
            self.logger.info("load_initial parsed %s ballot positions." % len(ballotpositions))
            self.logger.info("load_initial parsed %s races." % len(races))
            parse_end = datetime.datetime.now()
            self.logger.info('load_initial finished parsing at %s.' % parse_end)
            self.logger.info('load_initial starting inserts at %s.' % datetime.datetime.now())

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

            ###
            ### LOGGING
            ###
            self.logger.info("load_initial inserted %s candidates." % len(candidates))
            self.logger.info("load_initial inserted %s ballot positions." % len(ballotpositions))
            self.logger.info("load_initial inserted %s races." % len(races))
            end = datetime.datetime.now()
            self.logger.info('load_initial finished inserts at %s.' % end)
            self.logger.info("load_initial time overall: %s seconds." % float(str(end - start).split(':')[-1]))
            self.logger.info("load_initial time parsing: %s seconds." % float(str(parse_end - start).split(':')[-1]))
            self.logger.info("load_initial time loading: %s seconds." % float(str(end - parse_end).split(':')[-1]))
            self.logger.info('load_initial finshed at %s.' % end)

        else:
            self.logger.critical('load_initial error please specify an election date. Format: YYYY-MM-DD')
