# Setup

### ติดตั้ง provider hashicorp และ กำหนด env ของ airflow ให้เปลี่ยนไปใช้ Vault

```
    _PIP_ADDITIONAL_REQUIREMENTS: "apache-airflow-providers-hashicorp"
    AIRFLOW__SECRETS__BACKEND: "airflow.providers.hashicorp.secrets.vault.VaultBackend"
    AIRFLOW__SECRETS__BACKEND_KWARGS: >
      {"url":"http://vault:8200",
       "mount_point":"airflow",
       "connections_path":"connections",
       "variables_path":"variables",
       "config_path":"config",
       "kv_engine_version":2,
       "auth_type":"token",
       "token":"root"}
```

### เพิ่ม service  vault ในไฟล์ compose.yaml

```
  vault:
    image: hashicorp/vault:1.20
    cap_add: [ "IPC_LOCK" ]
    environment:
      VAULT_ADDR: "http://127.0.0.1:8200"
      VAULT_TOKEN: "root"
    ulimits:
      memlock: { soft: -1, hard: -1 }
    command:
      - server
      - -dev
      - -dev-root-token-id=root
      - -dev-listen-address=0.0.0.0:8200
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:8200/v1/sys/health || exit 1"]
      interval: 5s
      timeout: 5s
      retries: 30
      start_period: 5s
    ports:
      - "8200:8200"
```

สร้าง secret engine
```
docker compose exec vault sh -lc 'vault secrets enable -path=airflow -version=2 kv || true'
```


สร้าง Variable
```
docker compose exec vault sh -lc \
  'vault kv put airflow/variables/hello value="world"'
```

สร้าง Connection
```
docker compose exec vault sh -lc \
  'vault kv put airflow/connections/my_postgres_connection conn_uri="postgresql+psycopg2://username:password@host:5432/database"'
```