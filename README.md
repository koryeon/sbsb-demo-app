# SBSB Demo App: Web + PostgreSQL

FastAPI 웹 API와 PostgreSQL을 함께 사용하는 데모 프로젝트입니다. `DATABASE_URL`을 RDS 주소로 바꾸면 ECS Fargate + RDS 구성으로 배포할 수 있습니다.

## 로컬 실행

```bash
docker compose up --build
```

- 웹 API: <http://127.0.0.1:8000>
- 헬스체크: <http://127.0.0.1:8000/health>
- 메시지 목록: <http://127.0.0.1:8000/messages>

메시지 생성 예시:

```bash
curl -X POST http://127.0.0.1:8000/messages \
  -H 'Content-Type: application/json' \
  -d '{"text":"SBSB deployment works"}'
```

`DATABASE_URL`이 있으면 PostgreSQL을 사용하고, 별도 설정 없이 실행하면 SQLite 파일을 사용합니다. 운영 환경에서는 비밀번호가 포함된 URL을 저장소에 커밋하지 말고 Secrets Manager 또는 Key Vault로 주입하세요.
