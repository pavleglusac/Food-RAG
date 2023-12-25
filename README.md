# Food-RAG
Food-RAG (ili kako se već zove) je projekat koji omogućava korisnicima da jednostavno istražuju sastojke različitih jela kroz postavljanje upita u prirodnom jeziku. U projektu je implementirana ontologija u formi RDF grafa koja čuva podatke o sastojcima i jelima. Korisnicima se prikazuje jednostavan interfejs i pruža im se mogućnost da postavljaju upite u četu, koji se kasnije prevode u SPARQL oblik i izvršavaju se nad kreiranom ontologijom. 

## Instalacija

## Pokretanje
// ovdje mozda, između ostalog, objasniti kojim redom se pokreću oni siclni fajlovi


## Ontologija
Inicijalnu verziju ontologije kreirali smo upotrebom **_Protégé_** alata. Ona je sadržala samo klase *Dish* i *Ingredient*. *ObjectProperty* relacija *hasIngredient* je definisana tako da je tranzitivna i da su joj domen klase *Dish* i *Ingredient*, a *range* Ingredient. Ova jednostavna ontologija nalazi se u fajlu *empty_ontology_protege.rdf.*
Zatim smo ubacili nekoliko poznatih jela i tako kreiran fajl sačuvali pod nazivom *dishes.rdf*. 

Sledeći korak bio je popunjavanje ontologije sastojcima već umetnutih jela. Za tu svrhu smo koristili Python biblioteku **_wikipedia_**. Ona nudi jednostavnu funkciju *summary(article, sentences)* za sumarizaciju. Prvi parametar je naziv članka na vikipediji. Drugi je broj rečenica koji želimo da koristimo za sumarizaciju. U našem slučaju, odabrali smo vrednost 3, jer se u člancima o hrani na vikipediji sastojci obično pojavljuju u 3 najbitnije rečenice. Kada smo doblili kratku reprezentaciju članka, bilo je potrebno ekstrahovati podatke iz te reprezentacije. To smo postigli upotrebom **UNI-NER** (*Universal Named Entity Recognition*) modela. To je manji jezički model (7 milijardi parametara) namenjen za prepoznavanje imenovanih entiteta. Funkcioniše tako što mu se prosledi tekst i naziv entiteta koji se ekstrahuje. U našem slučaju, prosleđeni tekst bio je sumarizovani članak, a naziv entiteta koji se pronalazi bio je *“Ingredient”*. Na slici XX vidmo primer kako UNI-NER funkcioniše:

![Slika XX - primer upotrebe UNI-NER-a](Uniner.png)


Nismo imali dovoljno memorije da pokrenemo ovaj model lokalno, te smo ga, umesto toga,  pokrenuli na **_Google Colab_**-u. Nakon što smo ekstrahovali podatke o svakom jelu iz liste, **rekurzivno** smo pozivali funkcije ekstrakcije nad dobijenim sastojcima i taj proces ponavljali dok god postoje podaci o sastojcima. Na taj način smo za svako jelo dobili graf sastojaka. Ubacivanjem tih podataka u postojeću ontologiju dobili smo fajl *ingredients.rdf*.

Nakon što smo ubacili podatke u ontologiju, uvideli smo da naša ontologija ne prepoznaje sinonime. Na primer, sastojci *“sugar”*, *“sugars”* i *“table sugar”* su prepoznavani kao različiti iako predstavljaju isti sastojak. Taj problem smo najpre pokušali da rešimo korištenjem samo **_“word2vec”_** modela, ali on nije dao dovoljno dobre rezultate. Nakon toga smo pokrenuli **_BERT_** *sentence-transformer* za računanje sličnosti:  *“paraphrase-multilingual-MiniLM-L12-v2”*. Prepoznate sinonime sačuvali smo u fajlu *bert_synonyms.csv*. Ipak, ni ovi sinonimi nisu bili savršeno prepoznati, pa smo ih ručno filtrirali i upisali u fajl *filtered_synonyms.csv*. Končano, ove sinonime smo ubacili u ontologiju u fajl *with_synonyms.rdf*. Uveli smo novu tranzitivnu relaciju *hasSynonym*.

S obzirom na to da su podaci o jelima većinski bili automatski generisani i ponekad nepotpuni, odlučili smo da u ontologiju detaljno razradimo jednu vrstu hrane. Opredelili smo se za picu. Krierali smo taksonomiju pica i deo nje je prikazan na slici XX:

![Slika XX - deo taksonomije o picama](onto.png)


## Upiti

## Interfejs aplikacije

## Autori
##### Pavle Glušac, R2 15/2023
##### Nevena Radešić, R2 2/2023
