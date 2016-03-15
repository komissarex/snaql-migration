# snaql-migration
Lightweight SQL schema migration tool, based on [Snaql](https://github.com/semirook/snaql) query builder.

The main idea is to provide ability of describing migrations in raw SQL – every migration is a couple of files: `001-some-migration.apply.sql` and `001-some-migration.revert.sql`

Basic Usage
-----------

Install with pip:

```bash
$ pip install snaql-migration
```

Create some migration files. 
Let's say you have an app to deal with *users*:

```
/apps/users/migrations
    001-create-users.apply.sql
    001-create-users.revert.sql
    002-update-users.apply.sql
    002-update-users.revert.sql
    003-create-index.apply.sql
    003-create-index.revert.sql
```

Notes:
* migrations are sorted in ANSI order, so make sure you are numbering them with lead zeros
* `*.apply.sql` and `*.revert.sql` of the same migration must have equal name

Every migration is just a [Snaql](https://github.com/semirook/snaql) queries container.

001-create-users.apply.sql:
```sql
{% sql 'create_roles' %}
  CREATE TABLE roles (
    id INT NOT NULL,
    title VARCHAR(100),
    PRIMARY KEY (id)
  )
{% endsql %}

{% sql 'create_users', depends_on=['create_roles'] %}
  CREATE TABLE users (
    id INT NOT NULL,
    role_id INT NOT NULL,
    name VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY(role_id) REFERENCES roles (id)
  )
{% endsql %}
```

001-create-users.revert.sql:
```sql
{% sql 'revert_users' %}
  DROP TABLE users;
{% endsql %}

{% sql 'revert_roles', depends_on=['revert_users'] %}
  DROP TABLE roles;
{% endsql %}
```

Then create a simple YAML config file with database connection info and migrations locations:

```yaml
db_uri: 'postgres://test:@localhost/test'

migrations:
  users_app: 'apps/users/migrations'
```

Note: of course, you could describe several apps with different migrations location.

And then just:

```bash
$ snaql-migration --config=config.yml show    # shows all available migrations
```

```bash
$ snaql-migration --config=config.yml apply all    # applies all available migrations in all configured apps
```

```bash
$ snaql-migration --config=config.yml apply users_app/002-update-users    # applies all migrations up to 002-update-users in users_app (inclusive)
```

```bash
$ snaql-migration --config=config.yml revert users_app/002-update-users    # reverts all migrations down to 002-update-users in users_app (inclusive)
```

Supported databases
-------------------
* PostgreSQL through `Psycopg2`
* MySQL through `PyMySQL`