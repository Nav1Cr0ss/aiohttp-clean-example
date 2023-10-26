CREATE TYPE roleenum AS ENUM ('admin', 'staff');


CREATE TYPE drawingstatusenum AS ENUM ('uploaded','pending', 'processed', 'deleted');

CREATE TABLE account_users
(
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(150) NOT NULL,
    password_hash VARCHAR(150) NOT NULL,
    role          roleenum    NOT NULL default 'staff'::roleenum
);


CREATE TABLE drawing_files
(
    id       SERIAL PRIMARY KEY,
    user_id  INT REFERENCES account_users (id) NOT NULL,
    filename VARCHAR(255)                      NOT NULL,
    status   drawingstatusenum               NOT NULL
);

CREATE TABLE drawing_history
(
    id        SERIAL PRIMARY KEY,
    file_id   INT REFERENCES drawing_files (id)    NOT NULL,
    user_id   INT REFERENCES account_users (id) NOT NULL,
    status    drawingstatusenum               NOT NULL,
    timestamp TIMESTAMPTZ                       NOT NULL
);


CREATE
    OR REPLACE FUNCTION file_files_update_history_f()
    RETURNS TRIGGER AS
$$
BEGIN
    IF
        TG_OP = 'INSERT' THEN
        INSERT INTO drawing_history (file_id, user_id, status, timestamp)
        VALUES (NEW.id, NEW.user_id, NEW.status, NOW());
        RETURN NEW;
    ELSIF
        TG_OP = 'UPDATE' THEN
        INSERT INTO drawing_history (file_id, user_id, status, timestamp)
        VALUES (OLD.id, OLD.user_id, NEW.status, NOW());
        RETURN NEW;
    ELSIF
        TG_OP = 'DELETE' THEN
        INSERT INTO drawing_history (file_id, user_id, status, timestamp)
        VALUES (OLD.id, OLD.user_id, 'deleted'::drawingstatusenum, NOW());
        RETURN OLD;
    END IF;
END;
$$
    LANGUAGE plpgsql;

CREATE or replace TRIGGER file_files_update_history_t
    AFTER INSERT OR
        UPDATE OR
        DELETE
    ON drawing_files
    FOR EACH ROW
EXECUTE FUNCTION file_files_update_history_f();