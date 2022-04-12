-- returns overall order count for each driver and his order-to-ride conversion
WITH cnt_by_driver AS (
    SELECT
        id_driver,
        count(*) AS cnt
    FROM
        skytaxi.order_list
    WHERE
        1 = 1
        AND id_driver IS NOT NULL
    GROUP BY
        id_driver
),
o2r_by_driver AS (
    SELECT
        id_driver,
        sum(
            CASE
                WHEN order_finish_time IS NOT NULL THEN 1
                ELSE 0
            END
        ) :: float / count(*) AS o2r
    FROM
        skytaxi.order_list
    WHERE
        1 = 1
        AND id_driver IS NOT NULL
    GROUP BY
        id_driver
)
SELECT
    a.*,
    b.o2r
FROM
    cnt_by_driver a
    LEFT JOIN o2r_by_driver b ON a.id_driver = b.id_driver
ORDER BY
    cnt DESC