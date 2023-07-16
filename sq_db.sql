CREATE TABLE IF NOT EXISTS news (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,('', '/')
psw text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS brands (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS business_units (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
url text NOT NULL
);

-- INSERT INTO brands (name, url) VALUES
-- ('JOHNSON & JOHNSON', '/johnson'),
-- ('MEDTRONIC', '/medtronic'),
-- ('PORTEX, SMITHS MEDICAL', '/portex'),
-- ('PHILIPS', '/philips'),
-- ('GE HEALTHCARE', '/generalelectric'),
-- ('LOHMANN & RAUSCHER', '/lohmann&rauscher'),
-- ('TERUMO', '/terumo'),
-- ('BOSTON SCIENTIFIC', '/bostonscientific'),
-- ('FISHER & PAYKEL', '/fisher&paykel'),
-- ('MERIT MEDICAL', '/meritmedical'),
-- ('AMBU', '/ambu'),
-- ('MINDRAY', '/mindray'),
-- ('ROCHE', '/roche'),
-- ('PFM MEDICAL', '/pfmmedical'),
-- ('FEATHER', '/feather'),
-- ('MASIMO', '/masimo'),
-- ('ASP', '/asp'),
-- ('STRYKER', '/stryker'),
-- ('AEROGEN', '/aerogen'),
-- ('GUERBET', '/guerbet'),
-- ('SPECTRANETICS', '/spectranetics'),
-- ('BIOCER', '/biocer'),
-- ('JNJ Codman Cerenovus', '/codman'),
-- ('GVS FILTER TECHNOLOGY', '/gvs'),
-- ('KARL STORZ', '/karlstorz'),
-- ('GEOTEK', '/geotek'),
-- ('GCE', '/gce'),
-- ('MERIL', '/meril')


-- INSERT INTO business_units (name, url) VALUES
-- ('АНЕСТЕЗИОЛОГИЯ И РЕАНИМАЦИЯ', '/icu'),
-- ('ХИРУРГИЯ', '/surgery'),
-- ('КАРДИОЛОГИЯ И РЕНТГЕНХИРУРГИЯ', '/cardiovascular')