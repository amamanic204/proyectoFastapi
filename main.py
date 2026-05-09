from fastapi import FastAPI, Request, HTTPException
#you could delete the following line since we are using now templates
# from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select, text

# modelos
class Vendedor(SQLModel, table=True):
    vendedor_id: int | None = Field(default=None, primary_key=True)
    vendedor_nombre: str
    vendedor_apellido: str
    vendedor_correo: str | None = Field(default=None)
    vendedor_celular: str
    vendedor_contrasena: str
class Negocio(SQLModel, table=True):
    negocio_id: int | None = Field(default=None, primary_key=True)
    vendedor_id: int
    negocio_nombre: str | None = Field(default=None)
    negocio_visible: bool | None = Field(default=True)
    negocio_imagen: str | None = Field(default=None)
    negocio_descripcion: str | None = Field(default=None)
    negocio_municipio: str | None = Field(default=None)
    negocio_zona: str | None = Field(default=None)
    negocio_direccion: str | None = Field(default=None)
    negocio_coordenadas: str | None = Field(default=None)
class Producto(SQLModel, table=True):
    producto_id: int | None = Field(default=None, primary_key=True)
    producto_nombre: str
    producto_imagen: str | None = Field(default=None)
    producto_detalle: str | None = Field(default=None)
class Almacen(SQLModel, table=True):
    negocio_id: int = Field(primary_key=True)
    producto_id: int = Field(primary_key=True)
    producto_precio: str | None = Field(default=None)
    producto_imagen: str | None = Field(default=None)




engine = create_engine("postgresql://postgres:fjarilschmetterling@localhost/proy_unta_beta_v2", echo=True)

def create_db_and_tables():
	SQLModel.metadata.create_all(engine)

# if __name__ == 'main':
# 	create_db_and_tables() 

app = FastAPI()

@app.on_event("startup")
def on_startup():
	create_db_and_tables()

# the name attribute tell us how we can reference in our templates
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

