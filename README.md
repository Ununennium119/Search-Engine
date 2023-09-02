# Search-Engine

Simple search engine answering queries with one wildcard.

Runs queries in `input.txt` on docs and writes doc indexes sorted by number of matches (most match first) in the `result.txt`.
If number of matches in all docs are 0, -1 will be written in `result.txt`.

Queries should have exactly one wildcard in form of `\S*`.
