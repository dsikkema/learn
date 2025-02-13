 -- TOODO
 -- partial index
 create index active_useres_idx on users (email) where status = 'active'; -- avoid unnecessary data in idx
-- composite index for common queries
 create index users_email_status_idx on users (email, status);
-- covering index for frequently accessed columns
-- in covering index, the idx has all the data needed to execute a particular query, no 
-- need to read rows
create index users_search on users (id,email, status, created_at);

 
