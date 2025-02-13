select 'in select expr, a SRF (set returning function) is made to return
a series that will lined up in parallel to other rows.';
select generate_series(1, 5) a, generate_series(1,5) b;

select 'If one series is longer than another, nulls fill it';
select generate_series(1, 5) a, generate_series(2,4) b;

select 'in from expr, two SRF-results are cross joined

This is because in the from clause, the SRF is made to return
relations. (Nomenclature: relations includes tables, views,
subqueries, and results of functions that return sets of rows).

So the behavior applies where "comma does cross join" between 
relations.
';
select * from generate_series(1, 3) a, generate_series(1,3) b;

select 'Can treat the series as an arbitrary "do N times" loop';
select random() from generate_series(1, 3);

-- select 'Can use to populate tables, particularly useful in the 
-- select clause';

/**already populating table in simple_tables.sql, just showing example here**/
-- insert into numbers_small_tbl (b, c) 
-- select generate_series(1,100), generate_series(100,1, -1)
