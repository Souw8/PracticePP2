DROP PROCEDURE IF EXISTS add_phone(VARCHAR,VARCHAR,VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR,VARCHAR);
DROP FUNCTION IF EXISTS search_contacts(TEXT);


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_contact_id INTEGER;
BEGIN 
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE names=p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'CONTACT NOT FOUND';
        RETURN;
    END IF;
    
    INSERT INTO phones(contact_id,phone,types)
    VALUES (v_contact_id,p_phone,p_type)
    ON CONFLICT(phone) DO NOTHING;
END;
$$;



CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups(names)
    VALUES (p_group_name)
    ON CONFLICT (names) DO NOTHING;

    SELECT ID INTO v_group_id
    FROM groups
    WHERE name=p_group_name;

    UPDATE contacts
    SET group_id=v_group_id
    WHERE names=p_contact_name;

    IF NOT FOUND THEN
        RAISE NOTICE 'CONTACT NOT FOUND';
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.names,
        c.email,
        c.birthday,
        g.names,
        p.phone,
        p.types
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE 
        c.names ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
        OR g.names ILIKE '%' || p_query || '%';
END;
$$;

