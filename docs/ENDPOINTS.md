# Tested endpoints

All endpoints below have been verified against an Oracle Fusion
Applications public demo pod with HTTP Basic Auth.

Base path: `/hcmRestApi/resources/11.13.18.05`

| # | Resource      | Method | Path                              | Example script                |
| - | ------------- | ------ | --------------------------------- | ----------------------------- |
| 1 | Workers       | GET    | `/workers?limit=3`                | `examples/01_get_workers.py`  |
| 2 | Jobs          | GET    | `/jobs?limit=3`                   | `examples/02_get_jobs.py`     |
| 3 | Departments   | GET    | `/departments?limit=3`            | `examples/03_get_departments.py` |
| 4 | Locations     | GET    | `/locations?limit=3`              | `examples/04_get_locations.py` |
| 5 | Grades        | GET    | `/grades?limit=3`                 | `examples/05_get_grades.py`   |

## 1. Workers — `/workers`

Returns person/worker records.

**Key fields**

| Field                    | Type    | Notes                             |
| ------------------------ | ------- | --------------------------------- |
| `PersonId`               | number  | Internal surrogate key            |
| `PersonNumber`           | string  | Business-facing employee number   |
| `DateOfBirth`            | date    | `YYYY-MM-DD`                      |
| `CorrespondenceLanguage` | string  | ISO language code                 |

```bash
GET /hcmRestApi/resources/11.13.18.05/workers?limit=3
```

## 2. Jobs — `/jobs`

Returns job definitions.

**Useful query**: `?q=ActiveStatus=ACTIVE` to filter to active jobs only.

| Field          | Type    | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| `JobCode`      | string  | Business-facing code                   |
| `Name`         | string  | Human-readable job name                |
| `FullPartTime` | string  | `F` = full-time, `P` = part-time       |
| `ActiveStatus` | string  | `ACTIVE` / `INACTIVE`                  |

## 3. Departments — `/departments`

Returns department/organization records, including a link to the
physical location.

| Field          | Type    | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| `DepartmentId` | number  | Internal key                           |
| `Name`         | string  | Department name                        |
| `LocationId`   | number  | Foreign key into `/locations`          |

## 4. Locations — `/locations`

Returns physical locations with addresses.

| Field          | Type    | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| `LocationId`   | number  | Internal key                           |
| `LocationCode` | string  | Business code                          |
| `LocationName` | string  | Display name                           |
| `Country`      | string  | ISO-2 country code                     |

## 5. Grades — `/grades`

Returns grade definitions used for compensation and levelling.

| Field          | Type    | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| `GradeCode`    | string  | Business-facing grade code             |
| `GradeName`    | string  | Display name                           |
| `ActiveStatus` | string  | `ACTIVE` / `INACTIVE`                  |

## Common query parameters

| Param       | Purpose                                                     |
| ----------- | ----------------------------------------------------------- |
| `limit`     | Page size, default 25, max 500                              |
| `offset`    | Zero-based starting row                                     |
| `q`         | Filter, e.g. `q=ActiveStatus=ACTIVE`                        |
| `fields`    | Comma-separated projection, e.g. `fields=JobCode,Name`      |
| `expand`    | Inline child resources, e.g. `expand=assignments`           |
| `onlyData`  | `true` to omit `links` array                                |

See Oracle's official
[REST API reference](https://docs.oracle.com/en/cloud/saas/human-resources/farws/index.html)
for the full, authoritative list of parameters and field definitions.
