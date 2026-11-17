# A script with helper code to be used in the annual estimates

from ehrql import years

# QOF interval default (interval starts at the beginning of the financial year)

annual_intervals = years(17).starting_on("2009-04-01")