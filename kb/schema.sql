CREATE TABLE IF NOT EXISTS verses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  translation TEXT NOT NULL,
  book TEXT NOT NULL,
  chapter INTEGER NOT NULL,
  verse INTEGER NOT NULL,
  reference TEXT NOT NULL,
  text TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_verse_unique
  ON verses (translation, book, chapter, verse);

CREATE VIRTUAL TABLE IF NOT EXISTS verses_fts USING fts5(
  reference,
  text,
  content='verses',
  content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS verses_ai AFTER INSERT ON verses BEGIN
  INSERT INTO verses_fts(rowid, reference, text)
  VALUES (new.id, new.reference, new.text);
END;

CREATE TRIGGER IF NOT EXISTS verses_ad AFTER DELETE ON verses BEGIN
  INSERT INTO verses_fts(verses_fts, rowid, reference, text)
  VALUES('delete', old.id, old.reference, old.text);
END;

CREATE TRIGGER IF NOT EXISTS verses_au AFTER UPDATE ON verses BEGIN
  INSERT INTO verses_fts(verses_fts, rowid, reference, text)
  VALUES('delete', old.id, old.reference, old.text);
  INSERT INTO verses_fts(rowid, reference, text)
  VALUES (new.id, new.reference, new.text);
END;
