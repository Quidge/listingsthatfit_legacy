#### Template Parsing
---

###### Structure
```
template_parsing/
|-- seller_specific_parsers/
|		|-- parser_id_1/
|		|		|-- <various files and folders specific to this parser> 	[2]
|		|		|-- parse.py 	[2]
|		|		|-- tests/
|		|-- parser_id_2/	[1]
|		|		|-- <various files and folders specific to this parser> 	[2]
|		|		|-- parse.py 	[2]
|		|		|-- tests/
|		|-- ...
|		|-- parser_id_N/	[1]
|		|		|-- <various files and folders specific to this parser> 	[2]
|		|		|-- parse.py 	[2]
|		|		|-- tests/
|		|-- __init__.py
|--	tests/
|-- master_parse.py
|-- exception.py
|-- utils.py
|-- clothing_category_names.py
|-- __init__.py

* __init__.py files aren't included here but are, in actuality, present at every directory level.
```

###### Structure Notes:
`[1]`: This is the imagined naming structure for future parsers
`[2]`: The format is that, at the top level of the specific parser, regarless of whatever else is inside the parser or how it operates (and different parsers could easily operate differently), **all** each `parser_id_N` will have `parser_id_N/parse.py`.

###### General notes:
- The design for master_parse is:
	- Locate correct parser package for the provided parser number.
	- Use the the `parse()` function from the `parse.py` module from that package to pass in the json to be parsed.
	- Return a jsonified ParseResult. Should only throw errors and *not* return a json ParseResult if a unexpected error is encountered when parsing.
- ParseResult has a method, `rehydrate()`, which can take in a jsonified ParseResult and return a new, corresponding ParseResult.
- `template_parsing/clothing_type_names.py` is a mapping of clothing category names. It is understood that the parser would not return a `ParseResult.clothing_type` that was not detailed in `template_parsing/clothing_type_names.py`.
