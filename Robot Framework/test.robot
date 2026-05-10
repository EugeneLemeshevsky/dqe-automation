*** Settings ***
Library           SeleniumLibrary
Library           helper.py

*** Variables ***
${REPORT_FILE}      ${CURDIR}/report.html
${PARQUET_FOLDER}   ${CURDIR}/parquet_data/facility_type_avg_time_spent_per_visit_date
${FILTER_DATE}      ${EMPTY}
${BROWSER}          Chrome

*** Test Cases ***
Compare HTML Table With Parquet Dataset
    [Teardown]    Close Browser
    Open Browser    file:///${REPORT_FILE}    ${BROWSER}
    Wait Until Element Is Visible    class:table    timeout=10s
    ${table}=    Get WebElement    class:table
    ${df_html}=    Read Html Table    ${table}
    ${df_parquet}=    Read Parquet    ${PARQUET_FOLDER}    ${FILTER_DATE}
    ${differences}=    Compare Dataframes    ${df_html}    ${df_parquet}
