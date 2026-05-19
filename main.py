from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
#you could delete the following line since we are using now templates
# from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select, text
from typing import Annotated
import shutil
import os

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
app.mount("/media", StaticFiles(directory="media"), name="media")

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
	with Session(engine) as session:
		resultado_productos = session.exec(text("select c.vendedor_id, b.negocio_id, a.producto_nombre, a.producto_id, a.producto_detalle, a.producto_imagen, b.producto_precio from producto a join almacen b on a.producto_id=b.producto_id join negocio c on b.negocio_id=c.negocio_id where vendedor_id="+str(vendedor_id)))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "productos": productos})

@app.get("/vendedor/adicionar/producto/{vendedor_id}/{producto_id}", name="vendedor_adicionar_producto")
def vendedor_adicionar_producto(request: Request, vendedor_id: int, producto_id: int):
	with Session(engine) as session:
		negocios = session.exec(text("select negocio_id from negocio where vendedor_id="+str(vendedor_id)))
		session.commit()
		x = []
		for i in negocios:
			x.append(i._mapping)
		negocio=x[0]
		db_almacen = session.get(Almacen, (negocio.negocio_id, producto_id))
		if not db_almacen:
			almacen = Almacen(negocio_id=negocio.negocio_id, producto_id=producto_id)
			session.add(almacen)
			session.commit()
			session.refresh(almacen)
		else:
			session.delete(db_almacen)
			session.commit()
		resultado_productos = session.exec(text("select c.vendedor_id, b.negocio_id, a.producto_nombre, a.producto_id, a.producto_detalle, a.producto_imagen from producto a join almacen b on a.producto_id=b.producto_id join negocio c on b.negocio_id=c.negocio_id where vendedor_id="+str(vendedor_id)))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "productos": productos})


@app.get("/vendedor/registrar/productos/{vendedor_id}", name="vendedor_registrar_productos_form")
def vendedor_registrar_productos(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "vendedor_registrar_productos_form.html", {"vendedor_id": vendedor_id})

@app.post("/vendedor/registrar/productos/{vendedor_id}", name="vendedor_registrar_productos")
def registro_producto(request: Request, vendedor_id: int, detalle: Annotated[str, Form()]):
	pares = []
	par_nombre=[]
	for linea in detalle.split("\n"):
		par = linea.split(":")
		if len(par) == 2: 
			if par[0].upper() == "NOMBRE":
				par_nombre = par
			else:
				pares.append(par)
	if len(par_nombre) != 2:
		return templates.TemplateResponse(request, "vendedor_registrar_productos_form.html", {"vendedor_id": vendedor_id})

	with Session(engine) as session:
		session.add(Producto(producto_nombre=par_nombre[1], producto_detalle=detalle, producto_imagen="noimage.png"))
		session.commit()
		producto = session.exec(text("select producto_id from producto where producto_nombre=\'"+par_nombre[1]+"\'")).first()
		session.commit()
		if not producto:
			raise HTTPException(status_code=404, detail="Producto registrado INCORRECTAMENTE")
		
		producto_id = producto[0]
		insertar = "insert into producto_bruto values ("+str(producto_id)+", '"+par_nombre[0]+"', '"+par_nombre[1]+"')"
		for par in pares:
			insertar += ", ("+str(producto_id)+", '"+par[0]+"', '"+par[1]+"')"
		session.exec(text(insertar))
		session.commit()
		# ======================================================================================
		# this code is repeated from function 'adicionar' (un poquito mejorado)
		negocio = session.exec(text("select negocio_id from negocio where vendedor_id="+str(vendedor_id))).first()
		session.commit()
		if not negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		negocio_id = negocio[0]
		almacen = Almacen(negocio_id=negocio_id, producto_id=producto_id)
		session.add(almacen)
		session.commit()
		# eso es copiado el 'vendedor buscar' tambien
		resultado_productos = session.exec(text("select c.vendedor_id, b.negocio_id, a.producto_nombre, a.producto_id, a.producto_detalle, a.producto_imagen from producto a join almacen b on a.producto_id=b.producto_id join negocio c on b.negocio_id=c.negocio_id where vendedor_id="+str(vendedor_id)))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "productos": productos})

