# Entity Relationship Diagram

```mermaid
---
title: Lottery Number Generator
---
erDiagram
    GENERATION {
        uuid guid PK
        integer unique_identifier UK
        integer from
        integer to
        date created_at
    }

    NUMBER {
        uuid guid PK
        uuid generation_guid FK
        uuid color_guid FK
        integer number
    }

    COLOR_ENUM {
        uuid guid PK
        string color UK
    }

    GENERATION ||--|{ NUMBER : has
    NUMBER }o--|| COLOR_ENUM : has
```
COLOR_ENUM[^1]
[^1]: The decision for creating color enum as a table is for DBMS compability reasons (specifically SQLite3), in DBMS like PostgreSQL we could just use a ENUM field type
