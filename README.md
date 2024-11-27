# Py API

**Py API** is a simple REST API for training python code.

## Base structure:

project/
│
├── app.py             
├── config/             
│   ├── __init__.py
│   ├── dev.py
│   ├── prod.py
│   └── test.py
├── domain/            
│   ├── __init__.py
│   └── models.py      
├── dto/                
│   ├── __init__.py
│   └── book_dto.py     
├── filters/            
│   ├── __init__.py
│   └── book_filters.py 
├── repositories/       
│   ├── __init__.py
│   └── book_repository.py 
├── resources/          
│   ├── __init__.py
│   └── book_resource.py  
├── security/           
│   ├── __init__.py
│   └── auth.py        
├── service/           
│   ├── __init__.py
│   └── book_service.py 
├── .env                
├── requirements.txt    
├── tests/             
└── Procfile          
  


