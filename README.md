для того щоби запустити тестове завдання необхідно:

1)Завантажити цей репозиторій на локальний комп'ютер 

2)Зайти в консоль в директорії де містяться файли з цього репозиторію

3)Виконати наступні команди:
  1.   pip install -r requirements.txt
  2.   uvicorn main:app --reload

4)Далі в строці в консолі писатиме uvicorn running on <localhost:port> (Press CTRL+C to quit), 

5)Зайти в браузер або в postman чи іншу програму та послати запит для перевірки на <localhost:port>

наприклад запит який був предоставлений в описі тех завдання 

localhost:8000/paraphrase?tree=(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP
Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP
(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ
trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS
restaurants) ) ) ) ) ) ) )

для того щоби надіслати запит з власним лімітом треба використати наступний синтаксис

localhost:8000/paraphrase?tree=<...>&limit=<...> де замість <...> підставити дерево та ліміт
