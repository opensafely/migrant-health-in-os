
import argparse

from ehrql import create_measures, INTERVAL, years

from analysis.qof_dictionary import DISEASES
from analysis.def_disease_numerators import build_disease_numerator
from analysis.def_common_population import (
    build_common_population,
    apply_age_restriction,
)
import analysis.def_migration_status_variables as migration
import analysis.def_subgroups as subgroups

parser = argparse.ArgumentParser()
parser.add_argument("--disease", required=True, choices=DISEASES)
disease_name = parser.parse_args().disease
config = DISEASES[disease_name]


measures = create_measures()
measures.configure_dummy_data(population_size=1000)
measures.configure_disclosure_control(enabled=False)
measures.define_defaults(intervals=years(17).starting_on("2009-04-01"))


eligible_group, registration_duration = build_common_population()

migrant_status = migration.build_migrant_indicators(INTERVAL.end_date)
mig3_expr = migration.build_mig_status_3_cat(migrant_status)


numerator = build_disease_numerator(
    codelist=config["codelist"],
    resolved_codelist=config["resolved_codelist"],
)

eligible_group, registration_duration = apply_age_restriction(
    eligible_group,
    registration_duration,
    config["min_age"],
)


measures.define_measure(
    name=f"{disease_name}_by_mig_status",
    denominator=eligible_group,
    numerator=numerator,
    group_by={
        "migrant_status": mig3_expr,
        "age_band": subgroups.age_band,
    },
)

measures.define_measure(
    name=f"{disease_name}_overall",
    denominator=eligible_group,
    numerator=numerator,
)

for key, expr in migrant_status.items():
    safe_label = key.lower().replace(" ", "_").replace("-", "_")

    measures.define_measure(
        name=f"{disease_name}_by_{safe_label}",
        denominator=eligible_group & expr,
        numerator=numerator,
    )

measures.define_measure(
    name=f"{disease_name}_by_mig_status_person_time_denom",
    denominator=registration_duration,
    numerator=numerator,
    group_by={"migrant_status": mig3_expr},
)
