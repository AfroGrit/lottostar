#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Luke Kitunka"
__version__ = "0.1.0"
__license__ = "All Rights Reserved"

import argparse
import csv
import re


class Files():
    """
    Base class for file handling
    """

    def __init__(self):
        print('Opening files')


class OpenFiles(Files):
    """
    Elaborate to aggregate csv files
    """

    def dict_csv(self, fname):
        with open(fname) as f:
            # next(f)
            reader = csv.DictReader(f, delimiter=';')
            # Row = [Ticket_id, Mainballs, Sub1, Sub2]
            for line in reader:
                # print (line["mainballs"])
                print(line)


class Lottery:
    """
    Base class for lottery work
    """

    def __init__(self):
        pass
        # print ('Lottery created')


class LotteryNational(Lottery):
    """
    Details for a National lottery e.g. Germany only
    country
    date
    tickets and jackpot
    """

    def __init__(self, tickets, results):
        Lottery.__init__(self)
        # print(' Lottery National created')
        self.country = re.search('(.+?)_', results).group(1).upper()
        self.date = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", results).group(1)
        # self.date = extractdate #ddmmyyyy
        self.tickets = tickets
        self.results = results

    def __str__(self):
        print('\nLottery details')
        print('+++++++++++++++\n')
        return f"{self.country} Lottery, Draw on {self.date}.\nLoaded file: {self.tickets} & {self.results}\n"

    def __len__(self):
        # Get the number of tickets played from files
        with open(self.tickets) as f:
            # next(f)
            ticket = 0
            reader = csv.DictReader(f, delimiter=';')
            for line in reader:
                ticket += 1
        return ticket

    def view(self):
        resultplayed = OpenFiles.dict_csv(self.results)
        ticketsplayed = OpenFiles.dict_csv(self.tickets)
        return "{resultplayed}"


def main(args):
    foo = LotteryNational('germany_03-11-2019_32322-1.csv', 'germany_03-11-2019_32322 result-1.csv')
    print(foo)
    views = foo.view()

    print('/n')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)