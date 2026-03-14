1. time per query ?
2. ne ajuta cu ceva sa avem timp per query 0.1 daca limita e 5 ? \
3. este query history relevantt ?
3.5. o sa avem mai multe queruri de la acelasi om si atunci ne-ar fi folositor sa ceva cu ele
4. lassoo search/Elasticsearch
5. Nearest Neighbors
Multi-Channel Retrieval.
Bi-Encoder / Cross-Encoder Architectures
interbari cu erori gramaticale
"Two-stage recommender system architecture"
"Candidate generation and ranking pipeline"
"Approximate Nearest Neighbor (ANN) search scaling"
"Multi-stage retrieval RAG"
o sa ruleze de pe pc-urile noastre sau le dam la ceva central de al vostru


PLAN
organizam git
algoritmul de queriuri


1. Etapa de Ingestie și Indexare (Pregătirea Datelor)Înainte de a primi interogări, datele trebuie organizate pentru viteză:Stocare Duală: Companiile sunt salvate într-o bază de date care suportă atât căutare vectorială (pentru descrieri/semantism), cât și filtre exacte (pentru coduri NAICS, locație, venituri).Vectorizarea (Embeddings): Transformați câmpurile text (descriere, oferte de bază) în vectori folosind un Bi-Encoder pentru a permite căutarea rapidă tip ANN (Approximate Nearest Neighbor).
2. Procesarea Interogării (Query Understanding)Când utilizatorul introduce o căutare (ex: "Logistics in Germany"):Analiză și Rescriere: Un modul ușor de AI extrage filtrele structurate (Locație: Germany) și termenii semantici (Logistics).Expandare: Se corectează eventualele greșeli gramaticale pentru a nu rata companii relevante din cauza unui typo.
3. Recuperarea Candidaților (Candidate Generation) - "Sita Mare"Scopul este să reducem milioane de companii la câteva sute în milisecunde:Hybrid Search: Se execută în paralel o căutare pe cuvinte cheie/filtre (Elasticsearch) și o căutare semantică (Vector DB).Filtre Hard: Se elimină direct companiile care nu respectă criteriile obligatorii (ex: locația greșită).
4. Calificarea și Re-clasarea (Ranking & Qualification) - "Sita Fină"Aici se decide dacă un candidat este un "match" perfect sau doar unul "debatable":Scoring (Cross-Encoder): Cele câteva sute de candidați sunt rulați printr-un model mai precis care analizează relația directă dintre query și profilul companiei.LLM Qualification (Opțional/Final): Doar pentru top 10-20 rezultate, se poate folosi un LLM pentru a explica de ce compania se potrivește, asigurând acuratețea fără a sacrifica latența sau costul.
5. Optimizare și ScalabilitateSemantic Caching: Dacă doi utilizatori caută același lucru, rezultatul este servit instant din cache, fără a mai rula pipeline-ul.Monitorizarea Erorilor: Implementarea unor metrici precum NDCG pentru a vedea cât de sus în listă apar companiile cu adevărat relevante (perfect match).