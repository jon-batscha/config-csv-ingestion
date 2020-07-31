# config-driven-csv-ingestion

At a high-level, this package enables a user to send events/profiles directly to Klaviyo via Python3 using just a CSV file, a config, and a few lines of code. This package is a custom addition the Sales Engineering Team built atop the productized API to serve customers with unique data needs.

## Component files:

### `utils.py`

This file defines a few functions, (some intended for the user, along with helper functions). Using these pre-built functions, a user can send custom events to klaviyo from a CSV at scale in just a few lines of code (see: `sample_script.py`)

NOTE: do not make any changes to `utils.py`.

### `config.py`

This file allows the user to set their data mapping and public keys, that the script can then use to send data from the CSV to Klaviyo. The config can have multiple mapping dictionaries, each with keys (Klaviyo property names) mapping to values (CSV headers). The config is set to conform to the example data.

NOTE: change the public_key to your account's, and update the event/profile mappings as needed to conform to your CSV.

### `sample_script.py`

This file contains a sample script that:
1. generates event and profiles payloads from `sample_orders.csv`
2. send those payloads to klaviyo using all cores

### `sample_orders.csv`

Sample data illustrating placed orders.

## Caveats

- Merging data from different CSVs
    - This package assumes that all data for a given EVENT is contained in a given row of the csv; any merging of disparate tables needs to be done upstream of this package. For an automated workflow that can help you with this, see 
    - PROFILE properties can be sent piecemeal. For example: if you have one csv that has placed order events with a shipping address, you can use that to update a user's address, even if you are using another table to update the rest of the the user's info (phone, name, etc)
- Config Formatting
    - Each Event/Profile mapping uses the standard python dictionary format (follow example in `config.py`)
    - each config key and value must be a string (no boolean/None type allowed)
    - Events and profiles must have `$email` set
    - Events must have `event` set
    - Additionally, we STRONGLY suggest to set the following properties for events:
        - `time`
        - `$event_id`
- Timestamps:
    - Every event in Klaviyo must have a `'time'` attribute; profile properties do not 
    - Klaviyo accepts timestamps in either of the following formats: `ISO string` or `UNIX timestamp`; other formats will cause errors
    - If there is no `'time'` attribute in your csv that is mapped in your config, this code will add the current timestamp (using the computer's local time) to any event you send; regardless, it is highly incouraged to set an actual time field
- Duplicate events
    - Klaviyo de-dupes events that have the same `'event'`, `'$email'`, `'timestamp'`; for this reason, we advise you to include a unique `'$event_id'` to every event (most CRM's do this by default)
    - If the config has no `'$event_id'` set, this package will automatically add one using the following formula: `abs(hash(string(payload)))`; for this reason, events that are identical (considering only the mapped fields!) will have the same hash and thus will be de-duped
- Event/Profile Properties
    - Certain properties enable pre-built functionality in Klaviyo
        - we recommend using the naming conventions listed here: https://help.klaviyo.com/hc/en-us/articles/115005084927-Template-Tags-and-Variable-Syntax#klaviyo-special-properties18


## Further Available Automations
- From Snowflake: Reach out to our Sales Eng Team; we have a working solution that is in the process of being further documented/productized for easy sharing
- Automatic ingestion of data triggered by file upload: Reach out to the Sales Eng Team; we have a working solution that is in the process of being further documented/productized for easy sharing

## System Reqs

This package requires Python3 + `pip install requests`


