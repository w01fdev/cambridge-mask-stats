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
import datetime
import pandas as pd

# constants
AQI_LEVEL = (1, 2, 3, 4, 5)
AQI_HOURS = (340, 340, 220, 180, 90)
MINUTES_MAX = AQI_HOURS[1] * 60


class Base:
    def __init__(self, file: str, days: int = 30):
        self._days = days

        self._df = pd.read_csv(file, index_col=0, parse_dates=[0])
        self._calc_minutes_worn_ratio()

    def get_df(self) -> pd.DataFrame:
        """Returns a <pandas.DataFrame>."""

        return self._df

    def run_terminal(self):
        """Executes the output for the terminal."""

        stats_masks = StatsMasks(self._df, self._days)
        stats_masks.run_terminal()
        stats_date_range = StatsDateRange(self._df)
        stats_date_range.run_terminal()

    def _calc_minutes_worn_ratio(self):
        """Increases the minutes based on the aqi level.

        the ratio was determined using the data from the instructions for use
        and refers to the pro version of the mask with a lifetime of 340 hours
        at aqi level 2.
        """

        self._df['minutes_worn_ratio'] = 0

        for index, value in self._df.iterrows():
            for level, hours in zip(AQI_LEVEL, AQI_HOURS):
                if value.aqi_level == level:
                    self._df.at[index, 'minutes_worn_ratio'] = value.minutes_worn * (AQI_HOURS[1] / hours)


class Stats:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._title = ''

    def get_date_range(self, columns: list[str], **kwargs) -> pd.DataFrame:
        """Returns a DataFrame with date index and columns passed by parameter.

        :param columns: <str>
        :param kwargs: <dict>
            Parameters for <pandas.DataFrame.reindex>. More information at:
            https://pandas.pydata.org/docs/reference/index.html
        """

        date_range = pd.date_range(self._df.iloc[0].name.date(), self._df.iloc[-1].name.date())

        return self._df[columns].reindex(date_range, **kwargs)

    def run(self) -> pd.DataFrame:
        """Get a DataFrame with all series available in the class [abstract]."""

    def run_terminal(self):
        """Prints the title of the respective statistic."""

        print('\n{:*^50}\n{:}'.format(self._title, self.run()))


class StatsDate(Stats):
    """Statistics with a date range and all masks together."""

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)


class StatsDateRange(StatsDate):
    """Subclass for time series that output a range of dates."""

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self._title = ' StatsDateRange '
        self._mw = 'minutes_worn'
        self._mwr = 'minutes_worn_ratio'

        self._df: pd.DataFrame = self.get_date_range(['minutes_worn', 'minutes_worn_ratio'], fill_value=0)

    def run(self) -> pd.DataFrame:
        """Get a DataFrame with all series | df available in the class [abstract]."""

        df = pd.concat([self.get_count_days(), self.get_mean_min_daily(), self.get_sum_min_month(), self.get_sum_hrs(),
                        self.get_pct()], axis=1)
        df.rename_axis('worn | wear', axis=1, inplace=True)

        return df

    def get_count_days(self) -> pd.Series:
        """Returns a day counter for each month."""

        series: pd.Series = self._df[self._mw].resample('M').count()
        series = series.astype(int)
        series.name = 'count_d'

        return series

    def get_mean_min_daily(self) -> pd.DataFrame:
        """Returns the daily mean value in minutes for each month."""

        df: pd.DataFrame = self._df.resample('M').mean()
        df = df.astype(int)

        return df.rename(self._column_rename('mean_min_d', 'mean_min_d_ratio'), axis='columns')

    def get_sum_min_month(self) -> pd.DataFrame:
        """Returns the summed value in minutes for each month."""

        df: pd.DataFrame = self._df.resample('M').sum()

        return df.rename(self._column_rename('sum_min', 'sum_min_ratio'), axis='columns')

    def get_sum_hrs(self) -> pd.DataFrame:
        """Returns the summed value in hours for each month."""

        df: pd.DataFrame = (self._df.resample('M').sum() // 60)

        return df.rename(self._column_rename('sum_hrs', 'sum_hrs_ratio'), axis='columns')

    def get_pct(self) -> pd.Series:
        """Returns the value of wear in percentage for each month."""

        series: pd.Series = (self._df['minutes_worn_ratio'].resample('M').sum() / (AQI_HOURS[1] * 60) * 100)
        series = series.round(2)
        series.name = 'pct'

        return series

    def _column_rename(self, minutes_worn: str, minutes_worn_ratio: str) -> dict[str]:
        """Dictionary for simple renaming of columns in a <Pandas.DataFrame>."""

        return {self._mw: minutes_worn, self._mwr: minutes_worn_ratio}


class StatsMasks(Stats):
    """Statistics which are separated for each mask."""

    def __init__(self, df: pd.DataFrame, days: int = 30):
        super().__init__(df)
        self._title = ' StatsMasks '
        self._eol_days = days

    def run(self) -> pd.DataFrame:
        """Get a DataFrame with all series available in the class [abstract]."""

        df = pd.concat([self.get_worn_hours(), self.get_worn_hours_ratio(), self.get_worn_days(),
                        self.get_worn_percentage(), self.get_end_of_life()], axis=1)
        df.rename_axis('worn | wear', axis=1, inplace=True)

        return df

    def get_end_of_life(self) -> pd.DataFrame:
        """Prediction when the mask will probably reach the end of life."""

        ser = self.get_date_range(['minutes_worn_ratio'], fill_value=0)

        if self._eol_days == 0:
            mean = ser.mean()
        else:
            mean = ser.iloc[-self._eol_days:].mean()

        ser = self._df['minutes_worn_ratio'].groupby([self._df['id'], self._df['model']]).sum()
        ser_days = ser.copy(deep=True)
        ser_date = ser.copy(deep=True)
        ser_days.name = 'eol_d'
        ser_date.name = 'eol_date'

        for ix, (index, value) in enumerate(ser.iteritems()):
            eol = int(((AQI_HOURS[1] * 60) - value) // mean)
            ser_days.iloc[ix] = eol
            ser_date.iloc[ix] = datetime.date.today() + datetime.timedelta(days=eol)

        return pd.concat([ser_days, ser_date], axis=1)

    def get_worn_days(self):
        """Returns the days worn for each mask."""

        ser = self._df['minutes_worn'].groupby([self._df['id'], self._df['model']]).count()
        ser.name = 'worn_d'

        return ser

    def get_worn_hours(self, ratio: bool = False) -> pd.Series:
        """Returns the time worn in hours for each mask."""

        if ratio:
            column = 'minutes_worn_ratio'
            name = 'hrs_ratio'
        else:
            column = 'minutes_worn'
            name = 'hrs'

        series: pd.Series = self._df[column].groupby([self._df['id'], self._df['model']]).sum() // 60
        series.name = name

        return series

    def get_worn_hours_ratio(self):
        """Returns the time worn ratio in hours for each mask."""

        return self.get_worn_hours(ratio=True)

    def get_worn_percentage(self) -> pd.Series:
        """Returns the wear percentage for each mask."""

        series: pd.Series = self.get_worn_hours_ratio()
        series.name = 'pct'

        for index, value in series.iteritems():
            series.at[index] = round(((value / AQI_HOURS[1]) * 100), 2)

        return series


def main():
    """Main function of the program."""

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('--days', '-d', type=int, default=30,
                        help='days to be used in the end of life prediction. enter 0 for all [default: 30]')
    args = parser.parse_args()

    base = Base(args.file, args.days)
    base.run_terminal()


if __name__ == '__main__':
    main()
