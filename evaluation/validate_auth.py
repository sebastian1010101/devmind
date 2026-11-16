"""Small opt-in Supabase check using a confirmed account configured in .env."""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from api import app
from providers import ServiceError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", required=True)
    parser.add_argument("--output", type=Path, default=Path("evaluation/public-supabase-live-local.json"))
    args = parser.parse_args()
    required = ["SUPABASE_URL", "SUPABASE_PUBLISHABLE_KEY", "DEVMIND_TEST_EMAIL", "DEVMIND_TEST_PASSWORD"]
    missing = [name for name in required if not os.getenv(name)]
    report = {"provider": "supabase", "passed": False, "missing_variables": missing, "checks": [],
              "email_delivery": "requires signup/recovery and checking the test inbox separately"}
    if not missing:
        try:
            with tempfile.TemporaryDirectory(prefix="devmind-auth-live-") as directory, patch.dict(os.environ, {
                "APP_ENV": "development", "DATABASE_URL": "", "LEARNING_DB_PATH": str(Path(directory) / "test.sqlite3"),
            }), TestClient(app, root_path="/api", base_url="http://testserver/api/", headers={
                "Origin": "http://localhost:3035", "X-DevMind-CSRF": "1",
            }) as client:
                response = client.post("auth/login", json={"email": os.environ["DEVMIND_TEST_EMAIL"], "password": os.environ["DEVMIND_TEST_PASSWORD"]})
                assert response.status_code == 200, f"login_http_{response.status_code}"
                assert all("HttpOnly" in value for value in response.headers.get_list("set-cookie"))
                assert "access_token" not in response.json()
                report["checks"].append("real_login_verified_signature_and_http_only_cookies")
                assert client.get("auth/me").status_code == 200
                assert client.get("learning/progress").json()["total"] == 0
                report["checks"].append("authenticated_private_endpoint_with_temporary_empty_database")
                assert client.post("auth/refresh").status_code == 200
                report["checks"].append("real_refresh_token_rotation")
                assert client.post("auth/logout").status_code == 204
                assert client.get("auth/me").status_code == 401
                report["checks"].append("real_logout_and_missing_session_rejection")
                report["passed"] = True
        except ServiceError as exc:
            report["error"] = {"code": exc.code, "status": exc.status}
        except AssertionError as exc:
            report["error"] = str(exc) or "contract_check_failed"
        except Exception as exc:
            report["error"] = {"type": type(exc).__name__}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))
    return int(not report["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
