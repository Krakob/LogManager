# Spiral Knights guild log managers
The log manager is a script which provides tools for managing Spiral Knights guild logs in various ways. The script is also useable as a module in other scripts.

## Planned features:
* Log to Excel
** Replace all non-quoted commas with tabs.
** Make datetime format Excel compatible.
* Time period extraction
** Extract all data between two points of time in a log.
* Log combiner
** Compile all logs in a directory to a single log file, sorted and formatted properly without duplicates.
** Allow appending to an already existing log in case of missing files.
* Log to HTML
** Convert a log file to an HTML table.
** Work out filtering and whatnot through JS later on.
* Namechange handler
** Change all  names in a group of names (defined in other file) to be the same, to avoid confusion due to name changes.\*
* Treasury deposits compiler
** Compile all donations to treasury from all users to list of items and amounts.
** Compile all donations of all types to a list of players and amounts.
* Storage interaction compiler
** Same as above but for storage.
** Support for withdrawals and the various storages as well.

\* Name changes are not reflected in logs. For example, a user can deposit 5 CR as “Bob”, then change to “Alice”, and deposit 10 CR. The 5 CR donation will be listed under “Bob” even after the name change, while the 10 CR donation will be listed under “Alive”.