# 0. CSVからJSONファイルへ書き換え

<pre>
(1, 'taro', 'yamada', 0, 'D', 1, 1, 'doraemon', 14, 10, 0)
(1, 'taro', 'yamada', 0, 'D', 1, 2, 'akinator', 20, 5, 0)
(2, 'hanako', 'sato', 0, 'D', 2, 2, 'akinator', 16, 5, 0)

{"peron_id" : "1",
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

{"peron_id" : "2", 
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
