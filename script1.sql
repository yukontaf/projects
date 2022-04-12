-- this script returns cleared sample for AB test
WITH level_1 AS (
    SELECT
        user_id,
        id_group,
        ad_date,
        purchase_date,
        promo_type,
        time_left,
        ROW_NUMBER() OVER (
            PARTITION BY user_id,
            promo_type
            ORDER BY
                ad_date
        ) AS rn
    FROM
        skymusic_marketing_pilot_proc
    WHERE
        time_left IS NOT NULL
),
level_2 AS (
    SELECT
        level_1.*,
        LEAD(time_left) OVER (
            PARTITION BY user_id
            ORDER BY
                ad_date
        ) AS time_left_lead
    FROM
        level_1
    WHERE
        rn = 1
)
SELECT
    promo_type,
    id_group,
    cnt_30 :: float / cnt_all r_30,
    cnt_60 :: float / cnt_all r_60,
    cnt_90 :: float / cnt_all r_90,
    cnt_all
FROM
    (
        SELECT
            promo_type,
            id_group,
            sum(
                CASE
                    WHEN purchase_date <= ad_date + INTERVAL '30 day'
                    AND purchase_date IS NOT NULL THEN 1
                    ELSE 0
                END
            ) cnt_30,
            sum(
                CASE
                    WHEN purchase_date <= ad_date + INTERVAL '60 day'
                    AND purchase_date IS NOT NULL THEN 1
                    ELSE 0
                END
            ) cnt_60,
            sum(
                CASE
                    WHEN purchase_date <= ad_date + INTERVAL '90 day'
                    AND purchase_date IS NOT NULL THEN 1
                    ELSE 0
                END
            ) cnt_90,
            count(*) AS cnt_all
        FROM
            level_2 AS t
        WHERE
            (
                purchase_date < time_left_lead
                OR time_left_lead IS NULL
                OR purchase_date IS NULL
            )
            AND (
                purchase_date > time_left
                OR purchase_date IS NULL
            )
            AND promo_type <> 'Gold Bundle'
        GROUP BY
            promo_type,
            id_group
    ) sq ------
SELECT
    *
FROM
    (
        SELECT
            a.*,
            lead(time_left) over (
                PARTITION by user_id
                ORDER BY
                    ad_date ASC
            ) AS lead_time_left,
            lag(time_left) over (
                PARTITION by user_id
                ORDER BY
                    ad_date ASC
            ) AS lag_time_left
        FROM
            skymusic.marketing_pilot_proc a
    ) t
WHERE
    (
        lead_time_left > ad_date
        OR lead_time_left IS NULL
    )