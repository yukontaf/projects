-- returns chain growth of order-to-ride conversion for split by tariff 
SELECT
    t2.*,
    o2r / lag_o2r AS chain_growth
FROM
    (
        SELECT
            t.*,
            lag(o2r) over (
                PARTITION by name_tariff
                ORDER BY
                    dd
            ) AS lag_o2r
        FROM
            (
                SELECT
                    name_tariff,
                    date_trunc('day', order_time) AS dd,
                    sum(
                        CASE
                            WHEN order_finish_time IS NOT NULL THEN 1.0
                            ELSE 0.0
                        END
                    ) / count(*) AS o2r
                FROM
                    skytaxi.order_list a
                    LEFT JOIN skytaxi.tariff_dict b ON a.id_tariff = b.id_tariff
                WHERE
                    1 = 1
                    AND name_tariff IN ('Эконом', 'Комфорт')
                GROUP BY
                    name_tariff,
                    dd
                ORDER BY
                    dd,
                    name_tariff
            ) t
    ) t2