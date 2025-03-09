# Test02 Project - Migration Fix Documentation

## The Problem
The project had migration issues with the `Guia_de_transporte` app, specifically:
- A conflict with migration `0007_rename_unidade_guiadetransporte_em_falta_and_more.py`
- The `unidade` column didn't exist in the database but was referenced in the migration

## Solution Steps
1. Created a backup of the problematic migration
2. Created a new fix migration that:
   - Depends on the squashed migration `0001_initial_squashed_0006_add_em_falta_total`
   - Safely adds the missing `em_falta` column if it doesn't exist
3. Applied the fixed migration
4. Created new migrations for any outstanding model changes

## Commands Used
```bash
# List all migrations
python list_migrations.py

# Fix migrations
python fix_migrations.py

# Create new migrations for model changes
python create_new_migrations.py
```

## Lessons Learned
- Always check that columns exist before attempting to rename them in migrations
- Use `python manage.py makemigrations --dry-run` to see what changes will be made
- Back up migrations before deleting them