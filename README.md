# Step 1. Setup database
(It may take 1 - 2 days, depending on the hardware.)

```
wget http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz
wget http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-category.sql.gz
wget http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-categorylinks.sql.gz

gzip -d enwiki-latest-page.sql.gz
gzip -d enwiki-latest-category.sql.gz
gzip -d enwiki-latest-categorylinks.sql.gz
```

In mysql, create a new database named `enwiki`.
```
> CREATE DATABASE enwiki;
```


Run the sql scripts to add tables. 
```
sudo mysql -u root -p enwiki < enwiki-latest-page.sql
sudo mysql -u root -p enwiki < enwiki-latest-category.sql
sudo mysql -u root -p enwiki < enwiki-latest-categorylinks.sql
```


# Step 2. Dump category edges
Run `./category_edges.sql` to get category links. 
(It may take 30 min - 1 hour, depending on the hardware.)
```
sudo mysql enwiki -uroot -p < category_edges.sql > category_edges.csv
```
# Step 3. Get the Directed Acyclic Graph from the dumped category links
Run the following command to get `DAG.csv` from `category_edges.csv` (10 - 20 minutes).
```
python ./DAG.py
```
