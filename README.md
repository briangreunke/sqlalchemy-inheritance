# Class Inheritance with SQLAlchemy

This is an example of "[Joined Table Inheritance](https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance)"

In this case the database will have three tables to segment "users":

1. A base `users` table which will store the columns in the model definition for `User` including the `type` column
2. A `participant` table which will store the participant `id` (which has a foreign key constraint to the `user` table) and the specified attributes in the `participant` model (e.g. `email_address`)
3. A `host` table which will store the host `id` (which has a foreign key constraint to the `user` table) and the specified attributes in the `host` model (e.g. `website`)

For example:

1. Create a new participant with a `username=peter` and `email_address=peter@foo.bar`.
- The `user` table will have a row with two columns: `id`: `1`, and `type`: `participant`
- The `participant` table will have a new row with two columns `id`: `1` and `email_address`: `peter@foo.bar` 

(**Note**: both `id` columns have the same value because of the foreign key constraint)

## Querying

- Querying for all `Users` will return both `Participant` and `Host` objects
- Querying for all `Participants` will return **ony** `Participant` objects (and the same for `Host`)