"""Test data

Revision ID: a80e90973592
Revises: d4b5f056a576
Create Date: 2026-02-08 22:21:26.789665

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a80e90973592'
down_revision: Union[str, Sequence[str], None] = 'd4b5f056a576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind())
    
    activities_table = meta.tables['activities']
    buildings_table = meta.tables['buildings']
    organizations_table = meta.tables['organizations']
    organization_activities_table = meta.tables['organization_activities']
    
    op.bulk_insert(activities_table, [
        {'name': 'Еда', 'parent_id': None},
        {'name': 'Автомобили', 'parent_id': None},
        {'name': 'IT', 'parent_id': None},
    ])
    
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT id, name FROM activities WHERE name IN ('Еда', 'Автомобили', 'IT')")
    )
    activities_map = {row[1]: row[0] for row in result}
    
    op.bulk_insert(activities_table, [
        {'name': 'Мясная продукция', 'parent_id': activities_map['Еда']},
        {'name': 'Молочная продукция', 'parent_id': activities_map['Еда']},
        {'name': 'Хлебобулочные изделия', 'parent_id': activities_map['Еда']},
    ])
    
    op.bulk_insert(activities_table, [
        {'name': 'Грузовые', 'parent_id': activities_map['Автомобили']},
        {'name': 'Легковые', 'parent_id': activities_map['Автомобили']},
    ])
    
    result = connection.execute(
        sa.text("SELECT id FROM activities WHERE name = 'Легковые'")
    )
    cars_id = result.fetchone()[0]
    
    op.bulk_insert(activities_table, [
        {'name': 'Запчасти', 'parent_id': cars_id},
        {'name': 'Аксессуары', 'parent_id': cars_id},
    ])
    
    result = connection.execute(
        sa.text("SELECT id FROM activities WHERE name = 'IT'")
    )
    it_id = result.fetchone()[0]
    
    op.bulk_insert(activities_table, [
        {'name': 'Разработка ПО', 'parent_id': it_id},
        {'name': 'Хостинг', 'parent_id': it_id},
        {'name': 'Консалтинг', 'parent_id': it_id},
    ])
    
    result = connection.execute(
        sa.text("SELECT id, name FROM activities")
    )
    all_activities = {row[1]: row[0] for row in result}
    
    
    op.bulk_insert(buildings_table, [
        {
            'address': 'г. Москва, ул. Блюхера 32/1',
            'latitude': 55.7749,
            'longitude': 37.5884,
        },
        {
            'address': 'г. Москва, ул. Ленина 1, офис 3',
            'latitude': 55.7558,
            'longitude': 37.6173,
        },
        {
            'address': 'г. Санкт-Петербург, Невский пр. 100',
            'latitude': 59.9343,
            'longitude': 30.3351,
        },
    ])
    
    result = connection.execute(
        sa.text("SELECT id FROM buildings ORDER BY id")
    )
    building_ids = [row[0] for row in result]
    
    op.bulk_insert(organizations_table, [
        {
            'name': 'ООО "Рога и Копыта"',
            'building_id': building_ids[0],
            'phone':'8999999999',
            'description': 'ООО "Рога и Копыта" - мясная и молочная продукция',
            'created_at': datetime.datetime.now()
        },
        {
            'name': 'ПАО "Молоко"',
            'building_id': building_ids[1],
            'phone':'8999999999',
            'description': 'ПАО "Молоко" - молочная продукция',
            'created_at': datetime.datetime.now()
        },
        {
            'name': 'ИП "Автозапчасти"',
            'building_id': building_ids[0],
            'phone':'8999999919',
            'description': 'ИП "Автозапчасти" - запчасти и аксессуары',
            'created_at': datetime.datetime.now()
        },
        {
            'name': 'ООО "IT Solutions"',
            'building_id': building_ids[2],
            'phone':'8999999991',
            'description': 'ООО "IT Solutions" - разработка ПО',
            'created_at': datetime.datetime.now()
        },
        {
            'name': 'АО "Мясной комбинат"',
            'building_id': building_ids[1],
            'phone':'8999999199',
            'description': 'АО "Мясной комбинат" - мясная продукция',
            'created_at': datetime.datetime.now()
        },
        {
            'name': 'ЗАО "Хлебзавод №1"',
            'building_id': building_ids[2],
            'phone':'8999919999',
            'description': 'ЗАО "Хлебзавод №1" - хлебобулочные изделия',
            'created_at': datetime.datetime.now()
        },
    ])
    
    result = connection.execute(
        sa.text("SELECT id, name FROM organizations")
    )
    orgs_map = {row[1]: row[0] for row in result}
    
    org_activities_data = []
    
    # ООО "Рога и Копыта" - мясная и молочная продукция
    org_activities_data.append({
        'organization_id': orgs_map['ООО "Рога и Копыта"'],
        'activity_id': all_activities['Мясная продукция']
    })
    org_activities_data.append({
        'organization_id': orgs_map['ООО "Рога и Копыта"'],
        'activity_id': all_activities['Молочная продукция']
    })
    
    # ПАО "Молоко" - молочная продукция
    org_activities_data.append({
        'organization_id': orgs_map['ПАО "Молоко"'],
        'activity_id': all_activities['Молочная продукция']
    })
    
    # ИП "Автозапчасти" - запчасти и аксессуары
    org_activities_data.append({
        'organization_id': orgs_map['ИП "Автозапчасти"'],
        'activity_id': all_activities['Запчасти']
    })
    org_activities_data.append({
        'organization_id': orgs_map['ИП "Автозапчасти"'],
        'activity_id': all_activities['Аксессуары']
    })
    
    # ООО "IT Solutions" - разработка ПО
    org_activities_data.append({
        'organization_id': orgs_map['ООО "IT Solutions"'],
        'activity_id': all_activities['Разработка ПО']
    })
    
    # АО "Мясной комбинат" - мясная продукция
    org_activities_data.append({
        'organization_id': orgs_map['АО "Мясной комбинат"'],
        'activity_id': all_activities['Мясная продукция']
    })
    
    # ЗАО "Хлебзавод №1" - хлебобулочные изделия
    org_activities_data.append({
        'organization_id': orgs_map['ЗАО "Хлебзавод №1"'],
        'activity_id': all_activities['Хлебобулочные изделия']
    })
    
    if org_activities_data:
        op.bulk_insert(organization_activities_table, org_activities_data)


def downgrade():
    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind())
    
    connection = op.get_bind()
    
    connection.execute(
        sa.text("DELETE FROM organization_activities")
    )
    
    connection.execute(
        sa.text("DELETE FROM organizations")
    )
    
    connection.execute(
        sa.text("DELETE FROM buildings")
    )

    connection.execute(
        sa.text("DELETE FROM activities")
    )
    
    try:
        connection.execute(
            sa.text("DELETE FROM sqlite_sequence WHERE name IN ('activities', 'buildings', 'organizations', 'organization_activities')")
        )
    except:
        pass  
    
