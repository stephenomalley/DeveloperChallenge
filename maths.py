__author__ = 'Stephen'

import math
import decimal


class StatisticMaths(object):

    def calculate_mean(self, values):
        count = sum(values)
        return count/len(values)

    def calculate_median(self, values):
        sorted_values = sorted(values)
        length = len(sorted_values)
        if not length % 2:
            return (sorted_values[length / 2] + sorted_values[length / 2 - 1]) / 2.0
        return sorted_values[length / 2]

    def bankers_round(self, value):
        abs_value = abs(value)
        floor = math.floor(abs_value)

        if value == 0:
            sign = 0
        elif value < 0:
            sign = -1
        else:
            sign = 1

        if abs_value - floor != 0.5:
            return self.stat_round(abs_value) * sign

        if floor % 2 == 1:
            return int(math.ceil(abs_value) * sign)

        return int(floor * sign)

    def stat_round(self, value):
        return decimal.Decimal(value).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_EVEN)