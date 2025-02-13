/**
Note: macos, 64 bit, apple sillicon, running postgres 17.2 docker container.

The particular choice of plan that's run may be unpredictable and depend on
environment details or even random chance. The ANALYZE command, which runs
periodically as part of autovacuum (which is what cleans up old rows (which
don't actually get deleted from disk when they're deleted, but just marked
as deleted)), uses random sampling to generate statistics about a table, and
uses these statistical results to inform the "cost" estimates which the planner
tries to minimize. Different random samplings, or whether the autovacuum has
even been run or not, may then affect which plan is chosen.

So I've commented in the plans I've gotten when I've run these queries myself.
**/

-- prime the ANALYZE statistics
ANALYZE numbers_large_tbl;
ANALYZE numbers_small_tbl;
commit; -- idk just in case need to commit the analyze statistics lol
select 'seq scan';
EXPLAIN
select * from numbers_small_tbl where id > 10;
/**
                            QUERY PLAN                             
-------------------------------------------------------------------
 Seq Scan on numbers_small_tbl  (cost=0.00..2.25 rows=91 width=12)
   Filter: (id > 10)

Notes:
- just iterate over all rows, in order of how they're stored on disk.
- not using index even though it COULD be used! We could have used
   the index to find the addresses of rows where id > 10, but didn't. 
- Postgres stores data in blocks/pages (interchangeable). A TID (tuple ID) is
  an address to where a row is stored, including the block that stores it. A
  block only contains data from one type of table, and has a reference to the
  next block (in other words they form a kind of linked list). A sequential
  scan traverses this linked list.
- index imposes two costs which, depending on data size
   and proportion of the rows which are expected to match the filter (note:
   this is based on ANALYZE stats), may make it less attractive than just
   scanning and filtering.
    - extra IO operation to read index data structure itself
    - reading disk nonsequentially is a huge negative. Sequential reading
      of disk is hyperoptimized and aggressively prefetched at multiple different
      layers of OS and hardware.
- theoretically, there are optimizations like ordering the TIDs by block location
  before reading from disk, but that negates rapid-return result streaming ability.
  You have to wait for all TIDs to be read from index before the scan is even allowed
  to start returning, and this could mean memory overruns not to mention latency.
- alternately, with the sequential scan, there's a very high chance of taking adv-
  antage of caching, optimizations, and prefetching associated with reading sequent-
  ial blocks. Even if this means having to check, and filter out, some rows which we
  could have eliminated off the bat with an index scan over a fancy sorted b-tree
  data structure, or even read some blocks that don't even have a matching row in
  them, this could be worth it.
- especially, consider the advantage associated with scanning through a whole block
  that was retrieved in one IO operation rather than finding id=11 from the index
  in this block, then later coming back to this block to get id=99, and doing an
  extra IO operation you could have avoided.
**/

select 'seq scan for one-row match';
EXPLAIN
select * from numbers_small_tbl
where id = 5;
/**
                            QUERY PLAN                            
------------------------------------------------------------------
 Seq Scan on numbers_small_tbl  (cost=0.00..2.25 rows=1 width=12)
   Filter: 

Note:
- It's not just percent of matched rows that makes a difference for seq vs
  index: total row number matters too, smaller table still gives seq scan
  even when querying for 1 unique row.
**/

select 'Index scan';
EXPLAIN
select * from numbers_large_tbl
where id between 10 and 20;

/**
                                            QUERY PLAN                                            
--------------------------------------------------------------------------------------------------
 Index Scan using numbers_large_tbl_pkey on numbers_large_tbl  (cost=0.29..8.51 rows=11 width=12)
   Index Cond: ((id >= 10) AND (id <= 20))

Notes:
 - using index scan on the primary key's index. It helps that there's more data in this table and that
   I'm retrieving a lesser portion of it.
**/

select 'seq scan again';
EXPLAIN
select * from numbers_large_tbl
where id between 10 and 60000;
/**
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Seq Scan on numbers_large_tbl  (cost=0.00..2041.00 rows=59641 width=12)
   Filter: ((id >= 10) AND (id <= 60000))

Note:
- it's a larger table but a greater proportion of rows will match, making
seq scan once more attractive
**/

