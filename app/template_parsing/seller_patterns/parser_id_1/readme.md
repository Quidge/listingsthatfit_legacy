*structure*

template_parsing/
|-- seller_specific_parsers/
|		|-- parser_id_1/
|		|		|-- core/
|		|		|		|-- __init__.py
|		|		|		|-- get_table.py
|		|		|		|-- identify_clothing_type.py
|		|		|		|-- director.py
|		|		|-- parse.py
|		|		|-- __init__.py
|		|		|-- tests/
|		|-- parser_id_2/
|		|-- ...
|		|-- parser_id_N/
|		|-- __init__.py
|--	tests/
|-- master_parse.py
|-- exception.py
|-- __init__.py

Notes:
- Different parser_id_N packages may have different structures, but they will ALL have parse.py.
- /parser_id_N/parse.py will have a function, parse(), that will return a standard ParseResult object.
- template_parsing/master_parse.py has a function, parse(), that takes in a seller_parser_id and the json to be parsed. It uses the seller_parser_id to locate the appropriate seller_parsing package/directory.
- template_parsing/master_parse.py returns a json result, even if the parse fails.



parser_id_1
|-- core
|	|-- __init__.py
|	|-- get_table.py
|	|-- id_type.py
|	\-- director.py
|--	tests
|	|--	core_test.py
|	|-- sample1.json
|	|-- sample1_test.py
|	|-- sample2.json
|	|-- sample2_test.py
|	|-- sample3.json
|	|-- sample3_test.py
|	|-- ...
|	|-- ...
|	|-- sample$N.json
|	\-- sample$N_test.py
|-- parse.py
|-- __init__.py
