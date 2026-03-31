CREATE OR REPLACE FUNCTION search_phonebooks(pattern_text TEXT)
RETURNS TABLE(
    id INT,
    names VARCHAR,
    phones VARCHAR
)
AS $$
BEGIN
     
     RETURN QUERY
     SELECT p.id, p.names, p.phones
     FROM Phone111 p
     WHERE p.names ILIKE '%' || pattern_text || '%'
        OR p.phones ILIKE '%' || pattern_text || '%';

END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_phonebook_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    id INT,
    names VARCHAR,
    phones VARCHAR
)
AS $$
BEGIN

    RETURN QUERY
    SELECT p.id, p.names, p.phones
    FROM Phone111 p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;

END;
$$ LANGUAGE plpgsql;