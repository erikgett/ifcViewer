import streamlit as st
from tools import ifchelper
import json
import ifcopenshell

from pathlib import Path

from typing import Optional
import streamlit.components.v1 as components

frontend_dir = (Path(__file__).parent / "frontend-viewer").absolute()

_component_func = components.declare_component("ifc_js_viewer", path=str(frontend_dir))

def ifc_js_viewer(url: Optional[str] = None):
    component_value = _component_func(url=url)
    return component_value

def get_current_ifc_file():
    return session.array_buffer

def draw_3d_viewer():
    session.ifc_js_response = ifc_js_viewer(get_current_ifc_file())


def get_psets_from_ifc_js():
    if session.ifc_js_response:
        return json.loads(session.ifc_js_response)


def format_ifc_js_psets(data):
    return ifchelper.format_ifcjs_psets(data)


def initialise_debug_props(force=False):
    if not "BIMDebugProperties" in session:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }
    if force:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }


def get_object_data(fromId=None):
    def add_attribute(prop, key, value):
        if isinstance(value, tuple) and len(value) < 10:
            for i, item in enumerate(value):
                add_attribute(prop, key + f"[{i}]", item)
            return
        elif isinstance(value, tuple) and len(value) >= 10:
            key = key + "({})".format(len(value))

        propy = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifcopenshell.entity_instance) else None,
        }
        prop.append(propy)

    if session.BIMDebugProperties:
        initialise_debug_props(force=True)
        step_id = 0
        if fromId:
            step_id = int(fromId)
        else:
            step_id = int(session.object_id) if session.object_id else 0
        debug_props = st.session_state.BIMDebugProperties
        debug_props["active_step_id"] = step_id

        crumb = {"name": str(step_id)}
        debug_props["step_id_breadcrumb"].append(crumb)
        element = session.ifc_file.by_id(step_id)
        debug_props["inverse_attributes"] = []
        debug_props["inverse_references"] = []

        if element:
            for key, value in element.get_info().items():
                add_attribute(debug_props["attributes"], key, value)

            for key in dir(element):
                if (
                        not key[0].isalpha()
                        or key[0] != key[0].upper()
                        or key in element.get_info()
                        or not getattr(element, key)
                ):
                    continue
                add_attribute(debug_props["inverse_attributes"], key, getattr(element, key))

            for inverse in session.ifc_file.get_inverse(element):
                propy = {
                    "string_value": str(inverse),
                    "int_value": inverse.id(),
                }
                debug_props["inverse_references"].append(propy)

            print(debug_props["attributes"])


def edit_object_data(object_id, attribute):
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))


def execute():
    initialise_debug_props()
    st.header("🎮 IFC viewer")

    # Кнопка для скриншота
    if st.button('Сделать Скриншот'):
        # JavaScript для создания скриншота
        print("asdfasdf")

    if "ifc_file" in session and session["ifc_file"]:
        if "ifc_js_response" not in session:
            session["ifc_js_response"] = ""
        draw_3d_viewer()

    else:
        st.header("Перед просмотром загрузите ifc-модель")

session = st.session_state

execute()