import streamlit as st
from ifcopenshell import open as ifc_open


def find_plan_with_geometry(ifc_file_path):
    # Открываем IFC-файл
    ifc_file = ifc_open(ifc_file_path)

    # Получаем все элементы "IfcBuildingStorey" из модели
    building_storeys = ifc_file.by_type("IfcBuildingStorey")

    # Проходим по каждому элементу и ищем план с геометрией
    for storey in building_storeys:
        if storey.Representation and storey.Representation.ContextOfItems:
            representation = storey.Representation.ContextOfItems[0].Representation
            if representation.Items:
                # Найден план с геометрией, возвращаем его имя
                return storey.Name

    # Если не найдено плана с геометрией
    return None

# Открываем IFC-файл
ifc_file_path = "mad_scientist_212.ifc"
ifc_file = ifc_open(ifc_file_path)

# Ищем план по имени
plan_name = "Roof Level Upper"

# Получаем все элементы "IfcBuildingStorey" из модели
building_storeys = ifc_file.by_type("IfcBuildingStorey")

# Ищем план с указанным именем
found_plan = None
for storey in building_storeys:
    if storey.Name == plan_name:
        found_plan = storey
        break

# Если план найден, отображаем его
if found_plan:
    # Проверяем наличие представления и геометрии плана
    if found_plan.Representation and found_plan.Representation.ContextOfItems:
        representation = found_plan.Representation.ContextOfItems[0].Representation
        if representation.Items:
            shape = representation.Items[0]

            # Отображаем план в браузере с помощью Streamlit
            st.title("2D-план")
            st.write("Название плана:", found_plan.Name)
            st.image(shape, use_column_width=True)
        else:
            st.write("У плана нет геометрии для отображения.")
    else:
        st.write("План не содержит представления.")
else:
    st.write("План с именем", plan_name, "не найден.")



