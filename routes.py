from app import app, db
from flask import render_template, request, redirect, url_for, flash
import formularios
from models import Tarea


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", subtitulo="GRUPO 6")


@app.route("/sobrenosotros", methods=["GET", "POST"])
def sobrenosotros():
    formulario = formularios.FormAgregarTareas()

    if formulario.validate_on_submit():
        nueva_tarea = Tarea(titulo=formulario.titulo.data)
        db.session.add(nueva_tarea)
        db.session.commit()
        flash("✅ Tarea creada correctamente", "success")
        return redirect(url_for("listar_tareas"))

    return render_template("sobrenosotros.html", form=formulario)


@app.route("/tareas")
def listar_tareas():
    tareas = Tarea.query.order_by(Tarea.id.asc()).all()
    return render_template("tareas.html", tareas=tareas)


@app.route("/tarea/<int:tarea_id>/editar", methods=["GET", "POST"])
def editar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)

    if request.method == "POST":
        tarea.titulo = request.form.get("titulo")
        db.session.commit()
        flash("✅ Tarea actualizada correctamente", "success")
        return redirect(url_for("listar_tareas"))

    return render_template("editar.html", tarea=tarea)


@app.route("/tarea/<int:tarea_id>/eliminar", methods=["POST"])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    flash(" Tarea eliminada correctamente", "success")
    return redirect(url_for("listar_tareas"))