# Example Record Payloads

These files are example JSON payloads for local testing:

- `dataset.example.json`
- `msrun.example.json`
- `spectrum.example.json`
- `sample-upload.txt`

## Install nrp-cmd

The upstream `nrp-cmd` README recommends installing it in a dedicated Python
3.12 virtual environment with `uv`:

```bash
uv venv --python=python3.12 nrp-cmd-venv
source nrp-cmd-venv/bin/activate
uv pip install nrp-cmd
```

`nrp-cmd` depends on the system `libmagic` library. On Debian/Ubuntu systems,
install it before installing or running the command:

```bash
sudo apt install libmagic1
```

Check that the command is available:

```bash
nrp-cmd --help
```

See the upstream project for the latest installation notes:
<https://github.com/NRP-CZ/nrp-cmd>

## Create Records

Create records in dependency order. Relation fields point at published record
PIDs, not draft/upload PIDs. A URL like `/dataset/uploads/cqrdq-a9862` is a
draft/upload URL, so `cqrdq-a9862` is not valid for `metadata.dataset.id` in an
MSRun payload.

The example payloads use the file-backed publication path, so each draft must
receive at least one uploaded file before it can be published:

```json
{ "files": { "enabled": true } }
```

Create a dataset record, upload `sample-upload.txt` to the draft in the same
command, store the created record reference as `rec`, then publish it:

```bash
nrp-cmd create record --model dataset \
  examples/dataset.example.json \
  examples/sample-upload.txt '{"title":"My file"}' \
  --set rec

nrp-cmd publish record @rec
```

After publication, copy the published dataset record ID from the publish
response or the published record URL into `examples/msrun.example.json` at
`metadata.dataset.id`:

```json
"id": "REPLACE_WITH_PUBLISHED_DATASET_RECORD_ID"
```

Create and publish the MSRun the same way:

```bash
nrp-cmd create record --model msrun \
  examples/msrun.example.json \
  examples/sample-upload.txt '{"title":"My file"}' \
  --set rec

nrp-cmd publish record @rec
```

After publication, copy the published MSRun record ID into
`examples/spectrum.example.json` at `metadata.msrun.id`, and make sure
`metadata.dataset.id` also matches the published dataset record:

```json
"id": "REPLACE_WITH_PUBLISHED_MSRUN_RECORD_ID"
```

Finally create and publish the spectrum:

```bash
nrp-cmd create record --model spectrum \
  examples/spectrum.example.json \
  examples/sample-upload.txt '{"title":"My file"}' \
  --set rec

nrp-cmd publish record @rec
```