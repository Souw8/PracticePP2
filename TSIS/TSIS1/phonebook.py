import psycopg2
import csv
import json
from connect import get_connection



def add_contact(name, email, birthday, group_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups(names)
        VALUES (%s)
        ON CONFLICT (names) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE names = %s", (group_name,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(names, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (names) DO NOTHING
    """, (name, email, birthday, group_id))

    conn.commit()
    cur.close()
    conn.close()
def add_phone(name, phone, phone_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
def search(query):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()
def filter_by_group(group_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.names, c.email, c.birthday, g.names
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.names = %s
    """, (group_name,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()
def show_sorted(sort_by):
    allowed = {
        "name": "c.names",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }

    if sort_by not in allowed:
        print("Invalid sort option")
        return

    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT c.names, c.email, c.birthday, g.names
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {allowed[sort_by]}
    """

    cur.execute(query)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def export_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id, c.names, c.email, c.birthday, g.names
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    contacts = []

    for contact_id, name, email, birthday, group_name in cur.fetchall():
        cur.execute("""
            SELECT phone, types
            FROM phones
            WHERE contact_id = %s
        """, (contact_id,))

        phones = [
            {"phone": phone, "type": phone_type}
            for phone, phone_type in cur.fetchall()
        ]

        contacts.append({
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()
def import_json(filename="contacts.json"):
    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for contact in contacts:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE names = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} already exists. skip/overwrite: ")

            if choice == "skip":
                continue

            if choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE names = %s", (name,))

        cur.execute("""
            INSERT INTO groups(names)
            VALUES (%s)
            ON CONFLICT (names) DO NOTHING
        """, (contact["group"],))

        cur.execute("SELECT id FROM groups WHERE names = %s", (contact["group"],))
        group_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            contact["name"],
            contact["email"],
            contact["birthday"],
            group_id
        ))

        contact_id = cur.fetchone()[0]

        for phone in contact["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (contact_id, phone["phone"], phone["type"]))

    conn.commit()
    cur.close()
    conn.close()

def import_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            phone_type = row["type"]

            cur.execute("""
                INSERT INTO groups(names)
                VALUES (%s)
                ON CONFLICT (names) DO NOTHING
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE names = %s", (group,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(names, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (names) DO NOTHING
                RETURNING id
            """, (name, email, birthday, group_id))

            result = cur.fetchone()

            if result:
                contact_id = result[0]
            else:
                cur.execute("SELECT id FROM contacts WHERE names = %s", (name,))
                contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, types)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()


def paginated_navigation(page_size=5):
    conn = get_connection()
    cur = conn.cursor()

    page = 0

    while True:
        offset = page * page_size

        cur.execute("""
            SELECT * FROM get_contacts_paginated(%s, %s)
        """, (page_size, offset))

        rows = cur.fetchall()

        print(f"\n--- Page {page + 1} ---")

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts on this page.")

        command = input("next / prev / quit: ").lower()

        if command == "next":
            page += 1

        elif command == "prev":
            if page > 0:
                page -= 1
            else:
                print("Already on first page.")

        elif command == "quit":
            break

        else:
            print("Invalid command.")

    cur.close()
    conn.close()







if __name__=="__main__":
    while True:    
        command=input("Hello choose your command(add_contact,add_phone,import_json,export_json,show_sorted,filter_by_group,search):")
        if command=="add_contact":
            add_contact()
        elif command=="add_phone":
            name, phone,phone_type=input().split()
            add_phone(name, phone,phone_type)     #name, phone, phone_type
        elif command=="import_json":
            import_json()
        elif command=="export_json":
            export_json()
        elif command=="show_sorted":
           sort_by={ "name","birthday","date"}
           choice=input(f"choose which of the {sort_by} will be sorted by:")
           if choice=="name":
               show_sorted(choice)
           elif choice=="birthday":
               show_sorted(choice)
           else:
               show_sorted("date")
        elif command=="filter_by_group":
            group_name=input()
            filter_by_group(group_name)
        elif command=="search":
            any_query=input()
            search(any_query)
        elif command=="paginated_navigation":
            paginated_navigation()
        else:
            print("Sorry but there is nothing with this command")