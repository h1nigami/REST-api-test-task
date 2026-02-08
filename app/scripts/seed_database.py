"""
Скрипт для заполнения базы данных тестовыми данными
"""
import asyncio
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, text

from ..models import organization_activities, Activity, Organization, Building

DATABASE_URL = os.getenv("DSN")

async def seed_database():
    print("Начинаем заполнение базы данных тестовыми данными...")
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Проверяем существование таблицы sqlite_sequence
            print("🔍 Проверяем наличие таблицы sqlite_sequence...")
            result = await session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'"))
            sqlite_sequence_exists = result.fetchone() is not None
            
            if sqlite_sequence_exists:
                print("✅ Таблица sqlite_sequence существует")
                # Очищаем автоинкрементные счетчики для SQLite
                await session.execute(text("DELETE FROM sqlite_sequence WHERE name='activities'"))
                await session.execute(text("DELETE FROM sqlite_sequence WHERE name='buildings'"))
                await session.execute(text("DELETE FROM sqlite_sequence WHERE name='organizations'"))
                await session.execute(text("DELETE FROM sqlite_sequence WHERE name='organization_activities'"))
            else:
                print("ℹ️  Таблица sqlite_sequence не существует (нормально для новой базы)")
            
            # Очищаем таблицы (обратный порядок из-за внешних ключей)
            print("🧹 Очищаем таблицы...")
            
            await session.execute(text("DELETE FROM organization_activities"))
            await session.execute(text("DELETE FROM organizations"))
            await session.execute(text("DELETE FROM buildings"))
            await session.execute(text("DELETE FROM activities"))
            
            
        except Exception as e:
            print(f"⚠️  Предупреждение при очистке: {e}")


        # Создаем виды деятельности (древовидная структура)
        print("📊 Создаем виды деятельности...")
        
        # Корневые категории
        food = Activity(name="Еда", description="Продукты питания")
        vehicles = Activity(name="Автомобили", description="Автомобильная тематика")
        it = Activity(name="IT услуги", description="Информационные технологии")
        
        session.add_all([food, vehicles, it])
        await session.flush()
        
        # Подкатегории для Еды
        meat = Activity(name="Мясная продукция", description="Мясо и мясные изделия", parent_id=food.id)
        dairy = Activity(name="Молочная продукция", description="Молоко и молочные изделия", parent_id=food.id)
        bakery = Activity(name="Хлебобулочные изделия", description="Хлеб, булки, пироги", parent_id=food.id)
        
        # Подкатегории для Автомобилей
        trucks = Activity(name="Грузовые", description="Грузовые автомобили", parent_id=vehicles.id)
        cars = Activity(name="Легковые", description="Легковые автомобили", parent_id=vehicles.id)
        
        # Подкатегории для Легковых автомобилей
        parts = Activity(name="Запчасти", description="Автозапчасти", parent_id=cars.id)
        accessories = Activity(name="Аксессуары", description="Автоаксессуары", parent_id=cars.id)
        service = Activity(name="Техобслуживание", description="Сервисное обслуживание", parent_id=cars.id)
        
        # Подкатегории для IT услуг
        software = Activity(name="Разработка ПО", description="Разработка программного обеспечения", parent_id=it.id)
        hosting = Activity(name="Хостинг", description="Веб-хостинг и серверы", parent_id=it.id)
        consulting = Activity(name="Консалтинг", description="IT консалтинг", parent_id=it.id)
        
        session.add_all([meat, dairy, bakery, trucks, cars, parts, accessories, service, software, hosting, consulting])
        await session.flush()
        
        # Создаем здания
        print("🏢 Создаем здания...")
        
        buildings = [
            Building(
                address="ул. Ленина, 10",
                latitude=55.7558,
                longitude=37.6173,
            ),
            Building(
                address="пр. Мира, 25",
                latitude=55.7900,
                longitude=37.6750,
            ),
            Building(
                address="ул. Пушкина, 5",
                latitude=55.7650,
                longitude=37.6050,
            ),
            Building(
                address="ул. Гагарина, 15",
                latitude=55.7250,
                longitude=37.6250,
            ),
        ]
        
        session.add_all(buildings)
        await session.flush()
        
        # Создаем организации
        print("🏢 Создаем организации...")
        
        organizations = [
            Organization(
                name="Мясной двор",
                phone_number="+7-999-111-11-11",
                description="Продажа свежего мяса и колбасных изделий",
                building_id=buildings[0].id,
            ),
            Organization(
                name="Молочная ферма",
                phone_number="+7-999-222-22-22",
                description="Производство и продажа молочной продукции",
                building_id=buildings[0].id,
            ),
            Organization(
                name="Грузовики России",
                phone_number="+7-999-333-33-33",
                description="Продажа и аренда грузовых автомобилей",
                building_id=buildings[1].id,
            ),
            Organization(
                name="Автозапчасти 24/7",
                phone_number="+7-999-444-44-44",
                description="Запчасти для иномарок и отечественных авто",
                building_id=buildings[1].id,
            ),
            Organization(
                name="Автоаксессуары Премиум",
                phone_number="+7-999-555-55-55",
                description="Эксклюзивные аксессуары для автомобилей",
                building_id=buildings[1].id,
            ),
            Organization(
                name="IT Solutions Pro",
                phone_number="+7-999-666-66-66",
                description="Разработка корпоративного ПО и интеграция",
                building_id=buildings[2].id,
            ),
            Organization(
                name="Серверные Технологии",
                phone_number="+7-999-777-77-77",
                description="Обслуживание серверов и облачные решения",
                building_id=buildings[2].id,
            ),
            Organization(
                name="Продуктовый Мир",
                phone_number="+7-999-888-88-88",
                description="Сеть продуктовых магазинов",
                building_id=buildings[3].id,
            ),
            Organization(
                name="Хлебная Лавка",
                phone_number="+7-999-999-99-99",
                building_id=buildings[3].id,
            ),
        ]
        
        session.add_all(organizations)
        await session.flush()
        
        print("🔗 Связываем организации с видами деятельности...")
        
        org_activities_data = [
            # Мясной двор
            {"organization_id": organizations[0].id, "activity_id": meat.id, "is_primary": True},
            {"organization_id": organizations[0].id, "activity_id": food.id, "is_primary": False},
            
            # Молочная ферма
            {"organization_id": organizations[1].id, "activity_id": dairy.id, "is_primary": True},
            {"organization_id": organizations[1].id, "activity_id": food.id, "is_primary": False},
            
            # Грузовики России
            {"organization_id": organizations[2].id, "activity_id": trucks.id, "is_primary": True},
            {"organization_id": organizations[2].id, "activity_id": vehicles.id, "is_primary": False},
            
            # Автозапчасти 24/7
            {"organization_id": organizations[3].id, "activity_id": parts.id, "is_primary": True},
            {"organization_id": organizations[3].id, "activity_id": cars.id, "is_primary": False},
            {"organization_id": organizations[3].id, "activity_id": vehicles.id, "is_primary": False},
            
            # Автоаксессуары Премиум
            {"organization_id": organizations[4].id, "activity_id": accessories.id, "is_primary": True},
            {"organization_id": organizations[4].id, "activity_id": cars.id, "is_primary": False},
            
            # IT Solutions Pro
            {"organization_id": organizations[5].id, "activity_id": software.id, "is_primary": True},
            {"organization_id": organizations[5].id, "activity_id": it.id, "is_primary": False},
            
            # Серверные Технологии
            {"organization_id": organizations[6].id, "activity_id": hosting.id, "is_primary": True},
            {"organization_id": organizations[6].id, "activity_id": it.id, "is_primary": False},
            
            # Продуктовый Мир
            {"organization_id": organizations[7].id, "activity_id": food.id, "is_primary": True},
            {"organization_id": organizations[7].id, "activity_id": meat.id, "is_primary": False},
            {"organization_id": organizations[7].id, "activity_id": dairy.id, "is_primary": False},
            
            # Хлебная Лавка
            {"organization_id": organizations[8].id, "activity_id": bakery.id, "is_primary": True},
            {"organization_id": organizations[8].id, "activity_id": food.id, "is_primary": False},
        ]
        
        stmt = insert(organization_activities)
        await session.execute(stmt, org_activities_data)
        
        await session.commit()
        print("✅ База данных успешно заполнена тестовыми данными!")
        
        # Выводим статистику
        print("\n📊 Статистика:")
        print(f"   Видов деятельности: {len([food, vehicles, it, meat, dairy, bakery, trucks, cars, parts, accessories, service, software, hosting, consulting])}")
        print(f"   Зданий: {len(buildings)}")
        print(f"   Организаций: {len(organizations)}")
        print(f"   Связей организация-деятельность: {len(org_activities_data)}")

if __name__ == "__main__":
    asyncio.run(seed_database())