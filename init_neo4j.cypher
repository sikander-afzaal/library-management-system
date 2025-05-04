CREATE (:Author {name: 'George Orwell'});
CREATE (:Author {name: 'Harper Lee'});
CREATE (:Author {name: 'Jane Austen'});
CREATE (:Author {name: 'Francesc Miralles and Hector Garcia'});

CREATE (:Publisher {name: 'Penguin Books'});
CREATE (:Publisher {name: 'J.B. Lippincott & Co.'});
CREATE (:Publisher {name: 'T. Egerton'});
CREATE (:Publisher {name: 'Secker and Warburg'});
CREATE (:Publisher {name: 'Penguin Life'});

CREATE (:Genre {name: 'Fiction'});
CREATE (:Genre {name: 'Non-Fiction'});
CREATE (:Genre {name: 'Romance'});
CREATE (:Genre {name: 'Satire'});
CREATE (:Genre {name: 'Self Help'});

CREATE (:Book {title: '1984'});
CREATE (:Book {title: 'To Kill a Mockingbird'});
CREATE (:Book {title: 'Pride and Prejudice'});
CREATE (:Book {title: 'Animal Farm'});
CREATE (:Book {title: 'Ikigai'});

CREATE (:Customer {name: 'Sikander2'});

MATCH (b:Book {title: '1984'}), (a:Author {name: 'George Orwell'})
CREATE (a)-[:WROTE]->(b);

MATCH (b:Book {title: 'To Kill a Mockingbird'}), (a:Author {name: 'Harper Lee'})
CREATE (a)-[:WROTE]->(b);

MATCH (b:Book {title: 'Pride and Prejudice'}), (a:Author {name: 'Jane Austen'})
CREATE (a)-[:WROTE]->(b);

MATCH (b:Book {title: 'Animal Farm'}), (a:Author {name: 'George Orwell'})
CREATE (a)-[:WROTE]->(b);

MATCH (b:Book {title: 'Ikigai'}), (a:Author {name: 'Francesc Miralles and Hector Garcia'})
CREATE (a)-[:WROTE]->(b);

MATCH (b:Book {title: '1984'}), (p:Publisher {name: 'Penguin Books'})
CREATE (b)-[:PUBLISHED_BY]->(p);

MATCH (b:Book {title: 'To Kill a Mockingbird'}), (p:Publisher {name: 'J.B. Lippincott & Co.'})
CREATE (b)-[:PUBLISHED_BY]->(p);

MATCH (b:Book {title: 'Pride and Prejudice'}), (p:Publisher {name: 'T. Egerton'})
CREATE (b)-[:PUBLISHED_BY]->(p);

MATCH (b:Book {title: 'Animal Farm'}), (p:Publisher {name: 'Secker and Warburg'})
CREATE (b)-[:PUBLISHED_BY]->(p);

MATCH (b:Book {title: 'Ikigai'}), (p:Publisher {name: 'Penguin Life'})
CREATE (b)-[:PUBLISHED_BY]->(p);

MATCH (b:Book {title: '1984'}), (g:Genre {name: 'Fiction'})
CREATE (b)-[:BELONGS_TO]->(g);

MATCH (b:Book {title: 'To Kill a Mockingbird'}), (g:Genre {name: 'Fiction'})
CREATE (b)-[:BELONGS_TO]->(g);

MATCH (b:Book {title: 'Pride and Prejudice'}), (g:Genre {name: 'Romance'})
CREATE (b)-[:BELONGS_TO]->(g);

MATCH (b:Book {title: 'Animal Farm'}), (g:Genre {name: 'Satire'})
CREATE (b)-[:BELONGS_TO]->(g);

MATCH (b:Book {title: 'Ikigai'}), (g:Genre {name: 'Self Help'})
CREATE (b)-[:BELONGS_TO]->(g);

MATCH (c:Customer {name: 'Sikander2'}), (b:Book {title: '1984'})
CREATE (c)-[:BORROWED {state: 'Borrowed', borrow_date: date('2025-04-25')}]->(b);