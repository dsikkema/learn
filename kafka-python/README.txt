What I learned here is about using confluent_kafka for the consumer and producer apis for python client. Pretty simple to produce/consume a topic in a loop.

Was interesting that poll() needs a timeout! If no timeout, it will hang waiting when there are no new messages, and ctrl-c won't stop it. Needed to kill the process. And add a timeout.

Kafka used to require zookeeper for running various internals, I guess, but later versions let it use KRaft to manage itself. Claude gave bad docker compose files for kafka, so I found an online tutorial that worked, and just spun up kafka itself in one container using a docker compose file.

I run the scripts with `uv run script.py`. The only dependency I added was `uv add confluent_kafka`.

