# Postman collection

A Postman collection for the five tested endpoints will be added to this
folder as `oracle-hcm-rest-api-starter.postman_collection.json`.

Planned contents:

| Folder      | Request                    | Method | Path                              |
| ----------- | -------------------------- | ------ | --------------------------------- |
| Workers     | List workers (limit 3)     | GET    | `/workers?limit=3`                |
| Jobs        | List active jobs           | GET    | `/jobs?limit=3&q=ActiveStatus=ACTIVE` |
| Departments | List departments           | GET    | `/departments?limit=3`            |
| Locations   | List locations             | GET    | `/locations?limit=3`              |
| Grades      | List grades                | GET    | `/grades?limit=3`                 |

The collection will use Postman environment variables (`{{base_url}}`,
`{{username}}`, `{{password}}`) so credentials are never stored inside
the shared JSON export.
