"""Create angel_productivity and polo_productivity views

Revision ID: 1737083152
Revises: 1737083151
Create Date: 2025-01-17 09:27:12.888390

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '1737083151'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('default',)
depends_on: Union[str, Sequence[str], None] = None

# Alembic revision identifiers
revision = '1737083152'
down_revision = '1737083151'
branch_labels = None
depends_on = '1737083151'

def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE VIEW angel_productivity AS
        SELECT 
            angel.name AS courier,
            COUNT(a.id) AS total_deliveries,
            SUM(CASE WHEN a.data_de_atendimento <= a.data_limite THEN 1 ELSE 0 END) AS on_time_deliveries,
            ROUND(100.0 * SUM(CASE WHEN a.data_de_atendimento <= a.data_limite THEN 1 ELSE 0 END) / COUNT(a.id), 2) AS on_time_percentage
        FROM atendimento a
        JOIN angel ON a.id_angel = angel.id
        WHERE a.data_de_atendimento IS NOT NULL AND a.deleted_at IS NULL
        GROUP BY angel.name
        ORDER BY on_time_percentage DESC;
        """
    )
    op.execute("""
        CREATE OR REPLACE VIEW polo_productivity AS
        SELECT 
            polo.name AS polo,
            TO_CHAR(a.data_de_atendimento, 'Day') AS weekday,
            COUNT(*) AS total_deliveries
        FROM atendimento a
        JOIN polo ON a.id_polo = polo.id
        WHERE a.data_de_atendimento IS NOT NULL AND a.deleted_at IS NULL
        GROUP BY polo, weekday
        ORDER BY total_deliveries DESC;
    """)

def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS angel_productivity;")
    op.execute("DROP VIEW IF EXISTS polo_productivity;")
