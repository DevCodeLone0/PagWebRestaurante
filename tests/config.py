# Configuracion centralizada para pruebas

BASE_URL = "http://127.0.0.1:5000"

# Credenciales por rol
ADMIN_EMAIL = "admin@restaurante.com"
ADMIN_PASSWORD = "Admin1234"

CHEF_EMAIL = "chef@test.com"
CHEF_PASSWORD = "Chef1234"

MESERO_EMAIL = "mesero@test.com"
MESERO_PASSWORD = "Mesero1234"

CLIENTE_EMAIL = "cliente@test.com"
CLIENTE_PASSWORD = "Cliente1234"

# Datos de prueba
TEST_PLATO = {
    "nombre": "Plato de Prueba",
    "descripcion": "Plato generado por automatizacion",
    "precio": "25.50",
    "categoria": "platos_fuertes"
}

TEST_PROVEEDOR = {
    "nombre": "Proveedor Test",
    "empresa": "Empresa Test S.A.",
    "telefono": "555-1234",
    "email": "proveedor@test.com",
    "producto": "Ingredientes"
}

TEST_CLIENTE = {
    "nombre": "Cliente Automatizado",
    "telefono": "555-5678",
    "direccion": "Calle Falsa 123"
}
