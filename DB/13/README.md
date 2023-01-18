<img src="json1.JPG" width=70%>

# 0. CSVからJSONファイルへ書き換え
太郎さんは２つキャラを、花子さんは１つのキャラを持っている
CSV (comma separated value) 
person_ID, first_name, last_name, character_ID, character_name, HP, MP, EXP

CSV
<pre>
(1, 'taro', 'yamada', 1, 'doraemon', 14, 10, 0)
(1, 'taro', 'yamada', 2, 'akinator', 20, 5, 0)
(2, 'hanako', 'sato', 2, 'akinator', 16, 5, 0)
</pre>

JSON
<pre>
{
 "person_id" : "1",
 "first_name" : "yamada",
 "last_name": "taro", 
	"characters" : [
		{
			charater_id : "1",
			character_name : "doraemon", 
			HP : "15",
			MP : "10",
			EXP : "0"
		},
		{
			charater_id : "2",
			character_name : "akinator", 
			HP : "10",
			MP : "15",
			EXP : "5"
		}
	]
}

{
"person_id" : "2", 
 "first_name" : "hanako",
 "last_name": "sato",
	"characters" : [
		{
			charater_id : "1",
			character_name : "doraemon", 
			HP : "15",
			MP : "10",
			EXP : "0"
		}
	]
}	 
</pre>
