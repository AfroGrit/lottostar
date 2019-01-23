#!/usr/bin/env python3
""" Module Docstring """

__author__ = "Jean Luc Kitunka"
__version__ = "0.1.0"
__license__ = "All Rights Reserved"

import argparse
import csv
import errno
import logging
import os
import os.path
import re


class Lottery:
    """ Base class | lottery handler """

    def __init__(self, tickets, results):
        # print ('Lotter created')
        self.tickets = tickets
        self.results = results

    def credentials(self):
        raise NotImplementedError("check the subclasses")

    def tuplecsv(self):
        raise NotImplementedError("check the subclasses")

    def jackpot(self):
        raise NotImplementedError("check the subclasses")


class LotteryNational(Lottery):
    """ Details for a National lottery e.g. Germany only | country | date """

    def credentials(self):
        """ Use file name to extract the country """
        country = re.search('(.+?)_', self.results).group(1).upper()
        date = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", self.results).group(1)

    def view(self):
        """ Summarise and display """
        print('Summary of ', re.search('(.+?)_', self.results).group(1).upper(), 'lotto')
        print(23 * '=')

        # Read file and extract variables for views
        temptickets = self.tuplecsv(self.tickets)

        # Function that converts ['1,4,5,30,45', ...] into [(,4,5,30,45), ...]
        def listcleaner(thing):
            c = []
            for i in thing:
                a = i.split(",")
                b = tuple(map(int, a))
                c.append(b)
            return c

        # Use tuples for memory management.
        logging.info("Extract ticket ID into integers")
        print("Extracted ticket IDs: ", temptickets['ticket_id'])
        print("Extracted main balls: ",
              listcleaner(temptickets['mainballs']))  # Convert to a list of tuples for comparissons
        print("Extracted SUB1 IDs: ", temptickets['sub1'])
        # print ("\nExtracted SUB2 IDs are: ", list(map(int, temptickets['sub2']))) #Deal with empty lists

    def tuplecsv(self, tickets):
        """ bring in csv file and convert to tuples """
        logging.info("class that converts csv data into a list of tuples")
        try:
            def fitem(item):
                item = item.strip()
                try:
                    item = int(item)
                except ValueError:
                    pass
                return item

            # Read both files
            # with open(tickets) as ticketsin, open(results) as resultsin:
            with open(tickets) as ticketsin:
                reader = csv.DictReader(ticketsin, delimiter=';')
                # reader2 = csv.DictReader(resultsin, delimiter=';')

                data = {k.strip(): [fitem(v)] for k, v in next(reader).items()}
                for line in reader:
                    for k, v in line.items():
                        k = k.strip()
                        data[k].append(fitem(v))
                return data

        except FileNotFoundError:
            data = None

    def resultsfile(self):
        """  Report formatting and writer """
        print('\nWriting results to file.')
        print(23 * '=')

        # for every country
        # call the computed results
        # write to results file
        # append to other results

        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        def safe_open_w(path):
            """ Open "path" for writing, creating any parent directories as needed. """
            mkdir_p(os.path.dirname(path))
            return open(path, 'w')

        with safe_open_w('results/output-text.txt') as f:
            f.write("line %d\r\n")

    def jackpot(self):
        """ Compare ticket IDs with results and return Jackpot with ticket ID """
        print('\nJackPot')
        print(23 * '=')

    def __str__(self):
        """ Summary from input data """
        print('\nLottery details')
        print(23 * '+')
        # return f"{self.country} Lottery, Draw on {self.date}.\nLoaded file: {self.tickets} & {self.results}\n"

    def __len__(self):
        """ Return the numer of tickets enterered for a lottery"""
        # Get the number of tickets played/bought from files
        with open(self.tickets) as f:
            # next(f)
            ticket = 0
            reader = csv.DictReader(f, delimiter=';')
            for line in reader:
                ticket += 1
        return ticket


def main(args):
    # Prompt user which Lottery he/she would like to inspect
    # Use option above for subsequent queries

    # Sandbox
    foobar = LotteryNational(tickets='files/germany_03-11-2019_32322-1_mod.csv',
                             results='files/germany_03-11-2019_32322 result-1_mod.csv')
    # print(foobar)

    foobar.credentials()
    foobar.view()
    foobar.jackpot()
    foobar.resultsfile()

    # Configure logs
    LOG_FORMAT = "%(levelname)s %(asctime)s --- %(message)s"
    logging.basicConfig(file='files/logs/lottostat.log',
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        filemode='w')
    logger = logging.getLogger()


if __name__ == "__main__":
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
