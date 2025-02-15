
ANALYZE numbers_large_tbl;
ANALYZE numbers_small_tbl;
ANALYZE numbers_indexed;
commit; -- ¯\_(ツ)_/¯

select 'In times of old, it was told that CTEs were optimization fences.

It was told that, if I used a subquery, I would get an explain plan
like this...';
explain analyze
select c, ct from 
    (
        select c, count(c) ct from 
        numbers_large_tbl group by c
    ) 
where c = 42;
/**
                                                     QUERY PLAN                                                     
--------------------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=0.00..1791.01 rows=1 width=12) (actual time=3.088..3.088 rows=1 loops=1)
   ->  Seq Scan on numbers_large_tbl  (cost=0.00..1791.00 rows=1 width=4) (actual time=3.083..3.085 rows=1 loops=1)
         Filter: (c = 42)
         Rows Removed by Filter: 99999
 Planning Time: 0.049 ms
 Execution Time: 3.096 ms
**/

select 'But that a CTE would generate a very different explain plan.

But doesn''t this look similar?';
explain analyze
with cte as (
        select c, count(c) ct from 
        numbers_large_tbl group by c
    ) 
select c, ct from cte
where c = 42;
/**
                                                     QUERY PLAN                                                     
--------------------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=0.00..1791.01 rows=1 width=12) (actual time=2.363..2.363 rows=1 loops=1)
   ->  Seq Scan on numbers_large_tbl  (cost=0.00..1791.00 rows=1 width=4) (actual time=2.359..2.361 rows=1 loops=1)
         Filter: (c = 42)
         Rows Removed by Filter: 99999
 Planning Time: 0.026 ms
 Execution Time: 2.370 ms
**/

select 'Well, what if I add "as materialized" to my CTE? This is what
used to be the troublesome behavior. CTEs used to materialize by default
and the user couldn''t control it. Now, it does not always use matieraliz-
ation. Materialization is when the results of the CTE are precomputed before
the CTE is used. Can be valuable to prevent recomputing on each use if CTE
is a complex calculation or used many times, but can pose a problem in case
it prevents outer-level constraints (like where c=42) from being "pushed 
down" into the CTE to winnow down the result set it produces. When I explicitly enable
materialization on my CTE, the estimated cost and real time to execute are both much worse,
I don''t get filtering on the leaf node seq scan on numbers_large_tbl 
(this *did* happen in the previous plans, which helped improve their performance).';
explain analyze
with cte as materialized (
        select c, count(c) ct from 
        numbers_large_tbl group by c
    ) 
select c, ct from cte
where c = 42;
/**
                                                              QUERY PLAN                                                              
--------------------------------------------------------------------------------------------------------------------------------------
 CTE Scan on cte  (cost=8947.25..11197.25 rows=500 width=12) (actual time=35.530..40.557 rows=1 loops=1)
   Filter: (c = 42)
   Rows Removed by Filter: 99999
   CTE cte
     ->  HashAggregate  (cost=7166.00..8947.25 rows=100000 width=12) (actual time=17.475..30.338 rows=100000 loops=1)
           Group Key: numbers_large_tbl.c
           Batches: 5  Memory Usage: 8241kB  Disk Usage: 712kB
           ->  Seq Scan on numbers_large_tbl  (cost=0.00..1541.00 rows=100000 width=4) (actual time=0.003..3.713 rows=100000 loops=1)
 Planning Time: 0.029 ms
 Execution Time: 41.389 ms
**/
