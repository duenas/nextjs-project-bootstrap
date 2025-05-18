from flask import Flask, render_template, url_for
import requests
import json
import re

app = Flask(__name__)

def fix_json_string(json_str):
    # Fix the double quotes issue with id
    json_str = json_str.replace('"id":4"', '"id":4,"')
    json_str = json_str.replace('"id":5"', '"id":5,"')
    json_str = json_str.replace('"id":6"', '"id":6,"')
    json_str = json_str.replace('"id":7"', '"id":7,"')
    json_str = json_str.replace('"id":8"', '"id":8,"')
    json_str = json_str.replace('"id":9"', '"id":9,"')
    json_str = json_str.replace('"id":10"', '"id":10,"')
    json_str = json_str.replace('"id":11"', '"id":11,"')
    json_str = json_str.replace('"id":12"', '"id":12,"')
    json_str = json_str.replace('"id":13"', '"id":13,"')
    json_str = json_str.replace('"id":14"', '"id":14,"')
    json_str = json_str.replace('"id":15"', '"id":15,"')
    json_str = json_str.replace('"id":16"', '"id":16,"')
    json_str = json_str.replace('"id":17"', '"id":17,"')
    json_str = json_str.replace('"id":18"', '"id":18,"')
    
    # Fix missing commas between objects
    json_str = json_str.replace('}{', '},{')
    
    print("Fixed JSON:", json_str)  # Debug print
    return json_str

def get_categories():
    excluded_categories = ["PRESTAMOS EMPLEADOS", "OTROS GASTOS", "FLETE"]
    try:
        response = requests.get('https://www.fletgohn.com/sift_cat/api/productos/categorias')
        if response.status_code == 200:
            # Fix and parse the JSON response
            fixed_json = fix_json_string(response.text)
            print("Fixed JSON:", fixed_json)  # Debug print
            categories_data = json.loads(fixed_json)
            
            # Extract unique category names, excluding the specified ones
            categories = []
            seen = set()  # To handle duplicate categories
            for item in categories_data:
                category = item.get('categoria')
                if category and category not in excluded_categories and category not in seen:
                    categories.append(category)
                    seen.add(category)
            
            return sorted(categories)
    except Exception as e:
        print(f"Error fetching categories: {e}")
    
    # Fallback categories
    return ["BICICLETA", "MOTOCICLETA", "LUBRICANTES", "FERRETERIA", "REPUESTOS"]

# Sample data for categories and products
catalog = {
    "BICICLETA": [
        {"name": "Bicicleta de Montaña", "code": "BIC001", "price": "L.5000", "image": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=400&q=80", "description": "Bicicleta todo terreno para aventuras."},
    ],
    "MOTOCICLETA": [
        {"name": "Bateria Moto", "code": "MOTO001", "price": "L.1200", "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=400&q=80", "description": "Batería para motos, alta duración y rendimiento."},
    ],
    "LUBRICANTES": [
        {"name": "Aceite Sintético", "code": "LUB001", "price": "L.450", "image": "https://images.unsplash.com/photo-1635274605638-d44babc05a34?auto=format&fit=crop&w=400&q=80", "description": "Aceite sintético de alta calidad."},
    ],
    "FERRETERIA": [
        {"name": "Taladro Eléctrico", "code": "FER001", "price": "L.2500", "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=400&q=80", "description": "Taladro eléctrico potente para uso profesional y doméstico."},
    ],
    "REPUESTOS": [
        {"name": "Kit de Frenos", "code": "REP001", "price": "L.800", "image": "https://images.unsplash.com/photo-1586314580005-dca89e5ecb6d?auto=format&fit=crop&w=400&q=80", "description": "Kit completo de frenos para motos."},
    ],
    "JUGUETES": [
        {"name": "Carro de Control", "code": "JUG001", "price": "L.800", "image": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=400&q=80", "description": "Carro a control remoto para niños."},
    ],
    "BATERIA": [
        {"name": "Batería Auto", "code": "BAT001", "price": "L.2500", "image": "https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?auto=format&fit=crop&w=400&q=80", "description": "Batería para automóvil de larga duración."},
    ],
    "CUATRIMOTO": [
        {"name": "Cuatrimoto 150cc", "code": "CUA001", "price": "L.45000", "image": "https://images.unsplash.com/photo-1621963634744-d72af62f0c8f?auto=format&fit=crop&w=400&q=80", "description": "Cuatrimoto deportiva 150cc."},
    ],
    "LLANTAS": [
        {"name": "Llanta Moto", "code": "LLA001", "price": "L.1200", "image": "https://images.unsplash.com/photo-1586314580005-dca89e5ecb6d?auto=format&fit=crop&w=400&q=80", "description": "Llanta para motocicleta de alto rendimiento."},
    ],
    "CASCO": [
        {"name": "Casco Integral", "code": "CAS001", "price": "L.1500", "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80", "description": "Casco integral para máxima protección."},
    ],
    "ACCESORIOS": [
        {"name": "Guantes Moto", "code": "ACC001", "price": "L.450", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=400&q=80", "description": "Guantes para motociclista."},
    ],
}

whatsapp_number = "50431946109"

@app.route("/")
def home():
    categories = get_categories()
    filtered_catalog = {cat: catalog.get(cat, []) for cat in categories}
    return render_template("index.html", catalog=filtered_catalog, whatsapp_number=whatsapp_number)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
