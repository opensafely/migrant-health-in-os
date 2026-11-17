# A script to define the subgroups used in the annual estimates

from ehrql import INTERVAL, case, when
from ehrql.tables.tpp import patients, ons_deaths

# age

date_of_death = case(
    when(
        patients.date_of_death.is_not_null()
        & ons_deaths.date.is_not_null()
        & (patients.date_of_death <= ons_deaths.date)
    ).then(patients.date_of_death),

    when(
        patients.date_of_death.is_not_null()
        & ons_deaths.date.is_not_null()
        & (ons_deaths.date < patients.date_of_death)
    ).then(ons_deaths.date),

    when(patients.date_of_death.is_not_null()).then(
        patients.date_of_death
    ),

    when(ons_deaths.date.is_not_null()).then(
        ons_deaths.date
    )
)

age_reference_date = case(when(date_of_death.is_on_or_before(INTERVAL.end_date)
    ).then(date_of_death),
    otherwise=INTERVAL.end_date)

age = patients.age_on(age_reference_date)

age_band = case(
        when(age < 16).then("0-15"),
        when((age >= 16) & (age < 25)).then("16-24"),
        when((age >= 25) & (age < 35)).then("25-34"),
        when((age >= 35) & (age < 50)).then("35-49"),
        when((age >= 50) & (age < 65)).then("50-64"),
        when((age >= 65) & (age < 75)).then("65-74"),
        when((age >= 75) & (age < 85)).then("75-84"),
        when(age >= 85).then("85 plus"),
        otherwise="missing",
    )


