<h2>Deployment</h2>

```bash
docker-compose up --build
```

<h2>Migrations</h2>
```bash
alembic upgrade head
```
```bash
alembic revision --autogenerate -m "create table"
```

<h2>Local Testing</h2>
```bash
export TEST_ENV=active
cd backend
pytest tests
```

<h2>Environments</h2>
Prod: http://50.16.210.223/docs

<h2>Figma UI</h2>
https://www.figma.com/file/l8H9Q4ZCd00mEOV9YPLDlP/Ascoach?type=design&node-id=30-16481&mode=design

<h2>Documentation</h2>
https://www.notion.so/AsCoach-a661dedab2334709a7d232e67658b3bb