@app.get("/vendedor/editar/producto/{vendedor_id}/{producto_id}", name="vendedor_editar_producto_form")
def vendedor_editar_producto_form(request: Request, vendedor_id: int, producto_id: int):
	with Session(engine) as session:	
		producto = session.get(Producto, producto_id)
		if not producto:
			raise HTTPException(status_code=404, detail="Producto no encontrado")
		return templates.TemplateResponse(request, "vendedor_editar_producto_form.html", {"vendedor_id": vendedor_id, "producto":	producto})

@app.post("/vendedor/editar/producto/{vendedor_id}/{producto_id}", name="vendedor_editar_producto")
def vendedor_editar_producto(request: Request, vendedor_id: int, producto_id: int, detalle: Annotated[str, Form()]):
	pares = []
	par_nombre=[]
	for linea in detalle.split("\n"):
		par = linea.split(":")
		if len(par) == 2: 
			if par[0].upper() == "NOMBRE":
				par_nombre = par
			else:
				pares.append(par)
	if len(par_nombre) != 2:
		return templates.TemplateResponse(request, "vendedor_editar_productos_form.html", {"vendedor_id": vendedor_id, "producto_id": producto_id})

	with Session(engine) as session:
		db_producto = session.get(Producto, producto_id)
		if not db_producto:
			raise HTTPException(status_code=404, detail="Producto no encontrado")
		db_producto.sqlmodel_update({"producto_nombre": par_nombre[1], "producto_detalle": detalle})
		session.add(db_producto)
		session.commit()
		session.refresh(db_producto)

		producto_id = db_producto.producto_id
		insertar = "insert into producto_bruto values ("+str(producto_id)+", '"+par_nombre[0]+"', '"+par_nombre[1]+"')"
		for par in pares:
			insertar += ", ("+str(producto_id)+", '"+par[0]+"', '"+par[1]+"')"
		session.exec(text(insertar))
		session.commit()
		
		# eso es copiado el 'vendedor buscar' tambien
		resultado_productos = session.exec(text("select c.vendedor_id, b.negocio_id, a.producto_nombre, a.producto_id, a.producto_detalle, a.producto_imagen from producto a join almacen b on a.producto_id=b.producto_id join negocio c on b.negocio_id=c.negocio_id where vendedor_id="+str(vendedor_id)))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "productos": productos})


@app.post("/vendedor/cambiar/precio", name="vendedor_cambiar_precio")
def vendedor_cambiar_precio(request: Request, vendedor_id: Annotated[int, Form()], producto_id: Annotated[int, Form()], producto_precio: Annotated[str, Form()]):
	with Session(engine) as session:
		if producto_precio == " ":
			producto_precio = None
		negocio = session.exec(text("select negocio_id from negocio where vendedor_id="+str(vendedor_id))).first()
		session.commit()
		negocio_id = negocio[0]
		almacen = session.get(Almacen, (negocio_id, producto_id))
		if not almacen:
			nuevo_almacen = Almacen(negocio_id=negocio_id, producto_id=producto_id, producto_precio=producto_precio)
			session.add(nuevo_almacen)
			session.commit()
		else: 		
			almacen.sqlmodel_update({"producto_precio": producto_precio})
			session.add(almacen)
			session.commit()
			session.refresh(almacen)

@app.post("/upload/{vendedor_id}/{producto_id}", name="subir_imagen")
def subir_imagen(request: Request, vendedor_id: int, producto_id: int, file: UploadFile = File(...)):
    
	os.makedirs("media", exist_ok=True)

	file_path = f"media/productos/{file.filename}"

    # Save uploaded file
	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)
	
	with Session(engine) as session:
		db_producto = session.get(Producto, producto_id)
		if not db_producto:
			raise HTTPException(status_code=404, detail="producto no encontrado")
		db_producto.sqlmodel_update({"producto_imagen": file.filename})
		session.add(db_producto)
		session.commit()
		session.refresh(db_producto)
		# return db_producto

		resultado_productos = session.exec(text("select c.vendedor_id, b.negocio_id, a.producto_nombre, a.producto_id, a.producto_detalle, a.producto_imagen from producto a join almacen b on a.producto_id=b.producto_id join negocio c on b.negocio_id=c.negocio_id where vendedor_id="+str(vendedor_id)))
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
		return templates.TemplateResponse(request, "vendedor_gestionar_productos.html", {"vendedor_id": vendedor_id, "productos": productos})



