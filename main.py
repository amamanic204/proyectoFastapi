from fastapi import FastAPI, Request, HTTPException, Form
#you could delete the following line since we are using now templates
# from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select, text
from typing import Annotated

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
class Cambio_Contrasena(SQLModel):
	contrasena_antigua: str
	contrasena_nueva: str



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

# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# @app.get("/productos", response_class=HTMLResponse, include_in_schema=False)

# consultor
@app.get("/", name="index")
def index(request: Request):
	with engine.connect() as conn:
		resultado = conn.execute(text("select * from (select id from producto_bruto where valor like '%iphone%' group by id) join producto on id=producto_id"))
		conn.commit()
		lista = []
		for i in resultado:
			lista.append(i._mapping)
		print(lista)
		return templates.TemplateResponse(request, "index.html", {"productos": lista})

@app.get("/negocio/{negocio_id}", name="negocio")
def negocio(request: Request, negocio_id: int):
	with Session(engine) as session:
		negocio = session.get(Negocio, negocio_id)
		if not negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		resultado = session.exec(text("select * from almacen join producto on almacen.producto_id=producto.producto_id where "+str(negocio_id)+"=1"))
		session.commit()
		lista = []
		for i in resultado:
			lista.append(i._mapping)
		return templates.TemplateResponse(request, "negocio.html", {"productos": lista, "negocio": negocio})


# formularios
@app.get("/acceso", name="acceso")
def acceso(request: Request):
	return templates.TemplateResponse(request, "acceso.html")

@app.post("/acceso", name="acceso")
def acceso(request: Request, vendedor_celular: Annotated[str, Form()], vendedor_contrasena: Annotated[str, Form()]):
	with Session(engine) as session:
		vendedor = session.exec(select(Vendedor).where(Vendedor.vendedor_celular == vendedor_celular)).first()
		if not vendedor:
			return templates.TemplateResponse(request, "acceso.html")
		if (vendedor.vendedor_contrasena == vendedor_contrasena):
			negocio = session.exec(select(Negocio).where(Negocio.vendedor_id == vendedor.vendedor_id)).first()
			if not negocio:
				raise HTTPException(status_code=404, detail="Negocio no encontrado")
			return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": vendedor.vendedor_id, "negocio": negocio})
		else:
			return templates.TemplateResponse(request, "acceso.html")

@app.get("/registro", name="registro_form")
def registro_form(request: Request):
	return templates.TemplateResponse(request, "registro.html")

@app.post("/registro", name="registro")
def registro(request: Request, vendedor: Annotated[Vendedor, Form()]):
	# return templates.TemplateResponse(request, "registro.html")
	with Session(engine) as session:
		if vendedor.vendedor_correo == '':
			vendedor.vendedor_correo = None
		session.add(vendedor)
		session.commit()
		session.refresh(vendedor)
		negocio = Negocio(vendedor_id=vendedor.vendedor_id)
		session.add(negocio)
		session.commit()
		session.refresh(negocio)
		if not negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": vendedor.vendedor_id, "negocio": negocio})
		
# vendedor
@app.get("/vendedor/negocio/{vendedor_id}", name="vendedor_negocio")
def vendedor_negocio(request: Request, vendedor_id: int):
	with Session(engine) as session:
		negocio = session.exec(select(Negocio).where(Negocio.vendedor_id == vendedor_id)).first()
		if not negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": vendedor_id, "negocio": negocio})

@app.get("/vendedor/datos/{vendedor_id}", name="vendedor_datos")
def vendedor_datos(request: Request, vendedor_id:int):
	with Session(engine) as session:
		vendedor = session.get(Vendedor, vendedor_id)
		if not vendedor:
			raise HTTPException(status_code=404, detail="Vendedor no encontrado")
		return templates.TemplateResponse(request, "vendedor_datos.html", {"vendedor_id": vendedor_id, "vendedor": vendedor})

@app.get("/vendedor/gestionar/productos/{vendedor_id}", name="vendedor_gestionar_productos")
def vendedor_gestionar_productos(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id})

@app.get("/vendedor/registrar/productos/{vendedor_id}", name="vendedor_registrar_productos")
def vendedor_registrar_productos(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "vendedor_registrar_productos.html", {"vendedor_id": vendedor_id})

