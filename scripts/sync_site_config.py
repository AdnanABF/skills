#!/usr/bin/env python3
"""Validate and selectively merge a downloaded site configuration (no Frappe dependency)."""

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile


class ConfigError(ValueError):
	"""Validation failure whose message names keys only, never configuration values."""


PROTECTED_KEYS = {
	"host_name", "developer_mode", "maintenance_mode", "pause_scheduler",
	"disable_scheduler", "scheduler_tick_interval", "dns_multitenant",
	"serve_default_site", "restart_supervisor_on_update", "restart_systemd_on_update",
	"background_workers", "gunicorn_workers", "http_port", "webserver_port",
	"socketio_port", "file_watcher_port", "live_reload", "auto_update",
	"logging", "monitor", "bench_id", "frappe_user", "root_password",
}


def load_config(path: Path, label: str) -> dict:
	try:
		with path.open() as source:
			data = json.load(source)
	except (json.JSONDecodeError, UnicodeDecodeError):
		# Decoder messages can echo source content, so report the location only.
		raise ConfigError(f"{label} configuration is not valid JSON") from None
	if not isinstance(data, dict):
		raise ConfigError(f"{label} configuration must be a JSON object")
	return data


def selected_config(remote: dict, keys: list[str]) -> dict:
	selected = {}
	for key in dict.fromkeys(["encryption_key", *keys]):
		if key in PROTECTED_KEYS or key.startswith(("db_", "redis_", "socketio_", "mariadb_")):
			raise ConfigError(f"Protected local configuration key cannot be synced: {key}")
		if key not in remote:
			raise ConfigError(f"Required remote configuration key is missing: {key}")
		selected[key] = remote[key]
	key = selected["encryption_key"]
	valid = False
	if isinstance(key, str):
		try:
			valid = len(base64.b64decode(key, altchars=b"-_", validate=True)) == 32
		except (ValueError, TypeError):
			valid = False
	if not valid:
		raise ConfigError("Remote encryption_key must be a valid Fernet key")
	return selected


def atomic_write(path: Path, data: dict) -> None:
	fd, temporary = tempfile.mkstemp(prefix=".site-config-", dir=path.parent)
	try:
		with os.fdopen(fd, "w") as output:
			json.dump(data, output, indent=2)
			output.write("\n")
			output.flush()
			os.fsync(output.fileno())
		os.replace(temporary, path)
	finally:
		if os.path.exists(temporary):
			os.unlink(temporary)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("action", choices=["validate", "backup", "apply"])
	parser.add_argument("--remote", type=Path, required=True)
	parser.add_argument("--local", type=Path, required=True)
	parser.add_argument("--key", action="append", default=[])
	args = parser.parse_args()
	try:
		selected = selected_config(load_config(args.remote, "Remote"), args.key)
		local = load_config(args.local, "Local") if args.local.exists() else {}
		if args.action == "backup":
			if not args.local.is_file():
				raise ConfigError("Local site configuration is missing")
			stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
			fd, name = tempfile.mkstemp(prefix=f"site_config.pre-sync-{stamp}-", suffix=".json", dir=args.local.parent)
			with os.fdopen(fd, "wb") as backup:
				backup.write(args.local.read_bytes())
			print(f"Local configuration backup: {Path(name).name}")
		elif args.action == "apply":
			if not args.local.is_file():
				raise ConfigError("Local site configuration is missing")
			atomic_write(args.local, {**local, **selected})
		print(f"Configuration {args.action}: {', '.join(selected)}")
	except ConfigError as error:
		# Messages name keys or locations only; they never include configuration values.
		parser.exit(1, f"Configuration sync failed: {error}.\n")
	except (ValueError, OSError):
		# Unexpected decoder and OS errors can contain sensitive source content.
		parser.exit(1, "Configuration sync failed: check JSON, required keys, encryption key, protected keys, and file permissions.\n")


if __name__ == "__main__":
	main()