select 'sort from seq scan';
EXPLAIN
select * from numbers_small_tbl
where id between 10 and 20
order by id;
/**
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Sort  (cost=2.69..2.72 rows=11 width=12)
   Sort Key: id
   ->  Seq Scan on numbers_small_tbl  (cost=0.00..2.50 rows=11 width=12)
         Filter: ((id >= 10) AND (id <= 20))
Notes:
 - The topmost Node doesn't have an arrow.
 - every node below the topmost node has an arrow.
 - bottommost nodes are "scans" that return something like set of rows
 - Line indented just past a node is an attribute describing that node (e.g. Filter, Sort Key)
 - Nodes use nodes beneath as "input arguments" (good example of this will be Nested Loop node, 
   seen later)
 - first do seq scan, then that's input into the Sort node (sorted on id). 
**/
select 'no sort from index scan';
EXPLAIN
select * from numbers_large_tbl
where id between 10 and 20
order by id;
/**

                                            QUERY PLAN                                            
--------------------------------------------------------------------------------------------------
 Index Scan using numbers_large_tbl_pkey on numbers_large_tbl  (cost=0.29..8.51 rows=11 width=12)
   Index Cond: ((id >= 10) AND (id <= 20))

The index is sorted, so the rows scanned from it are sorted already, meaning there's
no need to sort them.
**/

select 'Inner join: hash join happens';
EXPLAIN
select *
from
  numbers_small_tbl t1 join
  numbers_large_tbl t2 on t1.id = t2.id;
/**
                                                    QUERY PLAN                                                    
------------------------------------------------------------------------------------------------------------------
 Merge Join  (cost=5.64..10.65 rows=100 width=24)
   Merge Cond: (t2.id = t1.id)
   ->  Index Scan using numbers_large_tbl_pkey on numbers_large_tbl t2  (cost=0.29..3148.29 rows=100000 width=12)
   ->  Sort  (cost=5.32..5.57 rows=100 width=12)
         Sort Key: t1.id
         ->  Seq Scan on numbers_small_tbl t1  (cost=0.00..2.00 rows=100 width=12)

Note:
seq scan the smaller table, sort it by id. then index scan the larger table: this inherently
produces a sorted scan. Two sorted sequences can be merge joined easily (imagine the algorithm
traversing up both sequences inside one loop, constantly checking with value of the two is
less, equal, or greater than the other)
**/

select 'Inner join: merge join happens';
EXPLAIN
select *
from
  numbers_large_tbl t1 join
  numbers_large_tbl t2 on t1.id = t2.id;
/**
                                       QUERY PLAN                                        
-----------------------------------------------------------------------------------------
 Hash Join  (cost=2791.00..4594.51 rows=100000 width=24)
   Hash Cond: (t1.id = t2.id)
   ->  Seq Scan on numbers_large_tbl t1  (cost=0.00..1541.00 rows=100000 width=12)
   ->  Hash  (cost=1541.00..1541.00 rows=100000 width=12)
         ->  Seq Scan on numbers_large_tbl t2  (cost=0.00..1541.00 rows=100000 width=12)

Note:
seq scan to build a map which
maps id to TID. Then seq scan the large table (no filter: we want to hit every row
therefore index scan has no benefit) checking if those ids are in the map (by computing
hash), and if so, then both these rows are added to the result set (and the map contains
the TID already for the first row that got put into the map so it can be easily located and read)
**/

select 'nested loop';
EXPLAIN
select *
from 
  numbers_large_tbl t1 join
  numbers_large_tbl t2 on t1.id = t2.id
where
  t1.b < t2.c and t2.c < 50;
/**
                                                QUERY PLAN                                                
----------------------------------------------------------------------------------------------------------
 Nested Loop  (cost=0.29..2183.12 rows=17 width=24)
   ->  Seq Scan on numbers_large_tbl t2  (cost=0.00..1791.00 rows=50 width=12)
         Filter: (c < 50)
   ->  Index Scan using numbers_large_tbl_pkey on numbers_large_tbl t1  (cost=0.29..7.83 rows=1 width=12)
         Index Cond: (id = t2.id)
         Filter: (b < t2.c)
Note:
Nested Loop's two child nodes are: the first one is the "outer" loop. Then, for each item produced
by that outer loop (in this case, "for each t2") then run the second child node: the innder loop,
which may use information from the current outer loop row (t2).

In this case, since t2.c < 50 is a very tight constraint and few rows will match it (again based on statistics
precomputed and known to the planner), one of our two loops can be small, so Nested Loop is a bit more attractive
than it would be if the WHERE clause allowed more rows.

So the outer loop is seq scan on t2 checking c<50. 
Inner loop takes each of those t2 and loops over the index scan over t1. It is specifically scanning 
for where the id matches t2 (this is in "Index Cond" because it can be determined purely from the index
itself, without actually having to read the row tuple), and where t1.b < t2.c (this is in "Filter" and not
Index Cond because it requires reading the actual row, not just the index).

In other words:

for each t2 in [the seq scan of t2, filtering on c < 50]:
  read the whole row for t2
  for each t1 in [the index scan of t1, where the indexed id = t2.id)]:
    read the whole row for t1
    if (t1.b < t2.c):
      add the joined t1,t2 row to the result set.
**/


/**
TOODO:
bitmap index scan: don't go to disk to read the actual rows. just get the bitmap.
You can AND/OR that with other bitmaps, and then potentially have fewer trips 
to the disk to have to make.

**/