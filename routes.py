from app import app, db
from flask import render_template, request, redirect, url_for, flash
import formularios
from models import Tarea


# -------------------------
# RUTA PRINCIPAL
# -------------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', subtitulo="Actividad en grupo TAI")


# -------------------------
# CREAR TAREA (FORMULARIO)
# -------------------------
@app.route('/sobrenosotros', methods=['GET', 'POST'])
def sobrenosotros():
    formulario = formularios.FormAgregarTareas()

    if formulario.validate_on_submit():
        nueva_tarea = Tarea(titulo=formulario.titulo.data)
        db.session.add(nueva_tarea)
        db.session.commit()

        flash("Tarea creada correctamente")

        return redirect(url_for('listar_tareas'))

    return render_template('sobrenosotros.html', form=formulario)


# -------------------------
# SALUDO SIMPLE
# -------------------------
@app.route('/saludo')
def saludo():
    return 'Hola bienvenido a Taller Apps'


# -------------------------
# USUARIO DINÁMICO
# -------------------------
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Hola {nombre} bienvenido a Taller Apps'


# -------------------------
# MOSTRAR TODAS LAS TAREAS
# -------------------------
@app.route('/tareas')
def listar_tareas():
    tareas = Tarea.query.all()
    return render_template('tareas.html', tareas=tareas)


# -------------------------
# EDITAR TAREA
# -------------------------
@app.route('/tarea/<int:tarea_id>/editar', methods=['GET', 'POST'])
def editar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)

    if request.method == 'POST':
        tarea.titulo = request.form.get('titulo')
        db.session.commit()

        flash("Tarea actualizada correctamente")
        return redirect(url_for('listar_tareas'))

    return render_template('editar.html', tarea=tarea)


# -------------------------
# ELIMINAR TAREA
# -------------------------
@app.route('/tarea/<int:tarea_id>/eliminar', methods=['POST'])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)

    db.session.delete(tarea)
    db.session.commit()

    flash("Tarea eliminada correctamente")
    return redirect(url_for('listar_tareas'))