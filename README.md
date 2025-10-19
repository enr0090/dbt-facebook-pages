# Facebook Pages dbt Transformation Models

A comprehensive dbt project that transforms raw Facebook Pages data into analytics-ready models, providing clean, tested, and documented data marts for business intelligence and reporting.

## 🚀 Features

- **Production-Ready Models**: Well-tested transformation logic for Facebook Pages data
- **Comprehensive Documentation**: Every model and column documented
- **Data Quality Tests**: Extensive testing to ensure data reliability
- **Modular Design**: Staging and mart layers following dbt best practices
- **Dashboard Ready**: Models optimized for BI tools and reporting

## 📊 Data Models

### Staging Models (`staging/`)
Clean and standardize raw data from the DLT extraction:

- `stg_facebook_pages__page` - Cleaned page information
- `stg_facebook_pages__post_history` - Standardized post data
- `stg_facebook_pages__daily_page_metrics_total` - Page metrics by day
- `stg_facebook_pages__lifetime_post_metrics_total` - Post performance metrics

### Mart Models
Business-ready analytics models:

- `facebook_pages__pages_report` - Comprehensive page analytics dashboard
- `facebook_pages__posts_report` - Post performance and engagement analysis

## 🛠 Quick Start

### Prerequisites

- Python 3.8+
- dbt-core and dbt-duckdb
- Raw Facebook Pages data (from DLT extraction pipeline)

### Installation

1. **Clone and setup environment:**
   ```bash
   git clone <repository>
   cd dbt-facebook-pages
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install dbt dependencies:**
   ```bash
   dbt deps
   ```

3. **Configure database connection:**
   ```bash
   # Edit .dbt/profiles.yml with your database connection details
   # Default is configured for DuckDB
   ```

4. **Run the models:**
   ```bash
   make pipeline
   ```

## 🏃‍♂️ Usage

### Make Commands (Recommended)

```bash
# Run the complete dbt pipeline
make pipeline

# Individual operations
make run             # Run all models
make test            # Run all tests
make docs            # Generate and serve documentation

# Development workflow
make run-staging     # Run only staging models
make run-marts       # Run only mart models
make compile         # Compile without running

# Setup and maintenance
make dev-setup       # Setup development environment
make check-connection # Test database connection
make clean           # Clean build artifacts
```

### Manual dbt Commands

```bash
# Run all models
dbt run

# Run specific models
dbt run --select staging
dbt run --select facebook_pages__pages_report

# Test data quality
dbt test

# Generate documentation
dbt docs generate && dbt docs serve
```

## 📁 Project Structure

```
dbt-facebook-pages/
├── dbt_project.yml                 # dbt project configuration
├── packages.yml                    # dbt package dependencies
├── Makefile                        # Easy management commands
├── requirements.txt                # Python dependencies
├── .dbt/
│   └── profiles.yml                # Database connection settings
├── models/
│   ├── facebook_pages.yml          # Model documentation and tests
│   ├── facebook_pages__pages_report.sql    # Pages analytics mart
│   ├── facebook_pages__posts_report.sql    # Posts analytics mart
│   ├── staging/
│   │   ├── stg_facebook_pages.yml          # Staging model docs/tests
│   │   ├── stg_facebook_pages__page.sql
│   │   ├── stg_facebook_pages__post_history.sql
│   │   ├── stg_facebook_pages__daily_page_metrics_total.sql
│   │   └── stg_facebook_pages__lifetime_post_metrics_total.sql
│   └── intermediate/
│       └── int_facebook_pages__latest_post.sql
├── macros/
│   └── staging/                    # Custom SQL macros
├── docs/                           # Generated documentation
└── target/                         # dbt build artifacts
```

## ⚙️ Configuration

### Database Connection

The project is configured for DuckDB by default. Update `.dbt/profiles.yml` for other databases:

```yaml
facebook_pages:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: 'facebook_pages_pipeline.duckdb'
      schema: 'main'
```

### Data Sources

Configure your data sources in `models/staging/src_facebook_pages.yml`:

```yaml
sources:
  - name: facebook_pages
    description: Raw Facebook Pages data from DLT pipeline
    tables:
      - name: page
      - name: post_history
      - name: daily_page_metrics_total
      - name: lifetime_post_metrics_total
```

## 📈 Analytics & Reporting

### Pages Report (`facebook_pages__pages_report`)
Comprehensive page analytics including:
- Page information and metadata
- Daily engagement metrics
- Growth trends and performance indicators
- Aggregated post performance

### Posts Report (`facebook_pages__posts_report`)
Detailed post-level analysis featuring:
- Individual post performance
- Engagement rates and metrics
- Content type analysis
- Publishing patterns and optimal timing

### Custom Analytics
Build on top of the staging models for custom analysis:

```sql
-- Example: Top performing posts by engagement
SELECT 
    post_id,
    post_message,
    total_engagement,
    engagement_rate
FROM {{ ref('facebook_pages__posts_report') }}
ORDER BY total_engagement DESC
LIMIT 10;
```

## 🔍 Data Quality & Testing

The project includes comprehensive tests:

- **Source freshness**: Ensures data is up-to-date
- **Uniqueness tests**: Validates primary keys
- **Not null tests**: Ensures required fields are populated
- **Relationship tests**: Validates foreign key relationships
- **Custom tests**: Business logic validation

Run tests with:
```bash
make test
```

## 📖 Documentation

Generate and view comprehensive documentation:

```bash
make docs
```

This includes:
- Data lineage diagrams
- Column-level documentation
- Test coverage reports
- Model dependencies

## 🔗 Data Pipeline Integration

This dbt project is designed to work with extracted data from:
👉 **[dlt-facebook-pages](../dlt-facebook-pages)** - Extract Facebook Pages data with DLT

### Complete Workflow

1. **Extract**: Use the DLT pipeline to extract raw data
2. **Transform**: Run this dbt project to create analytics models
3. **Analyze**: Connect BI tools to the transformed data

```bash
# In dlt-facebook-pages repository
make pipeline

# In dbt-facebook-pages repository (this repo)
make pipeline
```

## 🛠 Development

### Environment Setup
```bash
make dev-setup
source venv/bin/activate
```

### Development Workflow
1. Make changes to models
2. Test changes: `make compile`
3. Run models: `make run`
4. Test data quality: `make test`
5. Update documentation: `make docs-generate`

### Adding New Models
1. Create SQL file in appropriate directory
2. Add documentation in schema.yml files
3. Add tests for data quality
4. Update this README if needed

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   make check-connection
   ```

2. **Missing Source Data**
   - Ensure the DLT pipeline has run successfully
   - Check that the database path in profiles.yml is correct

3. **Model Compilation Errors**
   ```bash
   make compile
   ```

4. **Test Failures**
   - Review test output for specific failures
   - Check data quality in source tables

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Previous Step**: Extract data with the **[dlt-facebook-pages](../dlt-facebook-pages)** project before running these transformations.