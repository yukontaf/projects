-- returns table, where a new column with mean loan for each client's region and its standard deviation
SELECT
    id_client,
    amt_credit,
    name_city,
    var_amt,
    stddev_amt,
    cnt_by_city,
    2 *(stddev_amt / sqrt(cnt_by_city)) AS len_int,
    avg_by_city,
    avg_by_city + stddev_amt / sqrt(cnt_by_city) AS max_int,
    avg_by_city - stddev_amt / sqrt(cnt_by_city) AS min_int
FROM
    (
        SELECT
            id_client,
            amt_credit,
            name_city,
            variance(amt_credit) over (PARTITION by name_city) AS var_amt,
            sqrt(
                variance(amt_credit) over (PARTITION by name_city)
            ) AS stddev_calc_amt,
            stddev(amt_credit) over (PARTITION by name_city) AS stddev_amt,
            avg(amt_credit) over (PARTITION by name_city) avg_by_city,
            count(*) over (PARTITION by name_city) cnt_by_city
        FROM
            skybank.early_collection_clients a
            LEFT JOIN skybank.region_dict b ON a.id_city = b.id_city
        WHERE
            1 = 1
            AND amt_credit IS NOT NULL
            AND last_paid_inst IS NOT NULL
    ) t