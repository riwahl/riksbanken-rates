{{ config(
    materialized= 'table',
    unique_key = 'id'
)}}


WITH source AS (
    SELECT * FROM {{source('dev', 'reference_rate')}}
)

SELECT
    id,
    date as value_date,
    value as rate,
    'Styrränta' as description,
    series_id,
    inserted_at

FROM source