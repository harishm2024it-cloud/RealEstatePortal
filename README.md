# Real Estate Portal
# Real Estate Portal

A comprehensive web application for managing real estate properties, built with Flask, SQLAlchemy, and robust cloud-based best practices. This platform facilitates listing, searching, purchasing, and reviewing real estate properties, with a focus on clean architecture, CI/CD, and scalability on Azure.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Architecture](#business-architecture)
- [Conceptual and Logical Models](#conceptual-and-logical-models)
- [System Architecture (MVC & Azure)](#system-architecture-mvc--azure)
- [Tech Stack](#tech-stack)
- [Folder & File Structure](#folder--file-structure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Project Overview

This project provides an end-to-end solution for real estate management. It connects buyers and sellers, enables property listings, and supports a full review/feedback lifecycle—all delivered with a secure, scalable codebase.

---

## Business Architecture

### Key Entities:

- **User**: Buyers and sellers registering and interacting on the platform.
- **Property**: Houses/lands listed for sale by sellers.
- **Review**: Buyer feedback on sellers after transactions.
- **Transaction**: Processes marking the purchase and sale of a property.

### Core Business Processes:

1. **User Registration & Login**
2. **Property Listings by Sellers**
3. **Property Search & Browsing by Buyers**
4. **Buyer-Seller Communication**
5. **Purchase Process**
6. **Review Submission**
7. **Profile Management**

#### Conceptual Flow

```
[User Registration] → [Login] → [Dashboard]
      |                        |
 [Seller]                [Buyer]
   ↓                        ↓
[Property Listing]     [Property Search]
             \           /
       [Property Details]
             |          |
     [Contact Seller] [Purchase Property]
                   \   /
                 [Review Seller]
```

For visuals, see the `business_architecture.md`.

---

## Conceptual and Logical Models

- **User:** UserID, Name, Email, Password (hashed), Role (Buyer/Seller), CreatedAt
- **Property:** PropertyID, SellerID, Title, Price, Location, Status, ListedAt
- **Review:** ReviewID, BuyerID, SellerID, Rating (1-5), Comment, PostedAt
- **Transaction:** TransactionID, BuyerID, SellerID, PropertyID, Amount, TransactionDate

Key relationships:
- 1 seller → many properties
- Many buyers ↔ many properties (via transactions)
- Buyers review sellers (many reviews per seller)

Entity and relationship diagrams are provided in `business_architecture.md`.

---

## System Architecture (MVC & Azure)

### MVC Pattern

- **Model**: SQLAlchemy models (users, properties, reviews) — see `models/`
- **View**: Jinja2 HTML templates (`templates/`), static assets (`static/`)
- **Controller**: Flask routes and business logic (`app.py`)

#### MVC Overview

```
+---------+       +-------------+       +-----------+
|  User   | <-->  | Controller  | <-->  |  Model    |
|Browser  |       | (Flask)     |       | (ORM)     |
+---------+       +-------------+       +-----------+
                      |    |                ^
                      v    v                |
               +----------------------+     |
               |       View (Jinja2)  |     |
               +----------------------+     |
```

### Azure Integration

- Azure App Service: Host Flask application
- Azure SQL Database: Storage of all business data
- Azure Active Directory: User authentication
- Azure Monitor: Diagnostics and logging
- Azure Key Vault: Secure secret management

(See `mvc_architecture.md` for diagrams and deployment flow.)

---

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
- **Frontend**: Jinja2 templates, HTML, CSS (in `static/`)
- **Database**: Azure SQL Database
- **DevOps/Infra**: Azure DevOps, Azure App Service, Azure Key Vault, Azure Monitor
- **CI/CD**: Automated with Azure Pipelines (see `azure-pipelines.yml`)

### Python Requirements (see `requirements.txt`):

```txt
flask
flask-sqlalchemy
flask-login
werkzeug
```

---

## Folder & File Structure

```
Real-estate-portal-file-2/
├── app.py                  # Main Flask app (routes, logic)
├── requirements.txt        # Python dependencies
├── business_architecture.md# Business design docs
├── ci_cd_pipeline.md       # CI/CD, DevOps documentation
├── mvc_architecture.md     # MVC architecture documentation
├── models/                 # SQLAlchemy models
├── static/                 # CSS/JS/static files
├── templates/              # Jinja2 HTML templates
├── tests/                  # Unit tests (run in CI)
├── README.md               # Project documentation
```

---

## CI/CD Pipeline

A robust CI/CD workflow ensures every change is built, tested, and deployed automatically to Azure.

- **Tool**: Azure DevOps Pipelines (`azure-pipelines.yml`)
- **Build**: Installs dependencies and runs unit tests
- **Test**: Runs Python unittests
- **Deploy**: On test success, deploys Flask app to Azure App Service

**Sample Pipeline Stages:**

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
      - task: UsePythonVersion@0
      - script: pip install -r requirements.txt
      - script: python -m unittest discover tests

- stage: Deploy
  jobs:
  - deployment: DeployJob
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
            - task: AzureWebApp@1
```
Full pipeline details are in `ci_cd_pipeline.md`.

---

## Getting Started

### Prerequisites

- Python 3.x
- Azure subscription (for full deployment)
- Pip package manager

### Installation

1. **Clone**
    ```sh
    git clone https://github.com/harishakshay/RealEstatePortal.git
    cd RealEstatePortal/Real-estate-portal-file-2
    ```
2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```
3. **Run App**
    ```sh
    python app.py
    ```

### Running Tests

```sh
python -m unittest discover tests
```

### Deploying to Azure

- See `.azure-pipelines.yml` and `ci_cd_pipeline.md` for DevOps, or deploy directly via Azure App Service using Docker or the Azure CLI.

---

## Contributing

Contributions are welcome! Please open issues to report bugs or request features. For major changes, submit a PR or open an issue for discussion.

---

## License

This project is for educational and demonstration purposes.

---

## Author

Created by [Hemalatha](https://github.com/hemalatha-0307).

---

## References

For further exploration:
- [business_architecture.md](./business_architecture.md)
- [mvc_architecture.md](./mvc_architecture.md)
- [ci_cd_pipeline.md](./ci_cd_pipeline.md)
