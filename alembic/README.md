
## Paths:
* Configuration (basic) for alembic in project/alembic.ini
* Configuration (Specific) for alembic in project/src/env.py
* Versions of updates for DB in project/alembic/versions (Push this every time)
* Schema of DB in project/src/model (add new tables in project/src/model/__init__.py)

## Commands:
* alembic current - Show current version and basic check of functionality
* alembic history - Show history of updates
* alembic revision --autogenerate -m "Name of migration" - Create new migration (Equivalent to commit)
* alembic upgrade head - Migrate to latest version (Equivalent to push)
* alembic downgrade -1 - Migrate to previous version (Equivalent to rollback)