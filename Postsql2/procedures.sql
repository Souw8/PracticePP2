CREATE OR REPLACE PROCEDURE upsert(p_names VARCHAR,p_phones VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    
    IF EXISTS(
        SELECT 1
        FROM Phone111
        WHERE names=p_names
    )
    THEN 
        UPDATE Phone111
        SET phones=p_phones
        WHERE names=p_names;
    ELSE
        INSERT INTO Phone111(names,phones) 
        VALUES(p_names,p_phones);

    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN

    FOR i IN 1..array_length(p_names, 1)
    LOOP

        IF p_phones[i] ~ '^\+?[0-9]{10,15}$'
        THEN

            CALL upsert(
                p_names[i],
                p_phones[i]
            );

        ELSE

            RAISE NOTICE 'incorrect phone: %',
            p_phones[i];

        END IF;

    END LOOP;

END;
$$;



CREATE OR REPLACE PROCEDURE delete_user(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM Phone111
    WHERE names = p_value
       OR phones = p_value;

END;
$$;