Couch-style data versioning in sqlite
========
Draft

How do we retrieve old versions of data conveniently and efficiently?

CouchDB approach
---------
Couch documents have an `_id` and a `_rev`. When updating a document,
you specify the `_id` and the `_rev` of the version that you have.
You are not allowed to update it if the `_rev` is not the most recent one;
this ensures that changes are not overwritten.

If Couch stores documents with the same `_id` but different `_rev`s
and with the links between `_rev`s, it can retrive old versions.

With some abstraction, this paradigm becomes a convenient form of
distributed data version control.

SQLite implementation
--------------
Not everyone likes Couch as much as I do, and ScraperWiki uses SQLite,
so I've been making SQLite feel more like Couch. How do we put this
data version control in couch?

Let's start by trying to version one table that does not reference
other tables.

Create the table, and create a unique index on `_id` and `_rev`.

    CREATE TABLE foo (
      _id INTEGER, _currentrev INTEGER, _previousrev INTEGER,
      bar INTEGER, baz TEXT,
      FOREIGN KEY (_previousref) REFERENCES foo(_currentrev)
    );
    CREATE UNIQUE INDEX version ON foo (_id, _currentrev);

To get the latest version, select by `_id` and retrieve only
the highest `_previousrev`.

    SELECT * FROM foo GROUP BY _id -- and something about the version

Rather than updating rows, insert new rows that reference
old `_rev`s; for example, this is how you revise the record
for `_id` 3, setting `foo` to 42 and `baz` to "answer".

    INSERT INTO foo (3, 38, 37, 42, "answer");

When combining two database files that have gotten out of sync,
find the discrepencies and add a newer `_currentrev` that merges
the changes.

    -- Figure this out.

Simplify
-------------

Let's write custom SQLite functions to simplify this retrieval.

    SELECT * FROM foo WHERE version(*) = 12

And let's allow you to specify tags.

    SELECT * FROM foo WHERE version(*) = "master";
    SELECT * FROM foo WHERE version(*) = "0.2.1";
