from emodpy_malaria.reporters.builtin import add_malaria_cotransmission_report, add_report_event_counter, \
    add_report_infection_stats_malaria

from run_sims import manifest


def add_default_reports(emod_task, include_debugging_reports=False):
    # Different setups can have different simulation_duration. Pick it up directly from emod_task to use for reports
    simulation_duration = emod_task.config.parameters.Simulation_Duration
    report_start_day = simulation_duration-10*365
    if report_start_day < 0:
        report_start_day = 1

    add_malaria_cotransmission_report(emod_task, manifest=manifest,
                                      start_day=report_start_day, max_age_years=1000)
    add_report_infection_stats_malaria(emod_task, manifest=manifest,
                                       start_day=report_start_day, reporting_interval=30)
    # if include_debugging_reports:
    add_report_event_counter(emod_task, manifest=manifest,
                             start_day=report_start_day, event_trigger_list=["InfectionDropped","Received_Treatment"])