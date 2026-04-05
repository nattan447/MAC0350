CREATE TABLE aluno (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    curso TEXT NOT NULL
);

CREATE TABLE disciplina (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE matricula (
    aluno_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    PRIMARY KEY (aluno_id, disciplina_id),
    FOREIGN KEY (aluno_id) REFERENCES aluno (id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplina (id)
);

CREATE TABLE tarefa (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    disciplina_id INTEGER,
    FOREIGN KEY (disciplina_id) REFERENCES disciplina (id)
);

CREATE TABLE aluno_tarefa (
    aluno_id INTEGER NOT NULL,
    tarefa_id INTEGER NOT NULL,
    PRIMARY KEY (aluno_id, tarefa_id),
    FOREIGN KEY (aluno_id) REFERENCES aluno (id),
    FOREIGN KEY (tarefa_id) REFERENCES tarefa (id)
);