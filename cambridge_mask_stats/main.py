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

from typing import Any


# constants
AQI_LEVEL = (1, 2, 3, 4, 5)
AQI_HOURS = (340, 340, 220, 180, 90)


class Base:
    def __init__(self, file: str):
        self._df = pd.read_csv(file, index_col=0, parse_dates=[0])
        self._calc_minutes_worn_ratio()

        self._worn_hours = StatsWornHours(self._df)
        self._worn_percent = StatsWornPercent(self._df)

    def get_df(self) -> pd.DataFrame:
        """Returns a <pandas.DataFrame>.

        :return: <pandas.DataFrame>
        """

        return self._df

    def run_terminal(self):
        """Executes the output for the terminal."""

        self._output_title(self._worn_hours.get_title())
        self._worn_hours.run_terminal()
        self._worn_percent.run_terminal()

    def _calc_minutes_worn_ratio(self):
        """Increases the minutes based on the aqi level.

        the ratio was determined using the data from the instructions for use
        and refers to the pro version of the mask with a lifetime of 340 hours
        at aqi level 2.
        """

        for index, value in self._df.iterrows():
            for level, hours in zip(AQI_LEVEL, AQI_HOURS):
                if value.aqi_level == level:
                    self._df.at[index, 'minutes_worn'] = value.minutes_worn * (AQI_HOURS[1] / hours)

    @staticmethod
    def _output_title(title: str):
        """Prints the title in a specific format.

        :param title: <str>
        """

        print('\n{:*^50}'.format(title))


class Stats:
    def __init__(self, df: pd.DataFrame):
        self._df = df

        self._title = ''
        self._subtitle = ''
        self._header = None
        self._str = '{:2} {:25} {:}'

    def get_data(self) -> Any:
        """Return the data [abstract]."""

    def get_date_range_series(self, column: str, **kwargs) -> pd.Series:
        """Returns a series with date index and the column passed by parameter.

        :param column: <str>
        :param kwargs: <dict>
            Parameters for <pandas.DataFrame.reindex>. More information at:
            https://pandas.pydata.org/docs/reference/index.html
        :return: <pandas.Series>
        """

        date_range = pd.date_range(self._df.iloc[0].name.date(), self._df.iloc[-1].name.date())
        series = self._df[column].reindex(date_range, **kwargs)

        return series

    def get_title(self):
        """Returns the title.

        :return: <str>
        """

        return self._title

    def get_subtitle(self):
        """Returns the subtitle.

        :return: <str>
        """

        return self._subtitle

    def run_terminal(self):
        """Executes the base output for the terminal."""

        data = self.get_data()
        self._terminal_subtitle()
        self._run_terminal(data)

    def _run_terminal(self, data):
        """Executes the output for the terminal [abstract]."""

        for index, value in data.iteritems():
            print(self._str.format(*index, value))

    def _terminal_subtitle(self):
        """Print subtitle and column names for the terminal [abstract]."""

        print('\n{}'.format(self._subtitle))
        print(self._str.format(*self._header[0], self._header[1]))


class StatsWorn(Stats):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self._title = '[WORN]'


class StatsWornHours(StatsWorn):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)

        self._subtitle = '[HOURS WORN]'
        self._header = (('ID', 'MASK'), 'HOURS')

    def get_data(self):
        """Return the data [abstract]."""

        return self._df['minutes_worn'].groupby([self._df['id'], self._df['model']]).sum() // 60


class StatsWornPercent(StatsWorn):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)

        self._subtitle = '[WORN PERCENT]'
        self._header = (('ID', 'MASK'), 'PERCENT')

    def get_data(self):
        """Return the data [abstract]."""

        swh = StatsWornHours(self._df)
        data: pd.Series = swh.get_data()
        data.name = 'worn_percent'

        for index, value in data.iteritems():
            data.at[index] = round(((value / AQI_HOURS[1]) * 100), 2)

        return data


def main():
    """Main function of the program."""

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    base = Base(args.file)
    base.run_terminal()


if __name__ == '__main__':
    main()
