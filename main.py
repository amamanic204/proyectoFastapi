from fastapi import FastAPI, Request
#you could delete the following line since we are using now templates
# from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# the name attribute tell us how we can reference in our templates
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

productos: list[dict] = [
	{
		"id": 1,
		"nombre": "Samsung A42",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
	{
		"id": 2,
		"nombre": "Samsung s30",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
	{
		"id": 3,
		"nombre": "Samsung S20",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
	{
		"id": 4,
		"nombre": "Samsung A50",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
	{
		"id": 5,
		"nombre": "Samsung S63",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
	{
		"id": 6,
		"nombre": "Samsung S20",
		"detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"precio": "100 Bs",
	},
]



# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# @app.get("/productos", response_class=HTMLResponse, include_in_schema=False)

# consultor
@app.get("/", include_in_schema=False, name="index")
def index(request: Request):
	return templates.TemplateResponse(request, "index.html", {"productos": productos})

@app.get("/negocio/id_vendedor", include_in_schema=False, name="negocio")
def negocio(request: Request):
	return templates.TemplateResponse(request, "negocio.html")

@app.get("/acceso", name="acceso")
def acceso(request: Request):
	return templates.TemplateResponse(request, "acceso.html")

@app.get("/registro", name="registro")
def registro(request: Request):
	return templates.TemplateResponse(request, "registro.html")


# vendedor
@app.get("/vendedor/negocio/id_vendedor", name="vendedor_negocio")
def vendedor_negocio(request: Request):
	return templates.TemplateResponse(request, "vendedor_negocio.html")

@app.get("/vendedor/adicionar/productos/id_vendedor", name="vendedor_adicionar_productos")
def vendedor_adicionar_productos(request: Request):
	return templates.TemplateResponse(request, "vendedor_adicionar_productos.html")

@app.get("/vendedor/registrar/id_vendedor", name="vendedor_registrar_productos")
def vendedor_registrar_productos(request: Request):
	return templates.TemplateResponse(request, "vendedor_registrar_productos.html")






# ajustes

# @app.get("/ajustes/cambiar/visibilidad/id_vendedor", name="ajustes_cambiar_visibilidad")
# def ajustes_cambiar_contrasena(request: Request):
# 	return templates.TemplateResponse(request, "ajustes_cambiar_visibilidad.html")

# @app.get("/ajustes/cambiar/contrasena/id_vendedor", name="ajustes_cambiar_contrasena")
# def ajustes_cambiar_contrasena(request: Request):
# 	return templates.TemplateResponse(request, "ajustes_cambiar_contrasena.html")

# @app.get("/ajustes/cambiar/numero/id_vendedor", name="ajustes_cambiar_numero")
# def ajustes_cambiar_numero(request: Request):
# 	return templates.TemplateResponse(request, "ajustes_cambiar_numero.html")

# @app.get("/ajustes/eliminar/cuenta/id_vendedor", name="ajustes_eliminar_cuenta")
# def ajustes_eliminar_cuenta(request: Request):
# 	return templates.TemplateResponse(request, "ajustes_eliminar_cuenta.html")





