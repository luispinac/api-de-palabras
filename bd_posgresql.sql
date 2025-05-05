CREATE TABLE palabras (
    id SERIAL PRIMARY KEY,
    palabra TEXT NOT NULL,
    categoria TEXT NOT NULL
);

INSERT INTO palabras (palabra, categoria)
VALUES ('gato', 'animales'), ('auto', 'vehículos'), ('perro', 'animales');
