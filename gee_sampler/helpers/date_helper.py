import dateutil.parser

class DateHelper(object):
    @staticmethod
    def parse_date(datestring):
        return dateutil.parser.parse(datestring)
