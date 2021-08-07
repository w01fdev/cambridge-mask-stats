#!/usr/bin/env python3

"""Cambridge-Mask-Stats
Copyright (C) 2021 w01f - https://github.com/w01fdev/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

########################################################################

w01f hacks from Linux for Linux!

fck capitalism, fck patriarchy, fck racism, fck animal oppression...

########################################################################
"""

import argparse
import pandas as pd


class Base:
    def __init__(self, file: str):
        self._df = pd.read_csv(file, index_col=0, parse_dates=[0])
        self._calc_minutes_worn_ratio()

    def get_df(self) -> pd.DataFrame:
        """Returns a <pandas.DataFrame>.

        :return: <pandas.DataFrame>
        """

        return self._df

    def get_date_range_series(self, column: str, **kwargs) -> pd.Series:
        """

        :param column: <str>
        :param kwargs: <dict>
            Parameters for <Pandas.DataFrame.reindex>. More information at:
            https://pandas.pydata.org/docs/reference/index.html
        :return:
        """

        date_range = pd.date_range(self._df.iloc[0].name.date(), self._df.iloc[-1].name.date())
        series = self._df[column].reindex(date_range, **kwargs)

        return series

    def run_terminal(self):
        """Executes the output for the terminal."""

        total_worn_time = StatsTotalWornTime(self._df)
        total_worn_time.run_terminal()

    def _calc_minutes_worn_ratio(self):
        """Increases the minutes based on the aqi level.

        the ratio was determined using the data from the instructions for use
        and refers to the pro version of the mask with a lifetime of 340 hours
        at aqi level 2.
        """

        aqi_level = (1, 2, 3, 4, 5)
        aqi_hours = (340, 340, 220, 180, 90)

        for index, row in self._df.iterrows():
            for level, hours in zip(aqi_level, aqi_hours):
                if row.aqi_level == level:
                    self._df.at[index, 'minutes_worn'] = row.minutes_worn * (aqi_hours[1] / hours)


class Stats:
    def __init__(self, df: pd.DataFrame):
        self._df = df

        self._title = None
        self._header = None
        self._str = '{:2} {:25} {:>3}'

    def _terminal_header(self):
        """Heading and column names for the terminal [abstract]."""

        print(self._title)
        print(self._str.format(*self._header[0], self._header[1]))


class StatsTotalWornTime(Stats):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)

        self._title = '\n[TOTAL WORN TIME]'
        self._header = (('ID', 'MASK'), 'HOURS')
        self._data = self._df['minutes_worn'].groupby([self._df['id'], self._df['model']]).sum() // 60

    def run_terminal(self):
        """Executes the output for the terminal."""

        self._terminal_header()

        for index, value in self._data.iteritems():
            print(self._str.format(*index, value))


def main():
    """Main function of the program."""

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    base = Base(args.file)
    base.run_terminal()


if __name__ == '__main__':
    main()
