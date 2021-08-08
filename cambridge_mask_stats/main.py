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


# constants
AQI_LEVEL = (1, 2, 3, 4, 5)
AQI_HOURS = (340, 340, 220, 180, 90)


class Base:
    def __init__(self, file: str):
        self._df = pd.read_csv(file, index_col=0, parse_dates=[0])
        self._calc_minutes_worn_ratio()

    def get_df(self) -> pd.DataFrame:
        """Returns a <pandas.DataFrame>.

        :return: <pandas.DataFrame>
        """

        return self._df

    def run_terminal(self):
        """Executes the output for the terminal."""

        stats_masks = StatsMasks(self._df)
        stats_masks.run_terminal()

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


class Stats:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._title = ''

    def get_df(self) -> pd.DataFrame:
        """Get a DataFrame with all series available in the class [abstract]."""

    def run_terminal(self):
        """"""

        print('\n{:*^50}\n\n{}'.format(self._title, self.get_df()))


class StatsDate(Stats):
    """Statistics with a date range and all masks together."""

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)

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


class StatsMasks(Stats):
    """Statistics which are separated for each mask."""

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self._title = ' StatsMasks '

    def get_df(self) -> pd.DataFrame:
        """Get a DataFrame with all series available in the class [abstract]."""

        df = pd.concat([self.get_worn_hours(), self.get_worn_percentage()], axis=1)
        df.rename_axis('worn | wear', axis=1, inplace=True)

        return df

    def get_worn_hours(self) -> pd.Series:
        """Returns the time worn in hours for each mask."""

        series: pd.Series = self._df['minutes_worn'].groupby([self._df['id'], self._df['model']]).sum() // 60
        series.name = 'hrs'

        return series

    def get_worn_percentage(self) -> pd.Series:
        """Returns the wear percentage for each mask."""

        series: pd.Series = self.get_worn_hours()
        series.name = 'pct'

        for index, value in series.iteritems():
            series.at[index] = round(((value / AQI_HOURS[1]) * 100), 2)

        return series


def main():
    """Main function of the program."""

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    base = Base(args.file)
    base.run_terminal()


if __name__ == '__main__':
    main()
