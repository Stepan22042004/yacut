# Проект YaCut  

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.   


### Как запустить проект:  

```  

git clone git@github.com:Stepan22042004/yacut.git  

```  

```  

cd yacut  

```  

Cоздать и активировать виртуальное окружение:  

```  

python3 -m venv venv  


```  

* Если у вас Linux/macOS  

```  

    source venv/bin/activate  

```  



* Если у вас windows  
```
source venv/scripts/activate  

 ```  

Установить зависимости из файла requirements.txt:  

```  

python3 -m pip install --upgrade pip  

```  

```  
pip install -r requirements.txt  

```  

Создание базы данных:  

```  
flask db upgrade 

```  

Команда запуска:  

```  

flask run  
```  
### Стек использованных технологий  

### Язык программирования и фреймворк:  

- **Python**: основной язык программирования. 

- **Flask**: веб-фреймворк для разработки приложений на Python. 
### Тестирование:  

- **Pytest**: для написания тестов.  

### Информация об авторе  

 

Герасимов Степан  

[Stepan_2204](https://t.me/Stepan_2204)

 

### Документация в API 

[openapi.yml](https://github.com/Stepan22042004/yacut/blob/3673b0b5ca2e324de12217fb35133158bf523eaa/openapi.yml) 
