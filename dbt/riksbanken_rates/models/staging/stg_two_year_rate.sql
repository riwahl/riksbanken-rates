{{ config(
    materialized= 'table',
    unique_key = 'id'
)}}


WITH source AS (
    SELECT * FROM {{source('dev', 'two_year_rate')}}
)

SELECT
    id,
    date as value_date,
    value as rate,
    'Svensk bostadsobligation 2-års löptid' as description,
    series_id,
    inserted_at

FROM source