@app.get("/vendedor/salir/{vendedor_id}", name="vendedor_salir")
def vendedor_salir(request: Request, vendedor_id: int):
	return templates.TemplateResponse(request, "index.html")



# vendedor buscador
@app.get("/vendedor/buscar/{vendedor_id}", name="vendedor_buscar")
def buscar(request: Request, vendedor_id: int, busqueda: str):
	with Session(engine) as session:
		resultado_productos = session.exec(text("select * from (select id from producto_bruto where valor like '%"+busqueda+"%' group by id) a left join (select p.producto_id, p.producto_nombre, p.producto_detalle, p.producto_imagen, negocio.negocio_id, negocio.vendedor_id, almacen.producto_precio from producto p left join almacen on p.producto_id=almacen.producto_id left join negocio on almacen.negocio_id = negocio.negocio_id) b on a.id=b.producto_id"))

		# select * from (select id from producto_bruto where valor like '%"+busqueda+"%' group by id) a left join (select producto.producto_id, almacen.negocio_id from producto left join almacen on producto.producto_id=almacen.producto_id) b on a.id=b.producto_id
		# select * from (select id from producto_bruto where valor like '%iphone%' group by id) a left join (select producto.producto_id, almacen.negocio_id from producto left join almacen on producto.producto_id=almacen.producto_id) b on a.id=b.producto_id
		session.commit()
		productos = []
		for i in resultado_productos:
			productos.append(i._mapping)
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
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": db_negocio.vendedor_id, "negocio": db_negocio})

@app.get("/negocio/cambiar/nombre/{negocio_id}/", name="negocio_cambiar_nombre")
def negocio_cambiar_nombre(request: Request, negocio_id: int, nuevo_nombre: str):
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		db_negocio.sqlmodel_update({"negocio_nombre": nuevo_nombre}) 
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": db_negocio.vendedor_id, "negocio": db_negocio})

@app.get("/negocio/cambiar/ubicacion/{negocio_id}/", name="negocio_cambiar_ubicacion")
def negocio_cambiar_ubicacion(request: Request, negocio_id: int, nuevo_municipio: str, nueva_zona: str, nueva_direccion: str):
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		db_negocio.sqlmodel_update({"negocio_municipio": nuevo_municipio, "negocio_zona": nueva_zona, "negocio_direccion": nueva_direccion}) 
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": db_negocio.vendedor_id, "negocio": db_negocio})

@app.post("/negocio/cambiar/imagen/{vendedor_id}/{negocio_id}/", name="negocio_cambiar_imagen")
def negocio_cambiar_imagen(request: Request, vendedor_id: int, negocio_id: int , file: UploadFile = File(...)):
    
	os.makedirs("media", exist_ok=True)

	file_path = f"media/negocios/{file.filename}"

    # Save uploaded file
	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)
	
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		db_negocio.sqlmodel_update({"negocio_imagen": file.filename})
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		# return db_negocio

		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": vendedor_id, "negocio": db_negocio})

@app.get("/negocio/cambiar/descripcion/{negocio_id}/", name="negocio_cambiar_descripcion")
def negocio_cambiar_nombre(request: Request, negocio_id: int, nueva_descripcion: str):
	with Session(engine) as session:
		db_negocio = session.get(Negocio, negocio_id)
		if not db_negocio:
			raise HTTPException(status_code=404, detail="Negocio no encontrado")
		db_negocio.sqlmodel_update({"negocio_descripcion": nueva_descripcion }) 
		session.add(db_negocio)
		session.commit()
		session.refresh(db_negocio)
		return templates.TemplateResponse(request, "vendedor_negocio.html", {"vendedor_id": db_negocio.vendedor_id, "negocio": db_negocio})




# edicion vendedor
@app.post("/vendedor/cambiar/contrasena/form/", name="vendedor_cambiar_contrasena_form")
def vendedor_cambiar_contrasena_form(request: Request, vendedor_id: Annotated[int, Form()]):
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
@app.post("/almacen", response_model=Almacen, name="alma")
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



	

