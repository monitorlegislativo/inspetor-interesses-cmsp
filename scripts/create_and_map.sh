curl -XDELETE 'http://localhost:9200/inspetor/'
curl -XPUT localhost:9200/inspetor -d '{
   "mappings":
   {
    "i":
      { "properties" :
    	{
        "autores" : { "type" : "string", "analyzer" : "keyword" },
        "assuntos" : { "type" : "string", "analyzer" : "keyword" },
        "DataProj" : { "type" : "date", "format" : "dd/MM/YYYY" }
   		} 
	  }	
    }
}'

