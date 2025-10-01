# 📖 Инструкция по использованию кода

Этот набор классов решает задачу **организации потока данных** (donor → recipient).  
Можно воспринимать это как **поставщиков данных (Donor)** и **приёмников (Recipient)**.  
Основная идея:
- `Donor` (донор) генерирует или читает данные (из памяти, из файлов, из базы).
- `Iterator` позволяет итерироваться по этим данным в стиле `for item in donor`.
- `Item` — это единица данных: сам массив + информация (метаданные).
- `Recipient` (приёмник) сохраняет полученные `Item` в нужный формат (например, Zarr).
- `Converter` связывает доноров и приёмников, конвертируя данные из одного формата в другой.

---

## 🔹 Базовые классы

### `Item`

Единица данных: хранит сам массив и информацию о нём.
Объект сделан унифицированным для того, чтобы можно было легко менять доноров и реципиентов, не думаю о несостыковках в данных.

```python
array = np.random.rand(10, 10)

dict = {
	"id": 123
	"sex": "M"
}

item = Item(data=array, info=dict)
print(item)

```


---

### `Donor`

`Donor` — абстрактный источник данных.
При итерировании возвращает объекты `Item`
Чтобы сделать своего донора, нужно унаследоваться и определить:
- `__len__` → возвращает количество элементов
- `_getinfo(index)` → возвращает метаданные (словарь)
- `_getdata(index, info)` → возвращает массив данных


```python
class RandomSamplerDonor(Donor):
    def __init__(self, elem_shape, amount, class_item=Item, batch_size=1):
        super().__init__(class_item=class_item, batch_size=1)
        self.elem_shape = elem_shape
        self.amount = amount
    
    def _getinfo(self, index):
        info = {
            "id": str(uuid.uuid4()),
            "sex": True
        }
        return info

    def _getdata(self, index, info):
        data = np.random.rand(*self.elem_shape).astype("float32")
        return data

    def __len__(self):
        return self.amount
```

Пример итерации:
```python
donor = RandomSamplerDonor(elem_shape=(300, 300), amount=5)

print(f"Total volume: {len(donor)}")
print(f"Element example: {donor[0]}")

item: Item
for item in donor:
	print(item)
```


---

### `ZarrArrayDonor`

Читает данные из **Zarr-хранилища** + CSV-файла с картой.
```python
donor = ZarrArrayDonor(
    store_path="/path/to/zarr/Store",
    map_path="/path/to/mapfile.csv"
)
```

---

### `NpzArrayDonor`

Читает данные из набора `.npz` файлов и карты (`CSV`).

```python
donor = NpzArrayDonor(
    map_path="map.csv",
    data_path="/path/to/npz/"
)

```

---

## 🔹 Приёмники (`Recipient`)
`Recipient` - класс осуществляющий итеративное сохранение датасета.
Сохраняет объекты `Item`

```python
shape = (100, 12, 5000)  # количество элементов × размерность данных
chunks = (1, 12, 5000)

recipient = ZarrArrayRecipient(
    path="./saved_data",
    shape=shape,
    chunks=chunks
)

item = Item(data=np.random.rand(12, 5000), info={"id": "test"})
recipient.save(item)
recipient.close()
```

Совместная работа с донором:
```python

donor = RandomSamplerDonor(elem_shape=(300, 300), amount=500)

recipient = ZarrArrayRecipient(
    path="./saved_data",
    shape=(len(donor), 300, 300),
    chunks=(1, 300, 300)
)

for item in donor:
	recipient.save(item)

print("Data converted")


```

---
## 🔹 Конвертер (`Converter`)

`Converter` - собирает сливки с функционала **доноров** и **приёмников**.
По сути он только лишь выполняет цикл примера, описанного выше.

```python
donors = \
	[
		NpzArrayDonor(map_path="train.csv"),
		NpzArrayDonor(map_path="test.csv")
	]
	
total_length = sum(len(donor) for donor in donors)
recipient = ZarrArrayRecipient(
    path="./zarr_dataset",
    shape=(total_length, 12, 5000),
    chunks=(1, 12, 5000)
)

converter = Converter(
				donors=donors,
				files=["train.csv", "test.csv"], recipient=recipient)
				
converter.convert()
recipient.close()
```

---

## 🔹 Минимальные требования для расширения

Чтобы создать **своего донора**:
- Унаследоваться от `Donor`
- Определить:
    - `__len__(self)` — длина датасета
    - `_getinfo(self, index)` — метаданные
    - `_getdata(self, index, info)` — сами данные

Чтобы создать **своего приёмника**:
- Унаследоваться от `Recipient`
- Определить:
    - `set_index(self, item)` — куда и как сохранять описание
    - `set_data(self, index, item)` — как сохранять данные



## 🌏 Места использования
...