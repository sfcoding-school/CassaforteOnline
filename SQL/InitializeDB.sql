-- DROP DATABASE IF EXISTS saed;

-- DROP DATABASE IF EXISTS server1;

DROP DATABASE IF EXISTS server;

CREATE DATABASE IF NOT EXISTS server;

USE server;

--  CREAZIONE:
--  Tabella server
CREATE TABLE server(

    id INTEGER UNSIGNED PRIMARY KEY NOT NULL,
    address varchar(100)

);


--  CREAZIONE:
-- T abella Utente

CREATE TABLE user(

    mail VARCHAR(50) PRIMARY KEY NOT NULL,
    used_space INTEGER UNSIGNED NOT NULL DEFAULT 0 CHECK (used_space > 1024),
	pro BOOL NOT NULL DEFAULT false,
    password VARCHAR(600) DEFAULT ''
    -- DONE aggoingere pro booleano e password

);

--  CREAZIONE:
--  Tabella File

CREATE TABLE file(

    id integer UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    codest VARCHAR(100) NOT NULL,
    dim INTEGER UNSIGNED NOT NULL,
    nome VARCHAR(100) NOT NULL,
    owner VARCHAR(50),
    lavorazione BOOL DEFAULT false,    
    FOREIGN KEY (owner) REFERENCES user(mail) ON DELETE CASCADE

);

INSERT INTO server VALUES (1,'http://127.0.0.1:7791/?wsdl');
INSERT INTO server VALUES (2,'http://127.0.0.1:7792/?wsdl');
INSERT INTO server VALUES (3,'http://127.0.0.1:7793/?wsdl');    

--  CREAZIONE:
--  Tabella Slice

/*CREATE TABLE slice(

    id INTEGER UNSIGNED,
    FOREIGN KEY slice(id) REFERENCES file(id) ON DELETE CASCADE,
    slice_n INTEGER UNSIGNED NOT NULL,
    server INTEGER UNSIGNED NOT NULL, -- was address chiave esterna su tabella server da creare id(del server) indirizzo (di tt i server)
    FOREIGN KEY slice(server) REFERENCES server(id) ON DELETE CASCADE,
    uid VARCHAR(100),
    PRIMARY KEY(id, slice_n)
);

*/
-- Triggers:

-- After Insert


CREATE TRIGGER Space_Subtract_Before_Delete

    BEFORE DELETE ON file FOR EACH ROW
    UPDATE user u SET u.used_space = u.used_space - OLD.dim
    WHERE u.mail = OLD.owner;

-- Before Delete

CREATE TRIGGER Space_Sum_After_File_Update

    AFTER INSERT ON file FOR EACH ROW
    UPDATE user u SET u.used_space = u.used_space + NEW.dim
    WHERE u.mail = NEW.owner;

-- Before Insert (Verifica Spazio Rimanente)
-- NON FUNZIONA UN CAZZO!

 -- CREATE TRIGGER Verifica
 --   BEFORE INSERT ON file FOR EACH ROW
 --   BEGIN
 --       IF (((SELECT used_space FROM user WHERE user(mail) = NEW.owner) + NEW.dim ) > 999 )
 --            RAISERROR ('Error Text', 11, 1); -- this trick will throw an error
 --       END IF;
 --   END



-- POPOLAMENTO E TESTS:
/*

LOAD DATA LOCAL INFILE '/home/alexander/Documents/Database/server.txt' INTO TABLE server
FIELDS TERMINATED BY ' '
LINES TERMINATED BY '\n';


-- Riempie la tabella utente gli spazi sono a zero di default

LOAD DATA LOCAL INFILE '/home/alexander/Documents/Database/user.txt' INTO TABLE user
FIELDS TERMINATED BY ' '
LINES TERMINATED BY '\n';

show warnings;

-- Stampa tabella con tutti 0
SELECT * FROM user;

-- Riempie tabella file ed il trigger aggiorna lo spazio consumato sulla tabella user

LOAD DATA LOCAL INFILE '/home/alexander/Documents/Database/file.txt' INTO TABLE file
FIELDS TERMINATED BY ' '
LINES TERMINATED BY '\n';

SELECT * FROM file;

-- Riempie la tabella slice con i pezzi ed i relativi server

LOAD DATA LOCAL INFILE '/home/alexander/Documents/Database/slice.txt' INTO TABLE slice
FIELDS TERMINATED BY ' '
LINES TERMINATED BY '\n';

-- Stampa il tutto

SELECT * FROM user;
SELECT * FROM file;
SELECT * FROM slice;

-- DELETE FROM user WHERE mail = 'kingokon@hok.ot';

--

INSERT INTO file VALUES (3,'COD003',766, 'ahah.txt','kingokon@hok.ot');

SELECT * FROM user;
SELECT * FROM file;
SELECT * FROM slice;

-- Rimuove un file e verifica se elimina le slices e verifica trigger che diminuisce lo spazio consumato

DELETE FROM file WHERE owner = 'kingokon@hok.ot' AND id = 1;

select * from user;

-- update slice set address = '1000dawa' where (id = 2);
*/

