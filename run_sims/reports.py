from emodpy_malaria.reporters.builtin import add_malaria_cotransmission_report, add_report_infection_stats_malaria

from run_sims import manifest


def add_default_reports(emod_task, reporting_interval=30, test_run=False):
    if test_run:
        report_start_day = 3*365
    else:
        report_start_day = 30*365

    add_malaria_cotransmission_report(emod_task, manifest=manifest,
                                      start_day=report_start_day, max_age_years=1000)
    add_report_infection_stats_malaria(emod_task, manifest=manifest,
                                       start_day=report_start_day, reporting_interval=reporting_interval)
