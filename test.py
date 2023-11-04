from ifcopenshell import open as ifc_open

# Открываем IFC-файл
ifc_file_path = "mad_scientist_212.ifc"
ifc_file = ifc_open(ifc_file_path)

# Получаем все элементы "IfcBuildingStorey" из модели
building_storeys = ifc_file.by_type("IfcBuildingStorey")

# Создаем список для хранения названий планов
plan_names = []

# Проходим по каждому элементу "IfcBuildingStorey" и добавляем названия планов в список
for storey in building_storeys:
    plan_names.append(storey.Name)

# Выводим список планов
print("Список планов:")
for name in plan_names:
    print(name)