CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE (
    id INTEGER,
    names VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
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
        g.names
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;