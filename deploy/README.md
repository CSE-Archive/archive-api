# CSE Archive production deploy

This directory is the production stack as code. The VM's `/opt/csearchive`
is a copy of these files plus gitignored state — the repo is the source of
truth.

Two repos build images via GitHub Actions CD (runner-build, shipped with
`docker save | docker load`, see each repo's `.github/workflows/deploy.yaml`):

- **archive-api** → `csearchive-api:latest` (Django + gunicorn; this repo)
- **archive-frontend** → `csearchive-frontend:latest` (nginx serving the
  built Flutter web app)

This stack adds the database, the nginx gateway that terminates the
`api.csearchive.ir` vhost and serves `/media/` off disk, and joins both to
the shared proxy network of the VM's reverse proxy (which owns host ports
80/443) so it can reach them.

## Files

| File | Role |
|---|---|
| `compose.yaml` | the stack: db + api + frontend + web gateway |
| `nginx/web.conf` | gateway vhost (API proxy + `/media/` + CORS) |
| `caddy-sites.conf` | the site blocks appended to the reverse proxy's Caddyfile |
| `.env.example` | every env var, and where each half lives on the VM |
| `backup.sh` | nightly db dump + weekly media tar (cron on the VM) |
| `extract_media.py` | restores the old server's backup zip (fixes the Persian-filename encoding) |

## VM layout

```
/opt/csearchive/            this directory + runtime state
├── compose.yaml            from here
├── nginx/web.conf          from here
├── api.env                 API runtime env (secrets, chmod 600, NOT in git)
├── .env                    only DB_PASSWORD (NOT in git)
├── data/media/             uploaded files (2.6 GB, restored from the backup zip)
├── backups/                archive-backup.zip + temp.backup (restore sources)
/var/backups/csearchive/    nightly dumps + weekly media tars
```

## Daily workflow

Push to `main` in either repo → its Actions workflow builds the image on the
runner, ships it, and runs `docker compose up -d <service>` here. Nothing
else. Rollback = `git revert` + push.

After changing files in THIS directory, sync them to the VM and apply:

```sh
rsync -a deploy/ root@94.184.47.154:/opt/csearchive/
ssh root@94.184.47.154 'cd /opt/csearchive && docker compose up -d'   # picks up conf changes
```

## Fresh-server recovery (runbook)

Prereqs: Ubuntu VM with Docker, the shared reverse proxy stack running
(Caddy owns 80/443), DNS A records for `csearchive.ir` + `api.csearchive.ir` pointing at
the VM (**DNS-only/grey cloud** — Caddy's Let's Encrypt issuance needs to be
reachable directly).

1. **Lay down this directory** at `/opt/csearchive` (rsync above) and create
   the two env files from `.env.example`. Reuse the old production
   `SECRET_KEY` from the archive zip if restoring (signed-data continuity);
   escape literal `$` as `$$` — compose v5 interpolates env files.
2. **Bring up the database**: `cd /opt/csearchive && docker compose up -d db`
3. **Images**: either push to `main` once (CD ships both) or manually
   `docker load` from `docker save` tarballs built anywhere.
4. **Caddy**: append `caddy-sites.conf` to the reverse proxy's Caddyfile
   on the VM (its stack owns ports 80/443; exact path is an operator note,
   deliberately kept out of this public repo), then validate + reload (a
   failed reload leaves the old config serving):
   ```sh
   cd <proxy-stack-dir>
   docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile
   docker compose exec caddy caddy reload  --config /etc/caddy/Caddyfile
   ```
   Certificates issue automatically within minutes of DNS resolving here.
5. **Restore data** (from `backups/` or a nightly dump in
   `/var/backups/csearchive/`):
   ```sh
   # database (custom-format dump):
   docker compose cp temp.backup db:/tmp/ && \
     docker compose exec -T db pg_restore -U csearchive -d csearchive \
       --clean --if-exists --no-owner --no-privileges --exit-on-error /tmp/temp.backup
   # media: extract with the bundled script — the old zip stores Persian
   # filenames without the UTF-8 flag and needs the cp437->UTF-8 fix:
   python3 deploy/extract_media.py /path/to/archive-backup.zip
   ```
6. **Backups**: `cp deploy/backup.sh /usr/local/bin/csearchive-backup &&
   chmod 755 /usr/local/bin/csearchive-backup` and install
   `/etc/cron.d/csearchive-backup` (see the cron section below).
7. **Verify**: `https://csearchive.ir/` renders, `https://api.csearchive.ir/courses/?limit=1`
   returns JSON, `/admin/` login works, and every container of the reverse
   proxy's stack is still healthy — never `down` that stack.

## Backups

- Nightly (cron 04:00 Tehran): `csearchive-db-*.sql.gz` dumps, 14-day retention.
- Weekly: full `media` tar (named by ISO week), 2 copies kept.
- Manual run: `/usr/local/bin/csearchive-backup`
- Restore a db dump:
  ```sh
  gunzip -c csearchive-db-YYYYmmdd-HHMM.sql.gz | \
    docker compose exec -T db psql -U csearchive -d csearchive --single-transaction
  ```
  (plain SQL from pg_dump | gzip — different restore path than the
  custom-format `temp.backup` above.)

Cron file (`/etc/cron.d/csearchive-backup`) — cron fires in the VM's LOCAL
time; shift the hour to suit the box:

```
# CSE Archive nightly backup
SHELL=/bin/sh
17 4 * * * root /usr/local/bin/csearchive-backup
```

## Gotchas learned the hard way

- **compose `$` interpolation**: values with `$` in `api.env` need `$$`.
- **nginx healthchecks**: probe `http://127.0.0.1/` — busybox `wget
  localhost` resolves `::1` (IPv6) and fails against IPv4-only listeners.
- **API boot delay**: the api entrypoint runs collectstatic + migrate
  (~15 s on the 1-vCPU VM) before gunicorn listens; the gateway 502s in
  that window — the CD verify retries for this reason.
- **Persian filenames in the old zip**: stored as cp437-decoded UTF-8;
  `name.encode('cp437').decode('utf-8')` restores them.
- **Flutter builds on the Mac** need the pub mirror env
  (`PUB_HOSTED_URL=https://pub.flutter-io.cn`,
  `FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn`) and SDK 3.16.x.