@app.get("/vendedor/salir/{vendedor_id}", name="vendedor_salir")
def vendedor_salir(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "index.html")



# vendedor buscador
@app.get("/vendedor/buscar/{vendedor_id}", name="vendedor_buscar")
def buscar(request: Request, vendedor_id: int, busqueda: str):
	with Session(engine) as session:
		resultado_productos = session.exec(text("select * from (select id from producto_bruto where valor like '%"+busqueda+"%' group by id) join producto on id=producto_id"))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		print('---------------------------------------------')
		print(len(productos))
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "busqueda": busqueda, "productos": productos})





# edicion negocio
@app.get("/negocio/cambiar/visibilidad/{negocio_id}", name="negocio_cambiar_visibilidad")
def negocio_cambiar_visibilidad(request: Request, negocio_id: int):
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		db_negocio.sqlmodel_update({"negocio_visible": not db_negocio.negocio_visible}) 
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		return {'exito': True}


# edicion vendedor
@app.get("/vendedor/cambiar/contrasena/form/{vendedor_id}", name="vendedor_cambiar_contrasena_form")
def vendedor_cambiar_contrasena_form(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "vendedor_cambiar_contrasena_form.html", {"vendedor_id": vendedor_id})

@app.post("/vendedor/cambiar/contrasena/{vendedor_id}", name="vendedor_cambiar_contrasena")
def vendedor_cambiar_contrasena(request: Request, vendedor_id: int, contrasena_antigua: Annotated[str, Form()], contrasena_nueva: Annotated[str, Form()]):	
	with Session(engine) as session:
		db_vendedor = session.get(Vendedor, vendedor_id)
		if not db_vendedor:
			raise HTTPException(status_code=404, detail="Vendedor no encontrado")
		if (db_vendedor.vendedor_contrasena == contrasena_antigua):
			db_vendedor.sqlmodel_update({"vendedor_contrasena": contrasena_nueva})
			session.commit()
			session.refresh(db_vendedor)
			return templates.TemplateResponse(request, "vendedor_datos.html", {"vendedor": db_vendedor})
		else:
			return templates.TemplateResponse(request, "vendedor_cambiar_contrasena_form.html", {"vendedor_id": vendedor_id})

@app.get("/vendedor/cambiar/numero/{vendedor_id}", name="vendedor_cambiar_numero")
def vendedor_cambiar_numero(request: Request, vendedor_id: int):
	return {'exito': False}

@app.get("/vendedor/eliminar/cuenta/{vendedor_id}", name="vendedor_eliminar_cuenta")
def vendedor_eliminar_cuenta(request: Request, vendedor_id: int):
	return {'exito': False}







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
@app.get("/negocio", response_model=list[Negocio])
def read_negocio():
	with Session(engine) as session:
		negocio = session.exec(select(Negocio)).all()
		return negocio
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

# busquedas
def tiendas_tienen_producto(producto_id: int):
	negocios = []
	with Session(engine) as session:
		resultado_negocios = session.exec(text("select negocio.negocio_id, negocio_nombre, negocio_municipio, negocio_zona, negocio_direccion, negocio_descripcion from negocio join almacen on negocio.negocio_id=almacen.negocio_id where producto_id="+str(producto_id)))
		session.commit()
		for i in resultado_negocios:
			negocios.append(i._mapping)
	return negocios

@app.get("/buscar/", name="buscar")
def buscar(request: Request, busqueda: str):
	with Session(engine) as session:
		resultado_productos = session.exec(text("select * from (select id from producto_bruto join almacen on id=producto_id where valor like '%"+busqueda+"%' group by id) join producto on id=producto_id"))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		negocios = []
		if len(productos) == 1:
			negocios = tiendas_tienen_producto(productos[0]['producto_id'])
		return templates.TemplateResponse(request, "index.html", {"busqueda": busqueda,"productos": productos, "negocios": negocios})

@app.get("/buscar/producto/{producto_id}", name="buscar_producto")
def busqueda_producto(request: Request, producto_id: int):
	with Session(engine) as session:
		producto = session.get(Producto, producto_id)
		if not producto:
			raise HTTPException(status_code=404, detail="Producto no encontrado")
		productos = [producto]
		negocios = tiendas_tienen_producto(productos[0].producto_id)
		return templates.TemplateResponse(request, "index.html", {"productos": productos, "negocios": negocios})



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



	

