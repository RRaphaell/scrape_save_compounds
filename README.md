# scrape_save_compounds

### prepare environment
```
conda create --name <env_name>
conda activate <env_name>
pip install -r requirements.txt

# run docker
docker-compose up -d
```

### run program
```
python main.py
python main.py -c ADP
python main.py -c ADP STI
```

### show table
```
python main.py -t
```

### run tests
```
python -m pytest
```