productos: list[dict] = [
	{
		"producto_id": 1,
		"producto_nombre": "Samsung A42",
		"producto_detalle": """nombre: Samsung S20
					empresa: apple
					fecha_lanzamiento: 2020 12 12
		            descripcion: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""",
		"producto_precio": "100 Bs",
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





# CRUD vendedor
@app.post("/vendedor", response_model=Vendedor)
def create_vendedor(vendedor: Vendedor):
	with Session(engine) as session:
		session.add(vendedor)
		session.commit()
		session.refresh(vendedor)
		return vendedor
# @app.get("/hero", response_model=list[Hero])
# def read_hero():
# 	with Session(engine) as session:
# 		hero = session.exec(select(Hero)).all()
# 		return hero
@app.get("/vendedor/{vendedor_id}", response_model=Vendedor)
def read_one_vendedor(vendedor_id: int):
	with Session(engine) as session:
		vendedor = session.get(Vendedor, vendedor_id)
		if not vendedor:
			raise HTTPException(status_code=404, detail="Vendedor no encontrado")
		return vendedor
@app.patch("/vendedor/{vendedor_id}", response_model=Vendedor)
def update_vendedor(vendedor_id: int, vendedor: Vendedor):
	with Session(engine) as session:
		db_vendedor = session.get(Vendedor, vendedor_id)
		if not db_vendedor:
			raise HTTPException(status_code=404, detail="Vendedor no encontrado")
		vendedor_data = vendedor.model_dump(exclude_unset=True)
		db_vendedor.sqlmodel_update(vendedor_data)
		session.add(db_vendedor)
		session.commit()
		session.refresh(db_vendedor)
		return db_vendedor
@app.delete("/vendedor/{vendedor_id}")
def delete_vendedor(vendedor_id: int):
	with Session(engine) as session:
		vendedor = session.get(Vendedor, vendedor_id)
		if not vendedor:
			raise HTTPException(status_code=404, detail="vendedor no encontrado")
		session.delete(vendedor)
		session.commit()
		return {"ok": True}

# CRUD negocio
@app.post("/negocio", response_model=Negocio)
def create_negocio(negocio: Negocio):
	with Session(engine) as session:
		session.add(negocio)
		session.commit()
		session.refresh(negocio)
		return negocio
# @app.get("/hero", response_model=list[Hero])
# def read_hero():
# 	with Session(engine) as session:
# 		hero = session.exec(select(Hero)).all()
# 		return hero
@app.get("/negocio/{negocio_id}", response_model=Negocio)
def read_one_negocio(negocio_id: int):
	with Session(engine) as session:
		negocio = session.get(Negocio, negocio_id)
		if not negocio:
			raise HTTPException(status_code=404, detail="negocio no encontrado")
		return negocio
@app.patch("/negocio/{negocio_id}", response_model=Negocio)
def update_negocio(negocio_id: int, negocio: Negocio):
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="negocio no encontrado")
		negocio_data = negocio.model_dump(exclude_unset=True)
		db_negocio.sqlmodel_update(negocio_data)
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		return db_negocio
	
# CRUD producto
@app.post("/producto", response_model=Producto, name="registrar_producto")
def create_producto(producto: Producto):
	with Session(engine) as session:
		session.add(producto)
		session.commit()
		session.refresh(producto)
		return producto
# @app.get("/hero", response_model=list[Hero])
# def read_hero():
# 	with Session(engine) as session:
# 		hero = session.exec(select(Hero)).all()
# 		return hero
@app.get("/producto/{producto_id}", response_model=Producto)
def read_one_producto(producto_id: int):
	with Session(engine) as session:
		producto = session.get(Producto, producto_id)
		if not producto:
			raise HTTPException(status_code=404, detail="producto no encontrado")
		return producto
@app.patch("/producto/{producto_id}", response_model=Producto)
def update_producto(producto_id: int, producto: Producto):
	with Session(engine) as session:
		db_producto = session.get(Producto, producto_id)
		if not db_producto:
			raise HTTPException(status_code=404, detail="producto no encontrado")
		producto_data = producto.model_dump(exclude_unset=True)
		db_producto.sqlmodel_update(producto_data)
		session.add(db_producto)
		session.commit()
		session.refresh(db_producto)
		return db_producto
@app.delete("/producto/{producto_id}")
def delete_producto(producto_id: int):
	with Session(engine) as session:
		producto = session.get(Producto, producto_id)
		if not producto:
			raise HTTPException(status_code=404, detail="producto no encontrado")
		session.delete(producto)
		session.commit()
		return {"ok": True}

@app.get("/buscar/{busqueda}", name="buscar_producto")
def get_resultados(request: Request, busqueda: str):
	with engine.connect() as conn:
		resultado = conn.execute(text("select * from (select id from producto_bruto where valor like '%"+busqueda+"%' group by id) join producto on id=producto_id"))
		conn.commit()
		lista = []
		for i in resultado:
			lista.append(i._mapping)
		return templates.TemplateResponse(request, "index.html", {"productos": lista})


# engine = create_engine("postgresql://postgres:fjarilschmetterling@localhost/proy_unta_beta_v2", echo=True)

# with engine.connect() as conn:
# 	resultado = conn.execute(text("table vendedor"))
# 	conn.commit()
# 	print([dict(r._mapping) for r in resultado])
	
# CRUD almacen
@app.post("/almacen", response_model=Almacen)
def create_almacen(almacen: Almacen):
	with Session(engine) as session:
		session.add(almacen)
		session.commit()
		session.refresh(almacen)
		return almacen
# @app.get("/hero", response_model=list[Hero])
# def read_hero():
# 	with Session(engine) as session:
# 		hero = session.exec(select(Hero)).all()
# 		return hero
@app.get("/almacen/{negocio_id}/{producto_id}", response_model=Almacen)
def read_one_almacen(negocio_id: int, producto_id: int):
	with Session(engine) as session:
		almacen = session.get(Almacen, (negocio_id, producto_id))
		if not almacen:
			raise HTTPException(status_code=404, detail="almacen no encontrado")
		return almacen
@app.patch("/almacen/{negocio_id}/{producto_id}", response_model=Almacen)
def update_almacen(negocio_id: int, producto_id: int, almacen: Almacen):
	with Session(engine) as session:
		db_almacen = session.get(Almacen, (negocio_id, producto_id))
		if not db_almacen:
			raise HTTPException(status_code=404, detail="almacen no encontrado")
		almacen_data = almacen.model_dump(exclude_unset=True)
		db_almacen.sqlmodel_update(almacen_data)
		session.add(db_almacen)
		session.commit()
		session.refresh(db_almacen)
		return db_almacen
@app.delete("/almacen/{negocio_id}/{producto_id}")
def delete_almacen(negocio_id: int, producto_id: int):
	with Session(engine) as session:
		almacen = session.get(Almacen, (negocio_id, producto_id))
		if not almacen:
			raise HTTPException(status_code=404, detail="almacen no encontrado")
		session.delete(almacen)
		session.commit()
		return {"ok": True}



	





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





