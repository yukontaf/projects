-- returns moving average for the count of loans given separated by city and period
SELECT
    month_loan,
    name_city ---
,
    cnt,
    avg(cnt) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 3 preceding
            AND current ROW
    ) AS ma3_cnt,
    avg(cnt) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 10 preceding
            AND current ROW
    ) AS ma10_cnt,
    avg(cnt) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 20 preceding
            AND current ROW
    ) AS ma20_cnt ---
,
    amt_loan,
    avg(amt_loan) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 3 preceding
            AND current ROW
    ) AS ma3_amt,
    avg(amt_loan) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 10 preceding
            AND current ROW
    ) AS ma10_amt,
    avg(amt_loan) over (
        PARTITION by name_city
        ORDER BY
            month_loan ROWS BETWEEN 20 preceding
            AND current ROW
    ) AS ma20_amt ---
,
    sum(cnt) over (
        PARTITION by name_city
        ORDER BY
            month_loan ASC
    ) sum_cum_cnt,
    sum(amt_loan) over (
        PARTITION by name_city
        ORDER BY
            month_loan ASC
    ) sum_cum_amt
FROM
    (
        SELECT
            date_trunc('month', date_loan :: date) month_loan,
            sum(amt_loan) amt_loan,
            name_city,
            count(*) AS cnt
        FROM
            skybank_late_collection_clients a
            LEFT JOIN skybank_region_dict b ON a.id_city = b.id_city
        GROUP BY
            month_loan,
            name_city
        ORDER BY
            month_loan
    ) t