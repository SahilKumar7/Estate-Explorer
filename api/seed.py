"""
Seed script for Estate Explorer.

Drops all tables, recreates them, and inserts realistic dummy data:
- 3 users
- 12 property listings with details
- 2 chats with messages
- 2 saved posts

Run:  python seed.py   (from the api/ directory, with venv activated)
All users have password: password123
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from sqlalchemy import text

from app.database import engine, async_session
from app.models import (
    Base,
    User,
    Post,
    PostDetail,
    SavedPost,
    Chat,
    Message,
    chat_participants,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HASHED_PW = pwd_context.hash("password123")

NOW = datetime.now(timezone.utc)

UNSPLASH = "https://images.unsplash.com"

USER_DATA = [
    {
        "id": uuid.uuid4(),
        "username": "johndoe",
        "email": "john@example.com",
        "avatar": f"{UNSPLASH}/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop",
    },
    {
        "id": uuid.uuid4(),
        "username": "janerealty",
        "email": "jane@example.com",
        "avatar": f"{UNSPLASH}/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop",
    },
    {
        "id": uuid.uuid4(),
        "username": "mikeproperty",
        "email": "mike@example.com",
        "avatar": f"{UNSPLASH}/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop",
    },
]

POSTS_RAW = [
    {
        "title": "Luxury Manhattan Penthouse",
        "price": 2500000,
        "address": "432 Park Avenue, Apt 82A",
        "city": "New York",
        "bedroom": 4,
        "bathroom": 3,
        "latitude": "40.7614",
        "longitude": "-73.9718",
        "type": "buy",
        "property": "apartment",
        "images": [
            f"{UNSPLASH}/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
        ],
        "user_idx": 0,
        "detail": {
            "desc": "<p>Stunning penthouse with panoramic views of Central Park and the Manhattan skyline. Floor-to-ceiling windows flood every room with natural light. Features a chef's kitchen with Miele appliances, marble master bath, and a private terrace. Full-service building with 24/7 concierge, fitness center, and resident lounge.</p>",
            "utilities": "Owner",
            "pet": "Allowed",
            "income": "Proof required",
            "size": 3200,
            "school": 500,
            "bus": 100,
            "restaurant": 50,
        },
    },
    {
        "title": "Cozy Brooklyn Brownstone",
        "price": 4500,
        "address": "156 Dean Street",
        "city": "New York",
        "bedroom": 3,
        "bathroom": 2,
        "latitude": "40.6826",
        "longitude": "-73.9780",
        "type": "rent",
        "property": "house",
        "images": [
            f"{UNSPLASH}/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600573472592-401b489a3cdc?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600566753190-17f0baa2a6c3?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600047509807-ba8f99d2cdde?w=800&h=600&fit=crop",
        ],
        "user_idx": 1,
        "detail": {
            "desc": "<p>Charming three-story brownstone in the heart of Boerum Hill. Original hardwood floors, exposed brick, and a stunning garden-level kitchen that opens to a private backyard. Washer/dryer in unit. Walking distance to Atlantic Terminal and dozens of restaurants.</p>",
            "utilities": "Tenant",
            "pet": "Allowed",
            "income": "3x rent",
            "size": 1800,
            "school": 300,
            "bus": 200,
            "restaurant": 100,
        },
    },
    {
        "title": "Modern Chelsea Studio",
        "price": 3200,
        "address": "520 West 23rd Street",
        "city": "New York",
        "bedroom": 1,
        "bathroom": 1,
        "latitude": "40.7473",
        "longitude": "-74.0040",
        "type": "rent",
        "property": "apartment",
        "images": [
            f"{UNSPLASH}/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600566753086-00f18fb6b3ea?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210492486-724fe5c67fb0?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop",
        ],
        "user_idx": 2,
        "detail": {
            "desc": "<p>Sleek studio in a modern Chelsea building. Floor-to-ceiling windows, in-unit washer/dryer, and a gourmet kitchen with stainless steel appliances. Building amenities include a rooftop deck, gym, and package room. Steps from the High Line and Chelsea Market.</p>",
            "utilities": "Included",
            "pet": "Cats only",
            "income": "40x rent",
            "size": 550,
            "school": 800,
            "bus": 50,
            "restaurant": 30,
        },
    },
    {
        "title": "Victorian House in Noe Valley",
        "price": 1850000,
        "address": "1234 Sanchez Street",
        "city": "San Francisco",
        "bedroom": 3,
        "bathroom": 2,
        "latitude": "37.7502",
        "longitude": "-122.4310",
        "type": "buy",
        "property": "house",
        "images": [
            f"{UNSPLASH}/photo-1568605114967-8130f3a36994?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585154526-990dced4db0d?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1583608205776-bfd35f0d9f83?w=800&h=600&fit=crop",
        ],
        "user_idx": 0,
        "detail": {
            "desc": "<p>Beautifully restored Victorian home in one of SF's most sought-after neighborhoods. Original crown moldings, bay windows, and a modern open-plan kitchen. Sunny south-facing backyard perfect for entertaining. Two-car garage — a rarity in the city.</p>",
            "utilities": "Owner",
            "pet": "Allowed",
            "income": "Not required",
            "size": 2100,
            "school": 200,
            "bus": 150,
            "restaurant": 250,
        },
    },
    {
        "title": "SOMA Loft with City Views",
        "price": 5200,
        "address": "888 Brannan Street, Unit 401",
        "city": "San Francisco",
        "bedroom": 2,
        "bathroom": 2,
        "latitude": "37.7719",
        "longitude": "-122.4030",
        "type": "rent",
        "property": "condo",
        "images": [
            f"{UNSPLASH}/photo-1600607687644-c7171b42498f?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585154363-67eb9e2e2099?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600573472591-ee6981cf81d6?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600566753376-12c8ab7a5a2e?w=800&h=600&fit=crop",
        ],
        "user_idx": 1,
        "detail": {
            "desc": "<p>Industrial-chic loft in the heart of SOMA. 16-foot ceilings, polished concrete floors, and walls of windows showcasing the city skyline. Custom built-in shelving, chef's kitchen, and oversized master suite. Building includes a fitness center and rooftop terrace.</p>",
            "utilities": "Shared",
            "pet": "Small dogs only",
            "income": "3x rent",
            "size": 1400,
            "school": 600,
            "bus": 100,
            "restaurant": 80,
        },
    },
    {
        "title": "Elegant Kensington Flat",
        "price": 1200000,
        "address": "14 Kensington Court, W8",
        "city": "London",
        "bedroom": 2,
        "bathroom": 2,
        "latitude": "51.5010",
        "longitude": "-0.1870",
        "type": "buy",
        "property": "apartment",
        "images": [
            f"{UNSPLASH}/photo-1600047509782-20d39509f26d?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210491892-03d54c0aaf87?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585153490-76fb20a32601?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600573472556-e636c2acda9e?w=800&h=600&fit=crop",
        ],
        "user_idx": 2,
        "detail": {
            "desc": "<p>Elegant two-bedroom flat in a period conversion just moments from Kensington High Street. High ceilings, sash windows, and a beautifully landscaped communal garden. Porterage and lift access. Council Tax Band F.</p>",
            "utilities": "Owner",
            "pet": "Not allowed",
            "income": "Proof required",
            "size": 950,
            "school": 400,
            "bus": 80,
            "restaurant": 120,
        },
    },
    {
        "title": "Shoreditch Warehouse Conversion",
        "price": 3800,
        "address": "22 Curtain Road, EC2A",
        "city": "London",
        "bedroom": 1,
        "bathroom": 1,
        "latitude": "51.5235",
        "longitude": "-0.0812",
        "type": "rent",
        "property": "apartment",
        "images": [
            f"{UNSPLASH}/photo-1600566752355-35792bedcfea?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210491369-e753da563ce8?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600047508788-786f3865b4b9?w=800&h=600&fit=crop",
        ],
        "user_idx": 0,
        "detail": {
            "desc": "<p>Striking warehouse conversion in trendy Shoreditch. Exposed brickwork, steel beams, and concrete floors create an authentic industrial feel. Open-plan living with a bespoke kitchen island. Moments from Old Street station and Boxpark.</p>",
            "utilities": "Included",
            "pet": "Cats only",
            "income": "References required",
            "size": 680,
            "school": 700,
            "bus": 50,
            "restaurant": 20,
        },
    },
    {
        "title": "Pacific Heights Condo",
        "price": 975000,
        "address": "2400 Steiner Street, Unit 3",
        "city": "San Francisco",
        "bedroom": 2,
        "bathroom": 1,
        "latitude": "37.7919",
        "longitude": "-122.4367",
        "type": "buy",
        "property": "condo",
        "images": [
            f"{UNSPLASH}/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585154526-990dced4db0d?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210492486-724fe5c67fb0?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
        ],
        "user_idx": 1,
        "detail": {
            "desc": "<p>Bright condo with sweeping views of the Bay and Golden Gate Bridge from Pacific Heights. Freshly renovated with quartz countertops, hardwood floors, and designer fixtures. Shared rooftop deck. Walk Score of 96.</p>",
            "utilities": "HOA covered",
            "pet": "Allowed",
            "income": "Not required",
            "size": 1050,
            "school": 350,
            "bus": 120,
            "restaurant": 200,
        },
    },
    {
        "title": "Greenwich Village Townhouse",
        "price": 4200000,
        "address": "78 Washington Place",
        "city": "New York",
        "bedroom": 5,
        "bathroom": 4,
        "latitude": "40.7321",
        "longitude": "-73.9988",
        "type": "buy",
        "property": "house",
        "images": [
            f"{UNSPLASH}/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600573472592-401b489a3cdc?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1583608205776-bfd35f0d9f83?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1568605114967-8130f3a36994?w=800&h=600&fit=crop",
        ],
        "user_idx": 2,
        "detail": {
            "desc": "<p>Rare five-bedroom townhouse in the heart of Greenwich Village. Spanning four floors with a garden level, parlor floor with 12-foot ceilings, and a private roof terrace. Wood-burning fireplace, chef's kitchen, and a landscaped rear garden. Minutes from Washington Square Park.</p>",
            "utilities": "Owner",
            "pet": "Allowed",
            "income": "Not required",
            "size": 4500,
            "school": 250,
            "bus": 80,
            "restaurant": 30,
        },
    },
    {
        "title": "Canary Wharf Modern Flat",
        "price": 2800,
        "address": "1 Pan Peninsula Square, E14",
        "city": "London",
        "bedroom": 2,
        "bathroom": 2,
        "latitude": "51.5000",
        "longitude": "-0.0097",
        "type": "rent",
        "property": "condo",
        "images": [
            f"{UNSPLASH}/photo-1600607687644-c7171b42498f?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600566753190-17f0baa2a6c3?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210491892-03d54c0aaf87?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600585153490-76fb20a32601?w=800&h=600&fit=crop",
        ],
        "user_idx": 0,
        "detail": {
            "desc": "<p>Modern two-bed flat in a premium Canary Wharf tower. Floor-to-ceiling glazing with river views, open-plan living, and a sleek handleless kitchen. Building amenities include a 25m pool, spa, cinema room, and 24-hour concierge. Direct access to Canary Wharf station.</p>",
            "utilities": "Shared",
            "pet": "Not allowed",
            "income": "Employer reference",
            "size": 820,
            "school": 500,
            "bus": 60,
            "restaurant": 100,
        },
    },
    {
        "title": "Mission District Development Land",
        "price": 3200000,
        "address": "Lot 12, Valencia Street",
        "city": "San Francisco",
        "bedroom": 0,
        "bathroom": 0,
        "latitude": "37.7599",
        "longitude": "-122.4213",
        "type": "buy",
        "property": "land",
        "images": [
            f"{UNSPLASH}/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1625244724120-1fd1d34d00f6?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1568605114967-8130f3a36994?w=800&h=600&fit=crop",
        ],
        "user_idx": 1,
        "detail": {
            "desc": "<p>Prime development opportunity in the booming Mission District. Flat 5,200 sq ft lot zoned for mixed-use residential. Approved plans available for a 6-unit building. Excellent transit access with BART one block away. Surrounded by top-rated restaurants and vibrant nightlife.</p>",
            "utilities": "N/A",
            "pet": "N/A",
            "income": "N/A",
            "size": 5200,
            "school": 400,
            "bus": 50,
            "restaurant": 30,
        },
    },
    {
        "title": "Notting Hill Garden Flat",
        "price": 850000,
        "address": "32 Ladbroke Grove, W11",
        "city": "London",
        "bedroom": 1,
        "bathroom": 1,
        "latitude": "51.5133",
        "longitude": "-0.2050",
        "type": "buy",
        "property": "apartment",
        "images": [
            f"{UNSPLASH}/photo-1600047509807-ba8f99d2cdde?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600566752355-35792bedcfea?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1600210491369-e753da563ce8?w=800&h=600&fit=crop",
            f"{UNSPLASH}/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
        ],
        "user_idx": 2,
        "detail": {
            "desc": "<p>Delightful ground-floor garden flat on one of Notting Hill's most desirable streets. Private south-facing garden, period features throughout, and a modern fitted kitchen. Steps from Portobello Road Market and Ladbroke Grove station. Share of freehold.</p>",
            "utilities": "Owner",
            "pet": "Allowed",
            "income": "Not required",
            "size": 620,
            "school": 300,
            "bus": 100,
            "restaurant": 80,
        },
    },
]


async def seed():
    print("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print("Creating all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            users = []
            for u in USER_DATA:
                user = User(
                    id=u["id"],
                    username=u["username"],
                    email=u["email"],
                    password=HASHED_PW,
                    avatar=u["avatar"],
                    created_at=NOW - timedelta(days=30),
                )
                session.add(user)
                users.append(user)

            print(f"  Inserted {len(users)} users")

            posts = []
            for i, p in enumerate(POSTS_RAW):
                post_id = uuid.uuid4()
                post = Post(
                    id=post_id,
                    title=p["title"],
                    price=p["price"],
                    images=p["images"],
                    address=p["address"],
                    city=p["city"],
                    bedroom=p["bedroom"],
                    bathroom=p["bathroom"],
                    latitude=p["latitude"],
                    longitude=p["longitude"],
                    type=p["type"],
                    property=p["property"],
                    user_id=USER_DATA[p["user_idx"]]["id"],
                    created_at=NOW - timedelta(days=20 - i),
                )
                session.add(post)

                detail = PostDetail(
                    id=uuid.uuid4(),
                    post_id=post_id,
                    **p["detail"],
                )
                session.add(detail)
                posts.append(post)

            print(f"  Inserted {len(posts)} posts with details")

            for idx, (user_idx, post_idx) in enumerate([(0, 5), (1, 0)]):
                sp = SavedPost(
                    id=uuid.uuid4(),
                    user_id=USER_DATA[user_idx]["id"],
                    post_id=posts[post_idx].id,
                    created_at=NOW - timedelta(days=5 - idx),
                )
                session.add(sp)

            print("  Inserted 2 saved posts")

            chat1_id = uuid.uuid4()
            chat2_id = uuid.uuid4()

            chat1 = Chat(
                id=chat1_id,
                created_at=NOW - timedelta(days=3),
                seen_by=[USER_DATA[0]["id"], USER_DATA[1]["id"]],
                last_message="Sounds great, when can I schedule a viewing?",
            )
            chat2 = Chat(
                id=chat2_id,
                created_at=NOW - timedelta(days=1),
                seen_by=[USER_DATA[1]["id"]],
                last_message="Is the price negotiable?",
            )
            session.add(chat1)
            session.add(chat2)

            await session.flush()

            await session.execute(
                chat_participants.insert(),
                [
                    {"chat_id": chat1_id, "user_id": USER_DATA[0]["id"]},
                    {"chat_id": chat1_id, "user_id": USER_DATA[1]["id"]},
                    {"chat_id": chat2_id, "user_id": USER_DATA[1]["id"]},
                    {"chat_id": chat2_id, "user_id": USER_DATA[2]["id"]},
                ],
            )

            chat1_messages = [
                Message(
                    id=uuid.uuid4(),
                    text="Hi! I saw your listing for the Kensington flat. Is it still available?",
                    user_id=str(USER_DATA[0]["id"]),
                    chat_id=chat1_id,
                    created_at=NOW - timedelta(days=3, hours=2),
                ),
                Message(
                    id=uuid.uuid4(),
                    text="Yes, it's still on the market! Would you like to arrange a viewing?",
                    user_id=str(USER_DATA[1]["id"]),
                    chat_id=chat1_id,
                    created_at=NOW - timedelta(days=3, hours=1),
                ),
                Message(
                    id=uuid.uuid4(),
                    text="Sounds great, when can I schedule a viewing?",
                    user_id=str(USER_DATA[0]["id"]),
                    chat_id=chat1_id,
                    created_at=NOW - timedelta(days=3),
                ),
            ]

            chat2_messages = [
                Message(
                    id=uuid.uuid4(),
                    text="Hello, I'm interested in the Pacific Heights condo. Beautiful place!",
                    user_id=str(USER_DATA[2]["id"]),
                    chat_id=chat2_id,
                    created_at=NOW - timedelta(days=1, hours=4),
                ),
                Message(
                    id=uuid.uuid4(),
                    text="Thank you! It's one of our best listings. Let me know if you have any questions.",
                    user_id=str(USER_DATA[1]["id"]),
                    chat_id=chat2_id,
                    created_at=NOW - timedelta(days=1, hours=3),
                ),
                Message(
                    id=uuid.uuid4(),
                    text="Is the price negotiable?",
                    user_id=str(USER_DATA[2]["id"]),
                    chat_id=chat2_id,
                    created_at=NOW - timedelta(days=1),
                ),
            ]

            for msg in chat1_messages + chat2_messages:
                session.add(msg)

            print("  Inserted 2 chats with 6 messages")

    await engine.dispose()
    print("\nDone! Database seeded successfully.")
    print("Login credentials (all users): password123")
    print("Usernames: johndoe, janerealty, mikeproperty")


if __name__ == "__main__":
    asyncio.run(seed())
